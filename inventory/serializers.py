from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from inventory.models import Categorie, Brand, Unit, Warehouse, Product, Layer1, Layer2, Account, Transaction, Stock, StockPurchase, Sale, SaleItem
from django.contrib.auth.models import User
from rest_framework import serializers
# from djoser.serializers import UserCreateSerializer
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class AddUserCreateSerializer(UserCreateSerializer):
#     first_name = serializers.CharField(required=True)
#     last_name = serializers.CharField(required=True)

#     def create(self, validated_data):
#         user = super().create(validated_data)

#         if User.objects.count() == 1:
#             from .add_data import add_data_function
#             add_data_function()  # Assuming there's a function in add_data module

#         return user

#     class Meta(UserCreateSerializer.Meta):
#         model = User
#         fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'title', 'contact', 'email',
                  'status', 'address', 'balance', 'credit', 'debit']
        read_only_fields = ['credit', 'debit']

    def create(self, validated_data):
        validated_data['is_supplier'] = True
        validated_data['layer1_id'] = 6  # curent liability
        validated_data['layer2_id'] = 12  # supplier
        validated_data['main_layer'] = "liability"
        account = Account.objects.create(**validated_data)
        return account


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'title', 'contact', 'email',
                  'status', 'address', 'balance', 'credit', 'debit']
        read_only_fields = ['credit', 'debit']

    def create(self, validated_data):
        validated_data['is_customer'] = True
        validated_data['layer1_id'] = 1  # curent asset
        validated_data['layer2_id'] = 2  # receivable
        validated_data['main_layer'] = "assets"
        account = Account.objects.create(**validated_data)
        return account


class ProductSerializer(serializers.ModelSerializer):

    unit_name = serializers.SerializerMethodField()

    def get_unit_name(self, obj):
        return obj.unit.name

    category_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj.category.name

    brand_name = serializers.SerializerMethodField()

    def get_brand_name(self, obj):
        return obj.brand.name

    class Meta:
        model = Product
        fields = ['id', 'name', 'image',
                  'note', 'category', 'brand', 'unit', 'unit_name', 'category_name', 'brand_name']


class Layer1Serializer(serializers.ModelSerializer):

    def create(self, validated_data):
        main_layers = self.context['main_layer']
        return Layer1.objects.create(main_layer=main_layers, **validated_data)

    class Meta:
        model = Layer1
        fields = ['id', 'name']


class Layer2Serializer(serializers.ModelSerializer):

    def create(self, validated_data):
        layer1_id = self.context['layer1_id']
        main_layers = self.context['main_layers']
        main_layer = main_layers[0]['main_layer'] if main_layers else None
        return Layer2.objects.create(layer1_id=layer1_id, main_layer=main_layer, **validated_data)

    class Meta:
        model = Layer2
        fields = ['id', 'name']


class CreateAccountSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        layer2_id = self.context['layer2_id']
        main_layers = self.context['main_layers']
        main_layer = main_layers[0]['main_layer'] if main_layers else None
        layer1_ids = self.context['layer1_ids']
        layer1_id = layer1_ids[0]['layer1_id'] if layer1_ids else None
        return Account.objects.create(layer1_id=layer1_id, layer2_id=layer2_id, main_layer=main_layer, **validated_data)

    class Meta:
        model = Account
        fields = ['id', 'title', 'contact', 'email',
                  'status', 'balance', 'address']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'title', 'contact', 'email',
                  'status', 'address', 'balance', 'credit', 'debit']
        read_only_fields = ['balance', 'credit', 'debit']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['description', 'account_id', 'credit', 'transaction_date']


class StockPurchaseSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='transaction.description')
    date = serializers.DateField(source='transaction.transaction_date')
    invoice_no = serializers.IntegerField(source='transaction.invoice_no')
    account_name = serializers.SerializerMethodField()
    warehouse_name = serializers.SerializerMethodField()

    def get_account_name(self, obj):
        return obj.account.title

    def get_warehouse_name(self, obj):
        return obj.warehouse.name

    # def update(self, instance, validated_data):
    #     # Update transaction instance
    #     transaction_data = validated_data.pop('transaction', None)
    #     if transaction_data:
    #         transaction = instance.transaction
    #         transaction.invoice_no = transaction_data.get(
    #             'invoice_no', transaction.invoice_no)
    #         transaction.description = transaction_data.get(
    #             'description', transaction.description)
    #         transaction.credit = validated_data.get(
    #             'amount', transaction.credit)
    #         transaction.transaction_date = transaction_data.get(
    #             'transaction_date', transaction.transaction_date)
    #         transaction.save()

    #     # Update stock purchase instance
    #     instance.quantity = validated_data.get('quantity', instance.quantity)
    #     instance.amount = validated_data.get('amount', instance.amount)
    #     instance.save()

    #     return instance

    class Meta:
        model = StockPurchase
        fields = ['id', 'invoice_no', 'account', 'warehouse', 'transaction',
                  'quantity', 'amount', 'title', 'date', 'account_name', 'warehouse_name']
        read_only_fields = ['transaction']


class StockSerializer(serializers.ModelSerializer):

    account_name = serializers.SerializerMethodField()

    def get_account_name(self, obj):
        return obj.account_supplier.title

    product_name = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        return obj.product.name

    warehouse_name = serializers.SerializerMethodField()

    def get_warehouse_name(self, obj):
        return obj.warehouse.name

    class Meta:
        model = Stock
        fields = ['id', 'account_supplier','stock_purchase', 'warehouse', 'product', 'title',
                  'quantity', 'amount', 'vocuher_type', 'date', 'account_name', 'product_name', 'warehouse_name']
        read_only_fields = ['stock_purchase']
        
    def create(self, validated_data):
      stock_purchase_id = self.context['stock_purchase_id']
      validated_data['vocuher_type'] = 'Purchase'
      return Stock.objects.create(stock_purchase_id=stock_purchase_id, **validated_data)


class SaleSerializer(serializers.ModelSerializer):
    invoice_no = serializers.IntegerField(source='transaction.invoice_no')
    account_name = serializers.SerializerMethodField()
    warehouse_name = serializers.SerializerMethodField()

    def get_account_name(self, obj):
        return obj.account_customer.title

    def get_warehouse_name(self, obj):
        return obj.warehouse.name

    class Meta:
        model = Sale
        fields = ['id', 'invoice_no', 'account_customer', 'warehouse', 'transaction',
                  'quantity', 'amount', 'remarks', 'date', 'account_name', 'warehouse_name']
        read_only_fields = ['transaction']


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['id', 'sale', 'stock', 'product',
                  'quantity', 'amount', 'sale_amount']
        read_only_fields = ['sale','stock','sale_amount']
        
    def create(self, validated_data):
        sale_id = self.context['sale_id']
        sale = SaleItem.objects.create(sale_id=sale_id,**validated_data)
        return sale
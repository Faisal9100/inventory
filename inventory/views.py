# pylint: disable=trailing-whitespace
from ast import literal_eval
import ast
from datetime import datetime
import os
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import *
from .models import *
from .pagination import DefaultPagination
# from django.db.models import Subquery
from rest_framework import viewsets
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db.models import Sum, Max
from rest_framework.decorators import api_view
from inventory import serializers
from django.db.models import F, Value
from django.db.models.functions import Concat
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated
# Create your views here.


class CategorieViewSet(ModelViewSet):
    queryset = Categorie.objects.all().order_by('-id')
    serializer_class = CategorieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['name']
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all().order_by('-id')
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['name']


class UnitViewSet(ModelViewSet):
    queryset = Unit.objects.all().order_by('-id')
    serializer_class = UnitSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['name']


class SupplierViewSet(ModelViewSet):
    queryset = Account.objects.filter(is_supplier=1).order_by('-id')
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['title']


class CustomerViewSet(ModelViewSet):
    queryset = Account.objects.filter(is_customer=1).order_by('-id')
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['title']


class WarehouseViewSet(ModelViewSet):
    queryset = Warehouse.objects.all().order_by('-id')
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['name']


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related(
        'category', 'brand', 'unit').all().order_by('-id')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['name']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Assuming 'image' is the field name for the image file
        image_path = instance.image.path

        # Delete the image file if it exists
        if os.path.exists(image_path):
            os.remove(image_path)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class Layer1ViewSet(viewsets.ModelViewSet):
    serializer_class = Layer1Serializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.keyword is None:
            self.perform_destroy(instance)
        else:
            return Response({'error': 'You cannot delete this row.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        main_layer = self.request.GET.get('main_layer')
        context.update({'main_layer': main_layer})
        return context

    def get_queryset(self):
        return Layer1.objects.filter(main_layer=self.request.GET.get('main_layer')).order_by('-id')


class Layer2ViewSet(ModelViewSet):
    serializer_class = Layer2Serializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.keyword is None:
            self.perform_destroy(instance)
        else:
            return Response({'error': 'You cannot delete this row.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        main_layers = Layer2.objects.filter(
            layer1_id=self.kwargs['layer1_pk']).values('main_layer')
        return {'layer1_id': self.kwargs['layer1_pk'], 'main_layers': main_layers}

    def get_queryset(self):
        return Layer2.objects.filter(layer1_id=self.kwargs['layer1_pk'])


class CreateAccountViewSet(ModelViewSet):
    queryset = Account.objects.all().order_by('-id')
    serializer_class = CreateAccountSerializer
    http_method_names = ['post', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.keyword is None:
            self.perform_destroy(instance)
        else:
            return Response({'error': 'You cannot delete this row.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        main_layers = Layer2.objects.filter(
            id=self.kwargs['layer2_pk']).values('main_layer')
        layer1_ids = Layer2.objects.filter(
            id=self.kwargs['layer2_pk']).values('layer1_id')
        return {'layer2_id': self.kwargs['layer2_pk'], 'layer1_ids': layer1_ids, 'main_layers': main_layers}


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all().order_by('-id')
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['title']
    http_method_names = ['get', 'put', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.keyword is None:
            self.perform_destroy(instance)
        else:
            return Response({'error': 'You cannot delete this row.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StockPurchaseViewSet(viewsets.ModelViewSet):
    queryset = StockPurchase.objects.select_related(
        'account', 'transaction', 'warehouse').all().order_by('-id')
    serializer_class = StockPurchaseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['title']

    def destroy(self, request, pk=None):
        instance = self.get_object()
        stock_purchases = Stock.objects.filter(stock_purchase_id=instance.id)
        if stock_purchases.exists():
            raise ValidationError(
                "Cannot delete stock purchase with child rows in stock.")
        else:
            transaction_id = instance.transaction_id
            stock_purchase_data = StockPurchase.objects.filter(id=instance.id).values(
                'inventory_transaction').first()
            inventory_transaction_id = stock_purchase_data['inventory_transaction']
            # Delete transactions and sale instance
            Transaction.objects.filter(id__in=[
                transaction_id, inventory_transaction_id]).delete()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction_order = TransactionOrder.objects.create(
            vocuher_type="Purchase",
            transaction_date=serializer.validated_data['transaction']['transaction_date']
        )

        # Save transaction instance
        transaction = Transaction.objects.create(
            account_id=serializer.validated_data['account'].id,
            transaction_order_id=transaction_order.id,
            description=serializer.validated_data['transaction']['description'],
            vocuher_type="Purchase",
            transaction_date=serializer.validated_data['transaction']['transaction_date']
        )

        inventory_transaction = Transaction.objects.create(
            account_id=2,
            transaction_order_id=transaction_order.id,
            description=serializer.validated_data['transaction']['description'],
            vocuher_type="Purchase",
            transaction_date=serializer.validated_data['transaction']['transaction_date']
        )

        row_count = StockPurchase.objects.count()
        unique_id = row_count + 1
        # Get the current date in YYYYMMDD format
        current_date = datetime.now().strftime('%Y%m%d')
        invoice = f'PJV-{unique_id}-{current_date}'

       # Save stock purchase instance
        stock_purchase = StockPurchase.objects.create(
            invoice_no=invoice,
            account_id=serializer.validated_data['account'].id,
            warehouse_id=serializer.validated_data['warehouse'].id,
            transaction_id=transaction.id,
            inventory_transaction=inventory_transaction,
            quantity=0,
            amount=0
        )

        # Serialize response data
        response_serializer = self.get_serializer(stock_purchase)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class StockViewSet(ModelViewSet):
    serializer_class = StockSerializer

    def get_queryset(self):
        return Stock.objects.filter(stock_purchase_id=self.kwargs['stocks_purchase_pk']).select_related('account_supplier', 'warehouse', 'stock_purchase', 'product').all().order_by('-id')

    def destroy(self, request, pk=None, stocks_purchase_pk=None):
        instance = self.get_object()

        sale_items = SaleItem.objects.filter(stock_id=instance.id)
        if sale_items.exists():
            raise ValidationError(
                "Cannot delete stock with child rows in sale item.")
        else:
            stock__data = Stock.objects.filter(id=instance.id).values(
                'stock_purchase', 'quantity', 'amount').first()
            stockpurchase_id = stock__data['stock_purchase']
            dec_quantity = stock__data['quantity']
            dec_amount = stock__data['amount']

            stock_purchase_data = StockPurchase.objects.filter(id=stockpurchase_id).values(
                'account', 'transaction', 'inventory_transaction', 'quantity', 'amount').first()
            account_supplier = stock_purchase_data['account']
            transaction_id = stock_purchase_data['transaction']
            inventory_transaction_id = stock_purchase_data['inventory_transaction']
            quantity = stock_purchase_data['quantity']
            amount = stock_purchase_data['amount']

            transaction_credit = Transaction.objects.filter(
                id=transaction_id).values('credit').first()
            credit = transaction_credit['credit'] - dec_amount
            transaction = Transaction.objects.get(id=transaction_id)
            transaction.credit = credit
            transaction.save()

            transaction_debit = Transaction.objects.filter(
                id=inventory_transaction_id).values('debit').first()
            debit = transaction_debit['debit'] - dec_amount
            transactiondebit = Transaction.objects.get(
                id=inventory_transaction_id)
            transactiondebit.debit = debit
            transactiondebit.save()

            total_quantity = quantity - dec_quantity
            total_amount = amount - dec_amount
            stockpurchase = StockPurchase.objects.filter(id=stockpurchase_id).update(
                amount=total_amount, quantity=total_quantity)

            account_balance = Account.objects.filter(
                id=account_supplier).values('balance', 'credit').first()
            credit = account_balance['credit'] - dec_amount
            balance = account_balance['balance'] - dec_amount
            supplier_account = Account.objects.get(id=account_supplier)
            supplier_account.credit = credit
            supplier_account.balance = balance
            supplier_account.save()

            accountbalance = Account.objects.filter(
                id=2).values('balance', 'debit').first()
            debit_balance = accountbalance['balance'] - dec_amount
            debit = accountbalance['debit'] - dec_amount
            account = Account.objects.get(id=2)
            account.debit = debit
            account.balance = debit_balance
            account.save()

            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        stock_purchase_id = self.kwargs['stocks_purchase_pk']
        stock_purchase_data = StockPurchase.objects.filter(id=stock_purchase_id).values(
            'account', 'warehouse', 'transaction', 'inventory_transaction', 'quantity', 'amount').first()
        account_supplier = stock_purchase_data['account']
        warehouse = stock_purchase_data['warehouse']
        transaction_id = stock_purchase_data['transaction']
        inventory_transaction_id = stock_purchase_data['inventory_transaction']
        quantity = stock_purchase_data['quantity']
        amount = stock_purchase_data['amount']

        productid = serializer.validated_data.get('product').id
        priced = serializer.validated_data.get('price')
        dated = serializer.validated_data.get('date')

        check_product = Stock.objects.filter(
            product_id=productid, warehouse_id=warehouse).first()

        if check_product and check_product.price == priced and check_product.date == dated:
            stockid = check_product.id
            stock = Stock.objects.get(id=stockid)
            stock.quantity += serializer.validated_data.get('quantity')
            stock.qty_in += serializer.validated_data.get('quantity')
            stock.amount += serializer.validated_data.get('amount')
            stock.save()

        else:
            stock = Stock.objects.create(
                stock_purchase_id=stock_purchase_id,
                account_supplier_id=account_supplier,
                warehouse_id=warehouse,
                product_id=productid,
                quantity=serializer.validated_data['quantity'],
                qty_in=serializer.validated_data['quantity'],
                price=priced,
                amount=serializer.validated_data['amount'],
                date=dated
            )

        transaction_credit = Transaction.objects.filter(
            id=transaction_id).values('credit').first()
        credit = transaction_credit['credit'] + \
            serializer.validated_data.get('amount')
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.credit = credit
        transaction.save()

        transaction_debit = Transaction.objects.filter(
            id=inventory_transaction_id).values('debit').first()
        debit = transaction_debit['debit'] + \
            serializer.validated_data.get('amount')
        transactiondebit = Transaction.objects.get(id=inventory_transaction_id)
        transactiondebit.debit = debit
        transactiondebit.save()

        total_quantity = quantity + serializer.validated_data.get('quantity')
        total_amount = amount + serializer.validated_data.get('amount')
        stockpurchase = StockPurchase.objects.filter(id=stock_purchase_id).update(
            amount=total_amount, quantity=total_quantity)

        account_balance = Account.objects.filter(
            id=account_supplier).values('balance', 'credit').first()
        credit = account_balance['credit'] + \
            serializer.validated_data.get('amount')
        balance = account_balance['balance'] + \
            serializer.validated_data.get('amount')
        supplier_account = Account.objects.get(id=account_supplier)
        supplier_account.credit = credit
        supplier_account.balance = balance
        supplier_account.save()

        accountbalance = Account.objects.filter(
            id=2).values('balance', 'debit').first()
        debit_balance = accountbalance['balance'] + \
            serializer.validated_data.get('amount')
        debit = accountbalance['debit'] + \
            serializer.validated_data.get('amount')
        account = Account.objects.get(id=2)
        account.debit = debit
        account.balance = debit_balance
        account.save()

        response_serializer = self.get_serializer(stock)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.select_related(
        'account_customer', 'transaction', 'warehouse').all().order_by('-id')
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['remarks']

    def destroy(self, request, pk=None):
        instance = self.get_object()
        sale_items = SaleItem.objects.filter(sale_id=instance.id)
        if sale_items.exists():
            raise ValidationError(
                "Cannot delete sale with child rows in sale item.")

        # Retrieve transaction IDs
        transaction_id = instance.transaction_id
        sale_data = Sale.objects.filter(id=instance.id).values(
            'inventory_transaction', 'cogs_transaction', 'cash_sale_transaction').first()
        inventory_transaction_id = sale_data['inventory_transaction']
        cogs_transaction_id = sale_data['cogs_transaction']
        cash_sale_transaction_id = sale_data['cash_sale_transaction']

        # Delete transactions and sale instance
        Transaction.objects.filter(id__in=[
                                   transaction_id, inventory_transaction_id, cogs_transaction_id, cash_sale_transaction_id]).delete()
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction_order = TransactionOrder.objects.create(
            vocuher_type="Sales",
            transaction_date=serializer.validated_data['date']
        )

        # Save transaction instance
        transaction = Transaction.objects.create(
            account_id=serializer.validated_data['account_customer'].id,
            description=serializer.validated_data['remarks'],
            transaction_order_id=transaction_order.id,
            vocuher_type="Sales",
            transaction_date=serializer.validated_data['date']
        )

        inventory_transaction = Transaction.objects.create(
            account_id=2,
            description=serializer.validated_data['remarks'],
            transaction_order_id=transaction_order.id,
            vocuher_type="Sales",
            transaction_date=serializer.validated_data['date']
        )

        cogs_transaction = Transaction.objects.create(
            account_id=3,
            description=serializer.validated_data['remarks'],
            transaction_order_id=transaction_order.id,
            vocuher_type="Sales",
            transaction_date=serializer.validated_data['date']
        )

        cash_sale_transaction = Transaction.objects.create(
            account_id=4,
            description=serializer.validated_data['remarks'],
            transaction_order_id=transaction_order.id,
            vocuher_type="Sales",
            transaction_date=serializer.validated_data['date']
        )

        row_count = Sale.objects.count()
        unique_id = row_count + 1
        # Get the current date in YYYYMMDD format
        current_date = datetime.now().strftime('%Y%m%d')
        invoice = f'SJV-{unique_id}-{current_date}'

    # Save stock purchase instance
        sale = Sale.objects.create(
            invoice_no=invoice,
            account_customer_id=serializer.validated_data['account_customer'].id,
            warehouse_id=serializer.validated_data['warehouse'].id,
            transaction_id=transaction.id,
            inventory_transaction=inventory_transaction,
            cogs_transaction=cogs_transaction,
            cash_sale_transaction=cash_sale_transaction,
            remarks=serializer.validated_data['remarks'],
            date=serializer.validated_data['date']
        )

        response_serializer = self.get_serializer(sale)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class SaleItemViewSet(ModelViewSet):
    serializer_class = SaleItemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return SaleItem.objects.filter(sale_id=self.kwargs['sales_pk']).select_related('sale', 'stock', 'product').all().order_by('-id')

    def destroy(self, request, pk=None, sales_pk=None):
        instance = self.get_object()

        saleitem_data = SaleItem.objects.filter(id=instance.id).values(
            'sale', 'quantity', 'amount', 'sale_amount', 'stock_id').first()
        sale_id = saleitem_data['sale']
        dec_quantity = saleitem_data['quantity']
        dec_amount = saleitem_data['amount']
        dec_sale_amount = saleitem_data['sale_amount']
        stock_id = saleitem_data['stock_id']

        sale_data = Sale.objects.filter(id=sale_id).values('transaction', 'quantity', 'amount', 'account_customer',
                                                           'warehouse', 'cash_sale_transaction', 'cogs_transaction', 'inventory_transaction', 'sale_amount').first()
        transaction_id = sale_data['transaction']
        cash_sale_transaction_id = sale_data['cash_sale_transaction']
        cogs_transaction_id = sale_data['cogs_transaction']
        inventory_transaction_id = sale_data['inventory_transaction']
        quantity = sale_data['quantity']
        sale_amount = sale_data['sale_amount']
        amount = sale_data['amount']
        warehouse_id = sale_data['warehouse']
        account_id = sale_data['account_customer']

        transaction_debit = Transaction.objects.filter(
            id=transaction_id).values('debit').first()
        debit = transaction_debit['debit'] - dec_sale_amount
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.debit = debit
        transaction.save()

        inventory_transaction_credit = Transaction.objects.filter(
            id=inventory_transaction_id).values('credit').first()
        credit_inventory = inventory_transaction_credit['credit'] - dec_amount
        inventory_transaction = Transaction.objects.get(
            id=inventory_transaction_id)
        inventory_transaction.credit = credit_inventory
        inventory_transaction.save()

        cogs_transaction_debit = Transaction.objects.filter(
            id=cogs_transaction_id).values('debit').first()
        debit_cogs = cogs_transaction_debit['debit'] - dec_amount
        cogs_transaction = Transaction.objects.get(id=cogs_transaction_id)
        cogs_transaction.debit = debit_cogs
        cogs_transaction.save()

        cash_sale_transaction_credit = Transaction.objects.filter(
            id=cash_sale_transaction_id).values('credit').first()
        credit_cash_sale = cash_sale_transaction_credit['credit'] - \
            dec_sale_amount
        cash_sale_transaction = Transaction.objects.get(
            id=cash_sale_transaction_id)
        cash_sale_transaction.credit = credit_cash_sale
        cash_sale_transaction.save()

        total_quantity = quantity - dec_quantity
        total_sale_amount = sale_amount - dec_sale_amount
        total_amount = amount - dec_amount
        sale = Sale.objects.filter(id=sale_id).update(
            amount=total_amount, sale_amount=total_sale_amount, quantity=total_quantity)

        stocks_data = Stock.objects.filter(
            id=stock_id).values('qty_in').first()
        qty_in = stocks_data['qty_in']
        inec_inventory = dec_quantity + qty_in
        stock = Stock.objects.filter(id=stock_id).update(qty_in=inec_inventory)

        account_balance = Account.objects.filter(
            id=account_id).values('balance', 'debit').first()
        debit = account_balance['debit'] - dec_sale_amount
        balance = account_balance['balance'] - dec_sale_amount
        supplier_account = Account.objects.get(id=account_id)
        supplier_account.debit = debit
        supplier_account.balance = balance
        supplier_account.save()

        inventory_account_balance = Account.objects.filter(
            id=2).values('balance', 'credit').first()
        credit_balance = inventory_account_balance['balance'] + dec_amount
        credit = inventory_account_balance['credit'] - dec_amount
        inventory_account = Account.objects.get(id=2)
        inventory_account.credit = credit
        inventory_account.balance = credit_balance
        inventory_account.save()

        cogs_account_balance = Account.objects.filter(
            id=3).values('balance', 'debit').first()
        debitbalance = cogs_account_balance['balance'] - dec_amount
        cogs_debit = cogs_account_balance['debit'] - dec_amount
        account1 = Account.objects.get(id=3)
        account1.debit = cogs_debit
        account1.balance = debitbalance
        account1.save()

        cash_sale_account_balance = Account.objects.filter(
            id=4).values('balance', 'credit').first()
        creditbalance = cash_sale_account_balance['balance'] - dec_sale_amount
        cash_sale_credit = cash_sale_account_balance['credit'] - \
            dec_sale_amount
        cash_sale_account = Account.objects.get(id=4)
        cash_sale_account.credit = cash_sale_credit
        cash_sale_account.balance = creditbalance
        cash_sale_account.save()

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sale_id = self.kwargs['sales_pk']
        sale_data = Sale.objects.filter(id=sale_id).values('transaction', 'quantity', 'amount', 'account_customer',
                                                           'warehouse', 'cash_sale_transaction', 'cogs_transaction', 'inventory_transaction', 'sale_amount').first()
        transaction_id = sale_data['transaction']
        cash_sale_transaction_id = sale_data['cash_sale_transaction']
        cogs_transaction_id = sale_data['cogs_transaction']
        inventory_transaction_id = sale_data['inventory_transaction']
        quantity = sale_data['quantity']
        sale_amount = sale_data['sale_amount']
        amount = sale_data['amount']
        warehouse_id = sale_data['warehouse']
        account_id = sale_data['account_customer']

        product_id = serializer.validated_data.get('product').id
        product_name = Product.objects.filter(
            id=product_id).values('name').first()

        sale_quantity = serializer.validated_data.get('quantity')

        stock_result = Stock.objects.filter(warehouse_id=warehouse_id, product_id=product_id).aggregate(
            total_quantity=Sum('quantity'),
            highest_price=Max('price')
        )

        stock_qty = stock_result['total_quantity'] or 0
        stock_price = stock_result['highest_price']

        saleitem_result = SaleItem.objects.filter(warehouse_id=warehouse_id, product_id=product_id).aggregate(
            total_quantity=Sum('quantity')
        )

        saleitem_qty = saleitem_result['total_quantity'] or 0

        total_left = stock_qty - saleitem_qty
        total_left = max(total_left, 0)

        if stock_price == serializer.validated_data.get('price') or stock_price > serializer.validated_data.get('price'):
            raise serializers.ValidationError(
                {product_name['name']: ["Price can't be less than or Equal to the Default Value"]})

        if total_left < sale_quantity:
            raise serializers.ValidationError(
                {product_name['name']: ["You do not have enough quantity in the stock that you select"]})

        # Check if any stock row has quantity greater than or equal to the desired quantity
        stocks = Stock.objects.filter(
            product_id=product_id, warehouse_id=warehouse_id, qty_in__gte=1).order_by('id')
        purchase_amount = stock_price * sale_quantity
        qty = 0
        add_stocks = []
        for stock in stocks:
            q = sale_quantity - qty
            add_q = 0
            if stock.qty_in >= q:
                stock.qty_in -= q
                qty += q
                add_q = q
            else:
                qty += stock.qty_in
                stock.qty_in -= stock.qty_in
                add_q = stock.qty_in

            if add_q != 0:
                # purchase_amount += add_q * stock.price
                stock_d = [stock.id, add_q, add_q * stock.price]
                add_stocks.append(stock_d)
                stock.save()

            if qty == sale_quantity:
                break

        sale_item = SaleItem.objects.create(
            sale_id=sale_id,
            stock_id=add_stocks[0][0],
            product_id=serializer.validated_data['product'].id,
            warehouse_id=warehouse_id,
            quantity=serializer.validated_data['quantity'],
            sale_amount=serializer.validated_data['amount'],
            price=serializer.validated_data['price'],
            amount=purchase_amount
        )

        transaction_debit = Transaction.objects.filter(
            id=transaction_id).values('debit').first()
        debit = transaction_debit['debit'] + \
            serializer.validated_data.get('amount')
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.debit = debit
        transaction.save()

        inventory_transaction_credit = Transaction.objects.filter(
            id=inventory_transaction_id).values('credit').first()
        credit_inventory = inventory_transaction_credit['credit'] + \
            purchase_amount
        inventory_transaction = Transaction.objects.get(
            id=inventory_transaction_id)
        inventory_transaction.credit = credit_inventory
        inventory_transaction.save()

        cogs_transaction_debit = Transaction.objects.filter(
            id=cogs_transaction_id).values('debit').first()
        debit_cogs = cogs_transaction_debit['debit'] + purchase_amount
        cogs_transaction = Transaction.objects.get(id=cogs_transaction_id)
        cogs_transaction.debit = debit_cogs
        cogs_transaction.save()

        cash_sale_transaction_credit = Transaction.objects.filter(
            id=cash_sale_transaction_id).values('credit').first()
        credit_cash_sale = cash_sale_transaction_credit['credit'] + \
            serializer.validated_data.get('amount')
        cash_sale_transaction = Transaction.objects.get(
            id=cash_sale_transaction_id)
        cash_sale_transaction.credit = credit_cash_sale
        cash_sale_transaction.save()

        total_quantity = quantity + serializer.validated_data.get('quantity')
        total_sale_amount = sale_amount + \
            serializer.validated_data.get('amount')
        total_purchase_amount = amount + purchase_amount
        sale = Sale.objects.filter(id=sale_id).update(
            amount=total_purchase_amount, sale_amount=total_sale_amount, quantity=total_quantity)

        account_balance = Account.objects.filter(
            id=account_id).values('balance', 'debit').first()
        debit = account_balance['debit'] + \
            serializer.validated_data.get('amount')
        balance = account_balance['balance'] + \
            serializer.validated_data.get('amount')
        supplier_account = Account.objects.get(id=account_id)
        supplier_account.debit = debit
        supplier_account.balance = balance
        supplier_account.save()

        inventory_account_balance = Account.objects.filter(
            id=2).values('balance', 'credit').first()
        credit_balance = inventory_account_balance['balance'] - purchase_amount
        credit = inventory_account_balance['credit'] + purchase_amount
        inventory_account = Account.objects.get(id=2)
        inventory_account.credit = credit
        inventory_account.balance = credit_balance
        inventory_account.save()

        cogs_account_balance = Account.objects.filter(
            id=3).values('balance', 'debit').first()
        debitbalance = cogs_account_balance['balance'] + purchase_amount
        cogs_debit = cogs_account_balance['debit'] + purchase_amount
        account1 = Account.objects.get(id=3)
        account1.debit = cogs_debit
        account1.balance = debitbalance
        account1.save()

        cash_sale_account_balance = Account.objects.filter(
            id=4).values('balance', 'credit').first()
        creditbalance = cash_sale_account_balance['balance'] + \
            serializer.validated_data.get('amount')
        cash_sale_credit = cash_sale_account_balance['credit'] + \
            serializer.validated_data.get('amount')
        cash_sale_account = Account.objects.get(id=4)
        cash_sale_account.credit = cash_sale_credit
        cash_sale_account.balance = creditbalance
        cash_sale_account.save()

        response_serializer = self.get_serializer(sale_item)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def WarehouseProduct(request, pk):
    if request.method == 'GET':
        try:
            stock = Stock.objects.filter(warehouse_id=pk)
        except Stock.DoesNotExist:
            return Response({'message': 'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # product_ids = stock.values_list('product_id', flat=True).distinct()
             
        # product_data = []

        # for product_id in product_ids:
        #     

        stock_result = stock.values('price','product_id').annotate(total_quantity=Sum('quantity'))

        product_data = []

        for result in stock_result:   
                stock_qty = result['total_quantity']
                stock_price = result['price']
                product_id = result['product_id']
                
                product = Product.objects.filter(id=product_id).first()

                saleitem_result = SaleItem.objects.filter(warehouse_id=pk, product_id=product_id).aggregate(
                    total_quantity=Sum('quantity')
                )

                saleitem_qty = saleitem_result['total_quantity'] or 0

                total_left = stock_qty - saleitem_qty
                total_left = max(total_left, 0)

                product_data.append({
                    "product_name": product.name,
                    "product_id": product_id,
                    "quantity": total_left,
                    "price": stock_price,
                })

        response_data = {
            "results": product_data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    pagination_class = DefaultPagination
    http_method_names = ['get']

    def get_queryset(self):
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        account_id = self.request.query_params.get('account_id')

        queryset = Transaction.objects.select_related(
            'account').order_by('-id')
        if from_date and to_date:
            queryset = queryset.filter(
                transaction_date__range=[from_date, to_date])

        if account_id:
            queryset = queryset.filter(account_id=account_id)

        return queryset


@api_view(['GET'])
def transaction_details(request, transactions_order_pk):
    if request.method == 'GET':
        try:
            transaction = TransactionOrder.objects.filter(
                id=transactions_order_pk).first()
        except Transaction.DoesNotExist:
            return Response({'message': 'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "transaction_id": transaction.id,
            "transaction_date": transaction.transaction_date,
            "vocuher_type": transaction.vocuher_type,
            "created": transaction.created_at,
            "last_changes": transaction.updated_at
        }

        if transaction.vocuher_type == 'Purchase':

            transactions = Transaction.objects.filter(
                transaction_order_id=transactions_order_pk
            )

            first_transaction_id = transactions.first().id
            stock_purchases = StockPurchase.objects.filter(
                transaction_id=first_transaction_id)
            stocks = Stock.objects.filter(stock_purchase__in=stock_purchases)

            transaction_serializer = TransactionSerializer(
                transactions, many=True)
            stock_serializer = StockSerializer(stocks, many=True)

            response_data = {
                "data": data,
                "transactions": transaction_serializer.data,
                "stocks": stock_serializer.data
            }

            return Response(response_data)

        else:
            transactions = Transaction.objects.filter(
                transaction_order_id=transactions_order_pk
            )

            transaction_serializer = TransactionSerializer(
                transactions, many=True)

            response_data = {
                "data": data,
                "transactions": transaction_serializer.data,
            }

            return Response(response_data)

    else:
        return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TransactionOrderViewSet(ModelViewSet):
    serializer_class = TransactionOrderSerializer
    queryset = TransactionOrder.objects.all()

    def get_queryset(self):
        get = self.request.query_params.get('get')
        if get is not None:
            return TransactionOrder.objects.prefetch_related('transactions__stock_purchase__stocks__product', 'transactions__account').all()
        return super().get_queryset()

    def update_account_balances(self, transaction):
        account = transaction['account']
        account_data = Account.objects.get(id=account)
        account_data.credit += transaction['credit']
        account_data.debit += transaction['debit']

        one = ['liability', 'revenue', 'equity']
        two = ['assets', 'expense']
        
        if account_data.main_layer in one:
            account_data.balance = account_data.credit - account_data.debit
        elif account_data.main_layer in two:
            account_data.balance = account_data.debit - account_data.credit

        account_data.save()

    def check_account_balances(self, transaction):
        if transaction["vocuher_type"] not in ['Purchase', 'Sales']:
            one = ['liability', 'revenue', 'equity']
            two = ['assets', 'expense']

            account = transaction['account']
            account_data = Account.objects.get(id=account)
            account_data.credit += transaction['credit']
            account_data.debit += transaction['debit']

            if account_data.main_layer in one:
                balance = account_data.credit - account_data.debit
            elif account_data.main_layer in two:
                balance = account_data.debit - account_data.credit
            if balance < 0:
                raise serializers.ValidationError(
                    {
                        account_data.title: [
                            "Balance of this account is going to be negative"
                        ]
                    }
                )

    def save_transactions(self, main_transaction, transactions):

        for transaction in transactions:
            self.check_account_balances(transaction)

        for transaction in transactions:
            self.update_account_balances(transaction)

    def create(self, request, *args, **kwargs):
        try:
            req_data = ast.literal_eval(request.data)
        except:
            req_data = request.data
        mainTransaction = {"vocuher_type": req_data["vocuher_type"]}
        try:
            if req_data["transaction_date"]:
                mainTransaction["transaction_date"] = req_data["transaction_date"]
        except:
            pass
        debit = 0
        credit = 0
        transactions = []
        accounts = []
        try:
            req_transaction = ast.literal_eval(req_data["transactions"])
        except:
            req_transaction = req_data['transactions']
        for item in req_transaction:
            try:
                newItem = ast.literal_eval(item)
            except:
                newItem = item
            if newItem["account"] in accounts:
                raise serializers.ValidationError(
                    {
                        "Duplicate Entry": [
                            "Account Dual Entry in one transaction is not allowed."
                        ]
                    }
                )
            data = {
                "account": newItem["account"],
                "description": newItem["description"],
                "vocuher_type": newItem["vocuher_type"],
                "debit": newItem["debit"],
                "credit": newItem["credit"],
            }
            accounts.append(newItem["account"])
            debit += newItem["debit"]
            credit += newItem["credit"]
            transactions.append(data)

        vouchar_type = req_data["vocuher_type"]
        one = ['Cash Receipt', 'Bank Receipt']  # Receipts
        two = ['Cash Payment', 'Bank Payment']  # Payments
        if vouchar_type in two:
            if debit < credit:
                raise serializers.ValidationError(
                    {"Credit": ["Credit can't be more than Debit in Payment"]}
                )
            elif credit < debit:
                cashinhand = Account.objects.get(keyword='#cashInhand')
                data = {
                    "account": cashinhand.id,
                    "debit": 0,
                    "credit": debit - credit,
                }
                transactions.append(data)
        elif vouchar_type in one:
            if debit > credit:
                raise serializers.ValidationError(
                    {"Debit": ["Debit can't be more than Credit in Payment"]}
                )
            elif credit > debit:
                cashinhand = Account.objects.get(keyword='#cashInhand')
                data = {
                    "account": cashinhand.id,
                    "debit": credit - debit,
                    "credit": 0,
                }
                transactions.append(data)

        # Creating Main Transaction -------------------------------
        mainTransactionSerializer = TransactionOrderSerializer(
            data=mainTransaction)
        if mainTransactionSerializer.is_valid():
            main_transaction = mainTransactionSerializer.save()
        else:
            return Response(
                mainTransactionSerializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        # Save the transactions and check balances
        self.save_transactions(main_transaction, transactions)

        # Creating Transactions     -------------------------------
        data = []
        for item in transactions:
            item["transaction_order"] = mainTransactionSerializer.data["id"]
            item["transaction_date"] = req_data["transaction_date"]
            item["vocuher_type"] = req_data["vocuher_type"]
            serializer = CreateTransactionSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        trans = Transaction.objects.filter(
                transaction_order_id=main_transaction.id
            )

        transaction_serializer = TransactionSerializer(
                trans, many=True)

        headers = self.get_success_headers(transaction_serializer.data)
        return Response(
            transaction_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

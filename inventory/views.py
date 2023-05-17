import os
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import CategorieSerializer, BrandSerializer, UnitSerializer, SupplierSerializer, CustomerSerializer, WarehouseSerializer, ProductSerializer, Layer1Serializer, Layer2Serializer, AccountSerializer, CreateAccountSerializer, TransactionSerializer, StockPurchaseSerializer, StockSerializer, SaleSerializer, SaleItemSerializer
from .models import Categorie, Brand, Unit, Account, Warehouse, Product, Layer1, Layer2, Transaction, Stock, StockPurchase, Sale, SaleItem
from .pagination import DefaultPagination
# from django.db.models import Subquery
from rest_framework import viewsets
from rest_framework import status
from rest_framework.exceptions import ValidationError
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated
# Create your views here.

def index(request):
    return render(request, 'index.html')

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
    queryset = Product.objects.select_related('category', 'brand', 'unit').all().order_by('-id')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['name']
    
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
       main_layers = Layer2.objects.filter(layer1_id=self.kwargs['layer1_pk']).values('main_layer')
       return {'layer1_id': self.kwargs['layer1_pk'], 'main_layers': main_layers}

    def get_queryset(self):
        return Layer2.objects.filter(layer1_id=self.kwargs['layer1_pk'])

class CreateAccountViewSet(ModelViewSet):
    queryset= Account.objects.all().order_by('-id')
    serializer_class = CreateAccountSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.keyword is None:
            self.perform_destroy(instance)
        else:
            return Response({'error': 'You cannot delete this row.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        main_layers = Layer2.objects.filter(id=self.kwargs['layer2_pk']).values('main_layer')
        layer1_ids = Layer2.objects.filter(id=self.kwargs['layer2_pk']).values('layer1_id')
        return {'layer2_id': self.kwargs['layer2_pk'], 'layer1_ids': layer1_ids, 'main_layers': main_layers}


class AccountViewSet(ModelViewSet):
    queryset= Account.objects.all().order_by('-id')
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['title']
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.keyword is None:
            self.perform_destroy(instance)
        else:
            return Response({'error': 'You cannot delete this row.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StockPurchaseViewSet(viewsets.ModelViewSet):
    queryset = StockPurchase.objects.select_related('account','transaction', 'warehouse').all().order_by('-id')
    serializer_class = StockPurchaseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['title']
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        stock_purchases = Stock.objects.filter(stock_purchase_id=instance.id)
        if stock_purchases.exists():
            raise ValidationError("Cannot delete stock purchase with child rows in stock.")
        else:
            transaction_id = instance.transaction_id
            Transaction.objects.filter(id=transaction_id).delete()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


    def create(self, request, *args, **kwargs):
     serializer = self.get_serializer(data=request.data)
     serializer.is_valid(raise_exception=True)

     # Save transaction instance
     transaction = Transaction.objects.create(
        invoice_no=serializer.validated_data['transaction']['invoice_no'],
        account_id=serializer.validated_data['account'].id,
        description=serializer.validated_data['transaction']['description'],
        credit=serializer.validated_data['amount'],
        vocuher_type="Purchase",
        transaction_date=serializer.validated_data['transaction']['transaction_date']
     )

    # Save stock purchase instance
     stock_purchase = StockPurchase.objects.create(
        account_id=serializer.validated_data['account'].id,
        warehouse_id=serializer.validated_data['warehouse'].id,
        transaction_id=transaction.id,
        quantity=serializer.validated_data['quantity'],
        amount=serializer.validated_data['amount']
     )
     account_id=serializer.validated_data['account'].id
     
     account_balance = Account.objects.filter(id=account_id).values('balance', 'credit').first()
     credit = account_balance['credit'] + serializer.validated_data.get('amount')
     balance = account_balance['balance'] + serializer.validated_data.get('amount')
     supplier_account = Account.objects.get(id=account_id)
     supplier_account.credit = credit
     supplier_account.balance = balance
     supplier_account.save()

     
     accountbalance = Account.objects.filter(id=2).values('balance', 'debit').first()
     debit_balance = accountbalance['balance'] + serializer.validated_data.get('amount')
     debit = accountbalance['debit'] + serializer.validated_data.get('amount')
     account = Account.objects.get(id=2)
     account.debit = debit
     account.balance = debit_balance
     account.save()

     
     # Serialize response data
     response_serializer = self.get_serializer(stock_purchase)

     return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class StockViewSet(ModelViewSet):
    serializer_class= StockSerializer
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # pagination_class = DefaultPagination
    # search_fields = ['title']
    
    def get_serializer_context(self):
      stock_purchase_pk = self.kwargs['stocks_purchase_pk']
      return {'stock_purchase_id': stock_purchase_pk}

    def get_queryset(self):
        return Stock.objects.filter(stock_purchase_id=self.kwargs['stocks_purchase_pk']).select_related('account_supplier','warehouse', 'stock_purchase','product').all().order_by('-id')
    

class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.select_related('account_customer','transaction', 'warehouse').all().order_by('-id')
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['remarks']
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        sale = SaleItem.objects.filter(sale_id=instance.id)
        if sale.exists():
            raise ValidationError("Cannot delete sale with child rows in sale item.")
        else:
            transaction_id = instance.transaction_id
            Transaction.objects.filter(id=transaction_id).delete()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    def create(self, request, *args, **kwargs):
     serializer = self.get_serializer(data=request.data)
     serializer.is_valid(raise_exception=True)

     # Save transaction instance
     transaction = Transaction.objects.create(
        invoice_no=serializer.validated_data['transaction']['invoice_no'],
        account_id=serializer.validated_data['account_customer'].id,
        description=serializer.validated_data['remarks'],
        credit=serializer.validated_data['amount'],
        vocuher_type="Purchase",
        transaction_date=serializer.validated_data['date']
     )

    # Save stock purchase instance
     sale = Sale.objects.create(
        account_customer_id=serializer.validated_data['account_customer'].id,
        warehouse_id=serializer.validated_data['warehouse'].id,
        transaction_id=transaction.id,
        quantity=serializer.validated_data['quantity'],
        amount=serializer.validated_data['amount'],
        remarks=serializer.validated_data['remarks'],
        date=serializer.validated_data['date']
     )
     
     account_id=serializer.validated_data['account_customer'].id
     
     account_balance = Account.objects.filter(id=account_id).values('balance', 'credit').first()
     credit = account_balance['credit'] + serializer.validated_data.get('amount')
     balance = account_balance['balance'] + serializer.validated_data.get('amount')
     supplier_account = Account.objects.get(id=account_id)
     supplier_account.credit = credit
     supplier_account.balance = balance
     supplier_account.save()
     
     accountbalance = Account.objects.filter(id=2).values('balance', 'credit').first()
     credit_balance = accountbalance['balance'] - serializer.validated_data.get('amount')
     credit = accountbalance['credit'] + serializer.validated_data.get('amount')
     account = Account.objects.get(id=2)
     account.credit = credit
     account.balance = credit_balance
     account.save()
     
     accountbalance1 = Account.objects.filter(id=1).values('balance', 'debit').first()
     debit_balance = accountbalance1['balance'] + serializer.validated_data.get('amount')
     debit = accountbalance1['debit'] + serializer.validated_data.get('amount')
     account1 = Account.objects.get(id=1)
     account1.debit = debit
     account1.balance = debit_balance
     account1.save()
     
     response_serializer = self.get_serializer(sale)

     return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class SaleItemViewSet(ModelViewSet):
    # queryset= SaleItem.objects.select_related('sale','stock','product').all().order_by('-id')
    serializer_class= SaleItemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    # search_fields = ['title']
    
    def get_serializer_context(self):
      sale_pk = self.kwargs['sales_pk']
      return {'sale_id': sale_pk}

    def get_queryset(self):
        return SaleItem.objects.filter(sale_id=self.kwargs['sales_pk']).select_related('sale','stock','product').all().order_by('-id')
    
class WarehouseProductModelViewSet(ModelViewSet):
    serializer_class= StockSerializer
    http_method_names = ['get']
    
    def get_queryset(self):
        return Stock.objects.filter(warehouse_id=self.kwargs['warehouses_pk']).select_related('account_supplier','warehouse', 'stock_purchase','product').all().order_by('-id')

    
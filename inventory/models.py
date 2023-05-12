from django.db import models
# from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator 


# Create your models here.
class Categorie(models.Model):
    name = models.CharField(max_length=255)
    
class Brand(models.Model):
    name = models.CharField(max_length=255)
    
class Unit(models.Model):
    name = models.CharField(max_length=255)
    
class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(null=True)
    status = models.BooleanField(default=False)
    
class Product(models.Model):
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='product_category')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='product_brand')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='product_unit')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    note = models.TextField(null=True)
    
class Layer1(models.Model):
    name = models.CharField(max_length=255)
    MAIN_LAYER_CHOICES = [
        ('assets', 'Assets'),
        ('equity', 'Equity'),
        ('expense', 'Expense'),
        ('liability', 'Liability'),
        ('revenue', 'Revenue'),
    ]
    main_layer = models.CharField(max_length=10, choices=MAIN_LAYER_CHOICES)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class Layer2(models.Model):
    name = models.CharField(max_length=255)
    layer1 = models.ForeignKey('Layer1', on_delete=models.CASCADE)
    MAIN_LAYER_CHOICES = [
        ('assets', 'Assets'),
        ('equity', 'Equity'),
        ('expense', 'Expense'),
        ('liability', 'Liability'),
        ('revenue', 'Revenue'),
    ]
    main_layer = models.CharField(max_length=10, choices=MAIN_LAYER_CHOICES)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class Account(models.Model):
    title = models.CharField(max_length=255)
    layer1 = models.ForeignKey('Layer1', on_delete=models.CASCADE)
    layer2 = models.ForeignKey('Layer2', on_delete=models.CASCADE, blank=True, null=True)
    MAIN_LAYER_CHOICES = [
        ('assets', 'Assets'),
        ('equity', 'Equity'),
        ('expense', 'Expense'),
        ('liability', 'Liability'),
        ('revenue', 'Revenue'),
    ]
    main_layer = models.CharField(max_length=10, choices=MAIN_LAYER_CHOICES)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    credit = models.IntegerField(default=0)
    debit = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    is_supplier = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    ledger_view = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class Transaction(models.Model):
    description = models.TextField()
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    TRANSACTION_STATUS_CHOICES = [
        (1, 'Pending'),
        (2, 'Complete'),
    ]
    transaction_status = models.IntegerField(choices=TRANSACTION_STATUS_CHOICES, blank=True, null=True)
    
    BILL_TYPE_CHOICES = [
        ('Purchase', 'Purchase'),
        ('Cash Payment', 'Cash Payment'),
        ('Bank Payment', 'Bank Payment'),
        ('Cash Receipt', 'Cash Receipt'),
        ('Bank Receipt', 'Bank Receipt'),
    ]
    vocuher_type = models.CharField(max_length=50, choices=BILL_TYPE_CHOICES)
    credit = models.IntegerField(default=0)
    debit = models.IntegerField(default=0)
    invoice_no = models.IntegerField(blank=True, null=True)
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TransactionOrder(models.Model):
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    transaction_date = models.DateField()
    transaction_created = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class StockPurchase(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Stock(models.Model):
    title = models.CharField(max_length=255)
    account_supplier = models.ForeignKey('Account', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    stock_purchase = models.ForeignKey('StockPurchase', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    BILL_TYPE_CHOICES = [
        ('Purchase', 'Purchase'),
        ('Cash Payment', 'Cash Payment'),
        ('Bank Payment', 'Bank Payment'),
        ('Cash Receipt', 'Cash Receipt'),
        ('Bank Receipt', 'Bank Receipt'),
    ]
    vocuher_type = models.CharField(max_length=50, choices=BILL_TYPE_CHOICES)
    amount = models.IntegerField(default=0)
    receive_amount = models.IntegerField(default=0)
    due_amount = models.IntegerField(default=0)
    advance_amount = models.IntegerField(default=0)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

class Sale(models.Model):
    remarks = models.CharField(max_length=255)
    account_customer = models.ForeignKey('Account', on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.IntegerField(default=0)
    receive_amount = models.IntegerField(default=0)
    due_amount = models.IntegerField(default=0)
    advance_amount = models.IntegerField(default=0)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class SaleItem(models.Model):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    sale_amount = models.IntegerField(default=0)
    serial_no = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
# https://bingotingo.com/best-social-media-platforms/



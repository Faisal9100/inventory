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
    category = models.ForeignKey(
        Categorie, on_delete=models.CASCADE, related_name='product_category')
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='product_brand')
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='product_unit')
    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='products/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
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
    layer2 = models.ForeignKey(
        'Layer2', on_delete=models.CASCADE, blank=True, null=True)
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


class TransactionOrder(models.Model):
    BILL_TYPE_CHOICES = [
        ('Purchase', 'Purchase'),
        ('Sales', 'Sales'),
        ('Cash Payment', 'Cash Payment'),
        ('Bank Payment', 'Bank Payment'),
        ('Cash Receipt', 'Cash Receipt'),
        ('Bank Receipt', 'Bank Receipt'),
    ]
    vocuher_type = models.CharField(max_length=50, choices=BILL_TYPE_CHOICES)
    transaction_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Transaction(models.Model):
    description = models.TextField()
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    transaction_order = models.ForeignKey(
        'TransactionOrder', on_delete=models.CASCADE, related_name='transactionorder')

    BILL_TYPE_CHOICES = [
        ('Purchase', 'Purchase'),
        ('Sales', 'Sales'),
        ('Cash Payment', 'Cash Payment'),
        ('Bank Payment', 'Bank Payment'),
        ('Cash Receipt', 'Cash Receipt'),
        ('Bank Receipt', 'Bank Receipt'),
    ]
    vocuher_type = models.CharField(max_length=50, choices=BILL_TYPE_CHOICES)
    credit = models.IntegerField(default=0)
    debit = models.IntegerField(default=0)
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StockPurchase(models.Model):
    invoice_no = models.CharField(max_length=50)
    account = models.ForeignKey(
        'Account',
        limit_choices_to={'is_supplier': True},
        on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    inventory_transaction = models.ForeignKey(
        'Transaction', on_delete=models.CASCADE, related_name='inventoy_transaction')
    quantity = models.IntegerField()
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Stock(models.Model):
    title = models.CharField(max_length=255)
    account_supplier = models.ForeignKey(
        'Account',
        limit_choices_to={'is_supplier': True},
        on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    stock_purchase = models.ForeignKey(
        'StockPurchase', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    qty_in = models.IntegerField()
    price = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Sale(models.Model):
    invoice_no = models.CharField(max_length=50)
    remarks = models.CharField(max_length=255)
    account_customer = models.ForeignKey('Account',
                                         limit_choices_to={
                                             'is_customer': True},
                                         on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    cogs_transaction = models.ForeignKey(
        'Transaction', on_delete=models.CASCADE, related_name='cogs_transaction')
    cash_sale_transaction = models.ForeignKey(
        'Transaction', on_delete=models.CASCADE, related_name='cash_sale_transaction')
    inventory_transaction = models.ForeignKey(
        'Transaction', on_delete=models.CASCADE, related_name='inventory_transaction')
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    sale_amount = models.IntegerField(default=0)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SaleItem(models.Model):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    stock = models.ForeignKey(
        'Stock', on_delete=models.CASCADE, related_name='sale_stock')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    sale_amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# https://bingotingo.com/best-social-media-platforms/

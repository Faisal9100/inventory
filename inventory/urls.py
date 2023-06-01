from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategorieViewSet, basename='categories')
router.register(r'brands', views.BrandViewSet, basename='brands')
router.register(r'units', views.UnitViewSet, basename='units')
router.register(r'warehouses', views.WarehouseViewSet, basename='warehouses')
router.register(r'Suppliers', views.SupplierViewSet, basename='Suppliers')
router.register(r'customers', views.CustomerViewSet, basename='customers')
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'layer1s', views.Layer1ViewSet, basename='layer1s')
router.register(r'layer2s', views.Layer2ViewSet, basename='layer2')
router.register(r'accounts', views.AccountViewSet, basename='accounts')
router.register(r'stocks_purchase', views.StockPurchaseViewSet,
                basename='stocks_purchase')
router.register(r'vouchar', views.TransactionOrderViewSet, basename='vouchars')
router.register(r'sales', views.SaleViewSet, basename='sales')
router.register(r'transactions', views.TransactionViewSet, basename='transactions')

layer2_router = routers.NestedDefaultRouter(
    router, r'layer1s', lookup='layer1')
layer2_router.register(r'layer2s', views.Layer2ViewSet, basename='layer2')

account_router = routers.NestedDefaultRouter(
    router, r'layer2s', lookup='layer2')
account_router.register(
    r'accounts', views.CreateAccountViewSet, basename='account')

stock_router = routers.NestedDefaultRouter(
    router, r'stocks_purchase', lookup='stocks_purchase')
stock_router.register(r'stocks', views.StockViewSet, basename='stock')

sale_item_router = routers.NestedDefaultRouter(
    router, r'sales', lookup='sales')
sale_item_router.register(
    r'sale_items', views.SaleItemViewSet, basename='sale_item')

# transactions_router = routers.NestedDefaultRouter(
#     router, r'transactions', lookup='transactions')
# transactions_router.register(
#     r'details', views.TransactionDetailsViewSet, basename='detail')

# warehouseproduct_router = routers.NestedDefaultRouter(
#     router, r'warehouses', lookup='warehouses')
# warehouseproduct_router.register(
#     r'stock_is', views.Warehouse2ProductModelViewSet, basename='stock')


urlpatterns = [

    path('', include(router.urls)),
    path('', include(layer2_router.urls)),
    path('', include(account_router.urls)),
    path('', include(stock_router.urls)),
    path('', include(sale_item_router.urls)),
    # path('', include(transactions_router.urls)),
    # path('', include(warehouseproduct_router.urls)),
    path('warehouses/<int:pk>/stocks/',
         views.WarehouseProduct, name='get_stocks_quantity'),
    path('transactions_order/<int:transactions_order_pk>/details/',
         views.transaction_details, name='transactions_details'),

]

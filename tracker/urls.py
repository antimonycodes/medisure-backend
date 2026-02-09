from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .auth_views import signup, signin

router = DefaultRouter()
router.register(r'manufacturers', views.ManufacturerViewSet)
router.register(r'distributors', views.DistributorViewSet)
router.register(r'pharmacies', views.PharmacyViewSet)
router.register(r'batches', views.BatchViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'inventory', views.PharmacyInventoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('mint/', views.mint_batch, name='mint-batch'),
    path('verify/<str:qr_code>/', views.verify_medicine, name='verify-medicine'),
    path('journey/<str:batch_id>/', views.track_journey, name='track-journey'),
    path('transfer/', views.transfer_batch, name='transfer-batch'),
    path('auth/signup/', signup, name='signup'),
    path('auth/signin/', signin, name='signin'),
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
    path('pharmacy/dashboard/', views.pharmacy_dashboard_stats, name='pharmacy-dashboard-stats'),
    path('pharmacy/receive/', views.receive_batch, name='pharmacy-receive-batch'),
    path('pharmacy/<str:pharmacy_id>/inventory/', views.pharmacy_inventory, name='pharmacy-inventory'),
    path('cart/', views.get_cart, name='get-cart'),
    path('cart/add/', views.add_to_cart, name='add-to-cart'),
    path('cart/remove/<str:item_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/update/<str:item_id>/', views.update_cart_item, name='update-cart-item'),
    path('cart/clear/', views.clear_cart, name='clear-cart'),
    path('orders/create/', views.create_order, name='create-order'),
    path('orders/<str:order_id>/', views.get_order, name='get-order'),
    path('orders/', views.get_user_orders, name='get-user-orders'),
    path('orders/<str:order_id>/status/', views.update_order_status, name='update-order-status'),
    path('users/<int:user_id>/', views.get_user, name='get-user'),
    path('users/', views.list_users_by_role, name='list-users'),
    path('marketplace/', views.list_marketplace_drugs, name='marketplace'),
]
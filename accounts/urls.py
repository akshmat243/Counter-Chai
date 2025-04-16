from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add-vendor/', views.add_vendor, name='add_vendor'),
    path('add-counter/', views.add_counter, name='add_counter'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-customer/', views.add_customer, name='add_customer'),
    path('products/', views.product_view, name='products'),
    path('qr/', views.generate_qr, name='generate_qr'),

    
]

from django.urls import path
# from django.contrib.auth.views import LoginView
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('items/', items, name='items'),
    path('orders/', orders, name='orders'),
    path('create_order/<int:pk>/', create_order, name='create_order'),
    path('update_order/<int:pk>/', update_order, name='update_order'),
    path('delete_order/<int:pk>/', delete_order, name='delete_order'),
    path('delete_all_order/', delete_all_order, name='delete_all'),
    path('customers/<int:pk>/', customers, name='customers'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('user/', UserPage, name='user'),
    # path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
]

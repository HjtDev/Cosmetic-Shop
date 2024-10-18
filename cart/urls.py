from django.urls import path
from . import views


app_name = 'cart'


urlpatterns = [
    path('', views.cart_list_view, name='cart_list'),
    path('add/', views.add_view, name='add_to_cart')
]

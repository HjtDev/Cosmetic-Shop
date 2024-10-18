from django.urls import path
from . import views


app_name = 'cart'


urlpatterns = [
    path('', views.cart_list_view, name='cart_list'),
    path('add/', views.add_cart_view, name='add_to_cart'),
    path('update/', views.update_cart_view, name='update_cart'),
]

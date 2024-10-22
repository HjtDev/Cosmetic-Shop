from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path('complete/', views.checkout_view, name='checkout')
]

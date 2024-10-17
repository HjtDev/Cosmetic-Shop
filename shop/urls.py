from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('like/', views.like_view, name='like')
]

from django.urls import path
from . import views


app_name = 'product'


urlpatterns = [
    path('detail/<slug:slug>/', views.product_detail_view, name='detail_view'),
    path('detail/<slug:slug>/comment/', views.comment_view, name='comment'),
    path('all/', views.product_list_view, name='list_view'),
    path('category/<slug:slug>/', views.product_category_view, name='category_view')
]
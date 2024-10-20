from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('like/', views.like_view, name='like'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('faq/', views.faq_view, name='faq'),
    path('contact/', views.contact_view, name='contact')
]

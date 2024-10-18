from django.urls import path
from . import views


app_name = 'account'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/verify/', views.verify_view, name='verify')
]

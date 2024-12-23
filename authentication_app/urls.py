from django.urls import path
from . import views

app_name = 'authentication_app'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),  
    path('register/', views.CustomRegisterView.as_view(), name='register'), 
    path('logout/', views.CustomLogoutView.as_view(), name='logout'), 
]

from django.urls import path
from .views import signup, login_view
from . import views

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('shopping/', views.shopping_items, name='shopping_items'),
    
      path('signup_view/', views.signup_view, name='signup_view'),
       path('login_view_view/', views.login_view_view, name='login_view_view'),
       path('filter/',views.ProductFilterAPIView.as_view(), name='filter_products'),
]


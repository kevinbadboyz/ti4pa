from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    TableRestoListApiView, TableRestoDetailApiView,
    LoginView, LogoutView, RegisterWaitressAPI, ProfileDetailApiView, 
    CategoryListApiView, CategoryDetailApiView,
    MenuRestoListApiView, MenuRestoDetailApiView,
    OrderMenuListApiView, OrderMenuFilterApi,
    OrderMenuDetailListAPIView, OrderMenuDetailCreateApiView,
)
app_name = 'api'

urlpatterns = [    
    path('api/v1/login', LoginView.as_view()),
    path('api/v1/logout', LogoutView.as_view()),
    path('api/v1/register', RegisterWaitressAPI.as_view()),
    path('api/v1/profile/<int:user_id>', ProfileDetailApiView.as_view()),    
    path('api/table-resto', TableRestoListApiView.as_view()),
    path('api/table-resto/<int:id>', TableRestoDetailApiView.as_view()),
    path('api/category', CategoryListApiView.as_view()),
    path('api/category/<int:id>', CategoryDetailApiView.as_view()),
    path('api/menu-resto', MenuRestoListApiView.as_view()),
    path('api/menu-resto/<int:id>', MenuRestoDetailApiView.as_view()),
    path('api/order-menu', OrderMenuListApiView.as_view()),
    path('api/order-menu/filter/', OrderMenuFilterApi.as_view()),
    path('api/order-menu-detail', OrderMenuDetailCreateApiView.as_view()),
    path('api/order-menu-detail/search/', OrderMenuDetailListAPIView.as_view()),
]


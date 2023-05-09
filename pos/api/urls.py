from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    TableRestoListApiView, TableRestoDetailApiView,
    LoginView, LogoutView, RegisterWaitressAPI,
    ProfileDetailApiView, CategoryList, CategoryDetail,
    MenuRestoList, MenuRestoDetail,
)
app_name = 'api'

urlpatterns = [    
    path('api/v1/login', LoginView.as_view()),
    path('api/v1/logout', LogoutView.as_view()),
    path('api/v1/register', RegisterWaitressAPI.as_view()),
    path('api/v1/profile/<int:user_id>', ProfileDetailApiView.as_view()),    
    path('api/table-resto', TableRestoListApiView.as_view()),
    path('api/table-resto/<int:id>', TableRestoDetailApiView.as_view()),
    path('api/category', CategoryList.as_view()),
    path('api/category/<pk>', CategoryDetail.as_view()),
    path('api/menu-resto', MenuRestoList.as_view()),
    path('api/menu-resto/<pk>', MenuRestoDetail.as_view()),
]


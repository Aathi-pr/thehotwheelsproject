from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Car URLs
    path('car/<slug:slug>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/add/new/', views.car_create, name='car_add'),
    path('car/<slug:slug>/edit/', views.car_update, name='car_edit'),
    path('car/<slug:slug>/delete/', views.car_delete, name='car_delete'),
    
    # Case URLs
    path('case/<str:case_name>/', views.case_detail, name='case_detail'),
    path('case/add/new/', views.case_create, name='case_add'),
    path('case/<str:case_name>/edit/', views.case_update, name='case_edit'),
    path('case/<str:case_name>/delete/', views.case_delete, name='case_delete'),
    
    # Series URLs
    path('series/<slug:slug>/', views.series_detail, name='series_detail'),
    path('series/add/new/', views.series_create, name='series_add'),
    path('series/<slug:slug>/edit/', views.series_update, name='series_edit'),
    path('series/<slug:slug>/delete/', views.series_delete, name='series_delete'),
    
    # Manage Collection
    path('manage/', views.manage_collection, name='manage_collection'),
]

from . import views
from django.urls import path

app_name = 'crm'
urlpatterns = [
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('customers/add/', views.CustomerCreateView.as_view(), name='customer-add'),
    path('customers/<int:pk>/', views.CustomerUpdateView.as_view(), name='customer-modify'),
    path('', views.Dashboard.as_view(), name='dashboard'),
]

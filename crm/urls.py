from . import views
from django.urls import path

app_name = 'crm'
urlpatterns = [
    path('', views.Dummy.as_view(), name='dashboard'),
]

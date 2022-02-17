from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'customers', views.CustomerViewset)
router.register(r'addresses', views.CustomerAddressViewset)
router.register(r'documents', views.CustomerDocumentViewset)
router.register(r'customers/(?P<customer>[0-9]+)/addresses', views.CustomerAddressViewset, basename='cust-addresses')
router.register(r'customers/(?P<customer>[0-9]+)/documents', views.CustomerDocumentViewset, basename='cust-documents')

# The API URLs are now determined automatically by the router.
app_name = 'api'
urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('', include(router.urls)),
]

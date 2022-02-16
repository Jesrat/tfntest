from .views import CustomerViewset, CustomerAddressViewset, CustomerDocumentViewset
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'customers', CustomerViewset)
router.register(r'customers/(?P<customer>[0-9]+)/addresses', CustomerAddressViewset)
router.register(r'customers/(?P<customer>[0-9]+)/documents', CustomerDocumentViewset)

# The API URLs are now determined automatically by the router.
app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]

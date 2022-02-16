from .filters import CustomerFilterBackend
from .serializers import CustomerSerializer, CustomerAddressSerializer, CustomerDocumentSerializer
from crm.models import Customer, CustomerAddress, CustomerDocument
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class CustomerViewset(ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerAddressViewset(ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    filter_backends = [CustomerFilterBackend]
    permission_classes = [IsAuthenticated]
    queryset = CustomerAddress.objects.all()
    serializer_class = CustomerAddressSerializer

    def perform_create(self, serializer):
        return serializer.save(customer=get_object_or_404(Customer, id=self.kwargs['customer']))


class CustomerDocumentViewset(ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    filter_backends = [CustomerFilterBackend]
    permission_classes = [IsAuthenticated]
    queryset = CustomerDocument.objects.all()
    serializer_class = CustomerDocumentSerializer

    def perform_create(self, serializer):
        return serializer.save(customer=get_object_or_404(Customer, id=self.kwargs['customer']))

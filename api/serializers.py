from crm.models import Customer, CustomerDocument, CustomerAddress
from rest_framework import serializers

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = ['id', 'address_type', 'address']


class CustomerDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDocument
        fields = ['id', 'document_type', 'document']


class CustomerSerializer(serializers.ModelSerializer):
    addresses = CustomerAddressSerializer(many=True, required=False)
    documents = CustomerDocumentSerializer(many=True, required=False)
    class Meta:
        model = Customer
        fields = '__all__'

from .models import Customer, CustomerAddress, CustomerDocument
from core.forms import ModelFormControl
from django import forms
from django.utils.translation import gettext_lazy as _


class CustomerForm(ModelFormControl):
    form_control_exclude = ['birth_date']
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control date'}),
        label=_('Birth Date')
    )

    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'form-control date'})
        }


class CustomerAddressForm(ModelFormControl):
    form_control_exclude = ['address_type']
    id_address = forms.CharField(widget=forms.HiddenInput(attrs={'name': 'id_address[]'}))

    class Meta:
        model = CustomerAddress
        fields = ['address_type', 'address']
        labels = {'address': _('Address')}
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'name': 'address[]'}),
            'address_type': forms.Select(attrs={'data-live-search': 'true', 'class': 'form-control chosen-select'})
        }

class CustomerDocumentForm(ModelFormControl):
    form_control_exclude = ['document_type']
    id_document = forms.CharField(widget=forms.HiddenInput(attrs={'name': 'id_document[]'}))

    class Meta:
        model = CustomerDocument
        fields = ['document_type', 'document']
        labels = {'address': _('Document')}
        widgets = {
            'document': forms.Textarea(attrs={'rows': 2, 'name': 'document[]'}),
            'document_type': forms.Select(attrs={'data-live-search': 'true', 'class': 'form-control chosen-select'})
        }

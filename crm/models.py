from django.db import models
from django.utils.translation import gettext_lazy as _

html_table = {
    'attrs': [('class', 'table table-striped table-bordered')],
    'controls': ['delete', 'update', 'create', 'detail'],
}


# Create your models here.
class Customer(models.Model):
    names = models.CharField(_('names'), max_length=100)
    last_names = models.CharField(_('last names'), max_length=100)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    notes = models.TextField(_('notes'), null=True, blank=True)

    html_table = {
        **html_table,
        'td': [
            {'title': _('Id'), 'model_attr': 'id', },
            {'title': _('Names'), 'model_attr': 'names', },
            {'title': _('Last Names'), 'model_attr': 'last_names', },
            {'title': _('Birth Date'), 'model_attr': 'birth_date', },
        ]
    }

    def __str__(self):
        return '%s %s' % (self.names, self.last_names)

    class Meta:
        db_table = 'crm_customers'
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')


class CustomerDocument(models.Model):
    class DocType(models.TextChoices):
        dui = 'DUI', _('DUI')
        nit = 'NIT', _('NIT')
        other = 'OTHER', _('OTHER')
        passport = 'PASSPORT', _('PASSPORT')

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='documents', verbose_name=_('customer')
    )
    document_type = models.CharField(
        _('document type'), choices=DocType.choices, default=DocType.dui, max_length=100
    )
    document = models.CharField(_('document'), max_length=100)

    html_table = {
        **html_table,
        'td': [
            {'title': _('Id'), 'model_attr': 'id', },
            {'title': _('Customer'), 'model_attr': 'customer', },
            {'title': _('Doc Type'), 'model_attr': 'document_type', },
            {'title': _('Document'), 'model_attr': 'document', },
        ]
    }

    class Meta:
        db_table = 'crm_customer_documents'
        verbose_name = _('Customer Document')
        verbose_name_plural = _('Customer Documents')

    def __str__(self):
        return '%s - %s' % (self.customer, self.document)

    @property
    def to_report(self):
        return [
            self.customer.id, self.customer.names, self.customer.last_names, self.id, self.document_type, self.document
        ]


class CustomerAddress(models.Model):
    class AddressType(models.TextChoices):
        home = 'HOME', _('HOME')
        work = 'WORK', _('WORK')
        other = 'OTHER', _('OTHER')

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('customer')
    )
    address_type = models.CharField(
        _('address type'), choices=AddressType.choices, default=AddressType.home, max_length=100
    )
    address = models.TextField(_('address'))
    html_table = {
        **html_table,
        'td': [
            {'title': _('Id'), 'model_attr': 'id', },
            {'title': _('Customer'), 'model_attr': 'customer', },
            {'title': _('Address Type'), 'model_attr': 'address_type', },
            {'title': _('Address'), 'model_attr': 'address', },
        ]
    }

    class Meta:
        db_table = 'crm_customer_addresses'
        verbose_name = _('Customer Address')
        verbose_name_plural = _('Customer Addresses')

    def __str__(self):
        return '%s - %s' % (self.customer, self.address_type)

    @property
    def to_report(self):
        return [
            self.customer.id, self.customer.names, self.customer.last_names, self.id, self.address_type, self.address
        ]

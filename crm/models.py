from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Customer(models.Model):
    names = models.CharField(_('names'), max_length=100)
    last_names = models.CharField(_('last names'), max_length=100)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    notes = models.TextField(_('notes'), null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.names, self.last_names)

    class Meta:
        db_table = 'crm_customers'


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

    def __str__(self):
        return '%s - %s' % (self.customer, self.address_type)

    @property
    def to_report(self):
        return [
            self.customer.id, self.customer.names, self.customer.last_names, self.id, self.address_type, self.address
        ]

import logging
from .forms import CustomerForm, CustomerAddressForm, CustomerDocumentForm
from .models import Customer, CustomerAddress, CustomerDocument
from core.views import GenListView, NavigationHTML
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View


logger = logging.getLogger('customer_views')


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'crm/dashboard.html'


class CustomerListView(GenListView):
    model = Customer


class CustomerBaseView(LoginRequiredMixin, NavigationHTML):
    submit = 'Create'
    model = Customer
    form = CustomerForm(fields=['names', 'last_names', 'birth_date', 'notes'])
    address_forms = [CustomerAddressForm(fields=['id_address', 'address_type', 'address'])]
    blank_address_form = CustomerAddressForm(fields=['address_type', 'address'])
    document_forms = [CustomerDocumentForm(fields=['id_document', 'document_type', 'document'])]
    blank_document_form = CustomerDocumentForm(fields=['document_type', 'document'])

    def _render_object(self, request):
        context = {
            'form': self.form,
            'address_forms': self.address_forms,
            'address_blank_form': self.blank_address_form,
            'document_forms': self.document_forms,
            'document_blank_form': self.blank_document_form,
            'submit': self.submit,
            'model_meta': Customer._meta
        }
        return render(request, 'crm/customer_form.html', super().get_context_data(**context))



class CustomerCreateView(CustomerBaseView, View):

    def get(self, request, *args, **kwargs):
        return self._render_object(request)

    def post(self, request, *args, **kwargs):
        # check if customer has at least one address
        # there is a bug on request.POST if a key's value its an array it returns just the last item of the list
        # so convert the QueryDict to vanilla python dictionary
        # IMPORTANT! always return list if its just one value
        request_dict = {k: v for k, v in request.POST.lists()}
        logger.info(f'request_dict {request_dict}')
        try:
            addresses = list(zip(request_dict['address_type'], request_dict['address']))
            logger.info(f'addresses {addresses}')
        except KeyError:
            addresses = []
        try:
            documents = list(zip(request_dict['document_type'], request_dict['document']))
        except KeyError:
            documents = []
        logger.debug(f'addresses {addresses}')
        logger.debug(f'documents {documents}')

        # always return list no matter if its just one form
        # noinspection PyArgumentList
        self.form = CustomerForm(request.POST, fields=['names', 'last_names', 'birth_date', 'notes'])
        self.address_forms = []
        self.document_forms = []
        for address in addresses:
            self.address_forms.append(CustomerAddressForm(
                initial={'address_type': address[0], 'address': address[1]},
                fields=['address_type', 'address']
            ))
        for doc in documents:
            self.document_forms.append(CustomerDocumentForm(
                initial={'document_type': doc[0], 'document': doc[1]},
                fields=['document_type', 'document']
            ))
        logger.debug(f'addresses objects {self.address_forms}')
        logger.debug(f'documents objects {self.document_forms}')

        if not self.form.is_valid():
            return self._render_object(request)
        try:
            # if a child fails apply rollback to the parent and the siblings saved before
            with transaction.atomic():
                customer = self.form.save()
                for address in addresses:
                    logger.info(f'[customer] create customer saving address=>{address}')
                    CustomerAddress.objects.create(
                        customer=customer, address=address[1], address_type=address[0]
                    )
                for doc in documents:
                    logger.info(f'[customer] create customer saving document=>{doc}')
                    CustomerDocument.objects.create(
                        customer=customer, document=doc[1], document_type=doc[0]
                    )

            messages.success(request, _('customer has been created!'))
            return redirect('crm:customer-list')
        except Exception as e:
            logger.exception(e)
            messages.error(request, f'Customer can not be added due to error: {e}')
            self.form.add_error(None, f'Customer can not be added due to error: {e}')
            return self._render_object(request)



class CustomerUpdateView(CustomerBaseView, View):
    submit = 'Update'

    def get(self, request, pk, *args, **kwargs):
        logger.debug(f'[customer] manage_view GET {request.GET}')
        customer = get_object_or_404(Customer.objects.prefetch_related('addresses').all(), pk=pk)
        self.form = CustomerForm(instance=customer, fields=['names', 'last_names', 'birth_date', 'notes'])

        self.address_forms = []
        for address in customer.addresses.all():
            self.address_forms.append(CustomerAddressForm(
                initial={'id_address': address.pk, 'address_type': address.address_type, 'address': address.address},
                fields=['id_address', 'address_type', 'address'],
                auto_id=False
            ))
        self.document_forms = []
        for doc in customer.documents.all():
            self.document_forms.append(CustomerDocumentForm(
                initial={'id_document': doc.pk, 'document_type': doc.document_type, 'document': doc.document},
                fields=['id_document', 'document_type', 'document'],
                auto_id=False
            ))

        return self._render_object(request)

    def post(self, request, pk, *args, **kwargs):
        logger.debug(f'[customer] manage_view POST {request.POST}')
        # check if customer has at least one address
        # there is a bug on request.POST if a key's value its an array it returns just the last item of the list
        # so convert the QueryDict to vanilla python dictionary
        # IMPORTANT! always return list if its just one value
        request_dict = {k: v for k, v in request.POST.lists()}
        logger.info(f'request_dict {request_dict}')

        try:
            _addresses = list(zip(request_dict['id_address'], request_dict['address_type'], request_dict['address']))
            logger.info(f'addresses {_addresses}')
        except KeyError:
            _addresses = []
        try:
            _documents = list(zip(request_dict['id_document'], request_dict['document_type'], request_dict['document']))
            logger.info(f'documents {_documents}')
        except KeyError:
            _documents = []

        # check if there are new objects
        try:
            _additional_addresses = list(zip(
                request_dict['address_type'][len(_addresses):], request_dict['address'][len(_addresses):]
            ))
        except KeyError:
            _additional_addresses = []
        try:
            _additional_documents = list(zip(
                request_dict['document_type'][len(_documents):], request_dict['document'][len(_documents):]
            ))
        except KeyError:
            _additional_documents = []

        logger.debug(f'addresses {_addresses}')
        logger.debug(f'documents {_documents}')
        logger.debug(f'extra addresses {_additional_addresses}')
        logger.debug(f'extra documents {_additional_documents}')


        _customer = get_object_or_404(Customer, pk=pk)
        self.form = CustomerForm(request.POST, instance=_customer, fields=['names', 'last_names', 'birth_date', 'notes'])
        self.address_forms = []
        self.document_forms = []

        for i, address_type, address  in _addresses:
            self.address_forms.append(CustomerAddressForm(
                instance=get_object_or_404(CustomerAddress, pk=i, customer=_customer),
                data={'address_type': address_type, 'address': address},
                fields=['address_type', 'address']
            ))
        for i, document_type, document in _documents:
            self.address_forms.append(CustomerDocumentForm(
                instance=get_object_or_404(CustomerDocument, pk=i, customer=_customer),
                data={'document_type': document_type, 'document': document},
                fields=['document_type', 'document']
            ))

        logger.debug(f'addresses objects {self.address_forms}')
        logger.debug(f'documents objects {self.document_forms}')

        if not self.form.is_valid():
            # if we've reached this point its because form is not valid
            return self._render_object(request)
        try:
            # if a child fails the parent will be rollback and the siblings saved before
            with transaction.atomic():
                # SAVE USER
                self.form.save()

                # DELETE REMOVED ADDRESSES AND DOCUMENTS
                _customer.addresses.exclude(pk__in=[i[0] for i in _addresses]).delete()
                _customer.documents.exclude(pk__in=[i[0] for i in _documents]).delete()

                # UPDATE ADDRESSES AND DOCUMENTS
                for address_form in self.address_forms:
                    address_form.save()
                for document_form in self.document_forms:
                    document_form.save()

                # CREATE NEW ADDRESSES AND DOCUMENTS
                for new_address in _additional_addresses:
                    __ = CustomerAddress.objects.create(
                        customer=_customer, address_type=new_address[0], address=new_address[1]
                    )
                for new_document in _additional_documents:
                    __ = CustomerDocument.objects.create(
                        customer=_customer, document_type=new_document[0], document=new_document[1]
                    )
            messages.success(request, _('customer has been updated!'))
            return redirect('crm:customer-list')
        except Exception as e:
            messages.error(request, f'Customer can not be updated due to error: {e}')
            self.form.add_error(None, f'Customer can not be updated due to error: {e}')
            return self._render_object(request)

from crm.models import Customer, CustomerAddress, CustomerDocument
from django.contrib.auth import get_user_model

super_user_exists = get_user_model().objects.filter(is_superuser=True).exists()
print(f'super user already exists? {super_user_exists}')
if not super_user_exists:
    print(f'creating superuser WEBAPP')
    get_user_model().objects.create_superuser('webapp', 'jgomez@jesrat.com', '1234')
    print(f'superuser WEBAPP created pass is 1234, we strongly advice to change password on first login')

if not Customer.objects.all().count():
    data = [
        {
            'names': 'Josue',
            'last_names': 'Gomez',
            'address_type': CustomerAddress.AddressType.home,
            'address': 'Ciudad Franc',
            'document_type': CustomerDocument.DocType.dui,
            'document': '00000000-0'
        },
        {
            'names': 'Francisco',
            'last_names': 'Gomez',
            'address_type': CustomerAddress.AddressType.work,
            'address': '88 y 85 Av',
            'document_type': CustomerDocument.DocType.nit,
            'document': '0000-000000-000-0'
        }
    ]
    for i in data:
        customer = Customer.objects.create(names=i['names'], last_names=i['last_names'])
        _ = CustomerAddress.objects.create(customer=customer,address_type=i['address_type'],address=i['address'])
        _ = CustomerDocument.objects.create(customer=customer,document_type=i['document_type'],document=i['document'])


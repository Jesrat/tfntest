import argparse
import csv
import os
import sys


# To use this script make sure you have set the environment variable for the settings module
# export DJANGO_SETTINGS_MODULE=tfntest.settings

parser = argparse.ArgumentParser(prog='Report')
parser.add_argument(
    '--out-file',
    dest='out_file',
    default='report.csv',
    help='file to output result'
)
parser.add_argument(
    '--extract',
    dest='extract',
    choices=['documents', 'addresses'],
    help='information to extract'
)
args = parser.parse_args(sys.argv[1:])

def main():
    from crm.models import Customer

    with open(args.out_file, 'w', encoding='UTF8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['userid', "names", "last_names", "id", "type", "value"])
        for customer in Customer.objects.all():
            if args.extract == 'documents':
                for doc in customer.documents.all():
                    writer.writerow(doc.to_report)
            elif args.extract == 'addresses':
                for address in customer.addresses.all():
                    writer.writerow(address.to_report)



if __name__ == '__main__':
    if not os.environ.get('DJANGO_SETTINGS_MODULE'):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tfntest.settings")
    import django
    django.setup()
    main()

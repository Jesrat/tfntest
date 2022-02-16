from django.contrib.auth.models import User

super_user_exists = User.objects.filter(is_superuser=True).exists()
print(f'super user already exists? {super_user_exists}')
if not super_user_exists:
    User.objects.create_superuser('webapp', 'jgomez@jesrat.com', '1234')

import os
from django.core.files.storage import FileSystemStorage
from .settings import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/assets/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


class OverrideFileCustomOSStorage(FileSystemStorage):
    # This method is actually defined in Storage
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(MEDIA_ROOT, name))
        return name

    def path(self, *name):
        return os.path.abspath(os.path.join(MEDIA_ROOT, *name))

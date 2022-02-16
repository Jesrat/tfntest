from django.views.generic import TemplateView

# Create your views here.

class Dummy(TemplateView):
    template_name = 'crm/dummy.html'

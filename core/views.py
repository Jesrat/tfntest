from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.base import ContextMixin


class GenLoginView(auth_views.LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True


class GenLogoutView(auth_views.LogoutView):
    next_page = 'login'


class NavigationHTML(ContextMixin):
    nav_group_item = None
    nav_group_name = None

    # noinspection PyProtectedMember,PyUnresolvedReferences
    def get_context_data(self, **kwargs):
        if hasattr(self, 'model'):
            kwargs['model'] = self.model
            kwargs['model_meta'] = self.model._meta
            kwargs['nav_group_item'] = self.model._meta.object_name
            kwargs['nav_group_name'] = self.model._meta.app_label
        else:
            kwargs['nav_group_item'] = self.nav_group_item
            kwargs['nav_group_name'] = self.nav_group_name
        return super().get_context_data(**kwargs)


# noinspection PyProtectedMember
class GenListView(NavigationHTML, LoginRequiredMixin, ListView):
    paginate_by = None
    template_name = 'crm/objects_list.html'
    title = '%(verbose_name_plural)s'
    filters = []
    allow_empty = True

    def get_filters_from_request(self):
        # search filters in url if filters do exists change key append __in
        return {f'{k}__in': self.request.GET.getlist(k)
                for k in self.filters if self.request.GET.getlist(k, ['']) != ['']}

    # noinspection PyUnresolvedReferences
    def get_queryset(self):
        filters = self.get_filters_from_request()
        queryset = super().get_queryset()
        if filters:
            queryset = queryset.filter(**filters)
        return queryset

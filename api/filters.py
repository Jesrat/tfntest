from rest_framework.filters import BaseFilterBackend

class CustomerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(customer=view.kwargs['customer'])

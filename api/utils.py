from django.db.models import Q

from .models import Proposition


def propositions_filter(self):
    query = self.request.GET.get('query')
    try:
        query_int = int(query)
    except ValueError:
        query_int = -1

    if query:
        queryset = Proposition.objects.filter(
            Q(abstract__contains=query) |
            Q(number__contains=query) |
            Q(proposition_type__contains=query) |
            Q(proposition_type_initials__contains=query) |
            Q(year=query_int)
        )

    return queryset

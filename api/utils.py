from django.db.models import Q


def get_query(self):
    query = self.request.GET.get('query')
    try:
        query_int = int(query)
    except (ValueError, TypeError):
        query_int = -1

    return (query, query_int)


def propositions_filter(self, queryset):
    (query, query_int) = get_query(self)

    if query:
        queryset = queryset.filter(
            Q(abstract__contains=query) |
            Q(number__contains=query) |
            Q(proposition_type__contains=query) |
            Q(proposition_type_initials__contains=query) |
            Q(year=query_int)
        )

    return queryset


def user_votes_filter(self, queryset):
    (query, query_int) = get_query(self)

    if query:
        queryset = queryset.filter(
            Q(proposition__abstract__contains=query) |
            Q(proposition__number__contains=query) |
            Q(proposition__proposition_type__contains=query) |
            Q(proposition__proposition_type_initials__contains=query) |
            Q(proposition__year=query_int)
        )

    return queryset


def parliamentarians_filter(self, queryset):
    query = self.request.GET.get('query')

    if query:
        queryset = queryset.filter(
            Q(name__contains=query) |
            Q(political_party__contains=query) |
            Q(federal_unit__contains=query)
        )

    return queryset


def user_following_filter(self, queryset):
    query = self.request.GET.get('query')

    if query:
        queryset = queryset.filter(
            Q(parliamentary__name__contains=query) |
            Q(parliamentary__political_party__contains=query) |
            Q(parliamentary__federal_unit__contains=query)
        )

    return queryset

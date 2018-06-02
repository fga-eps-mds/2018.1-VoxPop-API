from api.models import Compatibility, Parliamentary

from django.db.models import Count, F, Q


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


def update_compatibility(self):

    all_parliamentarians_ids = Parliamentary.objects.all().values_list(
        'id',
        flat=True
    )

    valid_votes_queryset = self.request.user.votes.filter(
        Q(proposition__parliamentary_votes__option='Y') |
        Q(proposition__parliamentary_votes__option='N')
    ).annotate(
        parliamentary=F('proposition__parliamentary_votes__parliamentary')
    ).values(
        'parliamentary'
    ).annotate(
        valid_votes=Count('parliamentary')
    ).order_by(
        'parliamentary'
    )

    valid_votes = list()
    valid_votes_parliamentarians_ids = list()
    for valid_vote in valid_votes_queryset:
        valid_votes.append(valid_vote)
        valid_votes_parliamentarians_ids.append(valid_vote['parliamentary'])

    for parliamentary_id in all_parliamentarians_ids:
        if parliamentary_id not in valid_votes_parliamentarians_ids:
            valid_votes.append({
                'parliamentary': parliamentary_id,
                'valid_votes': 0
            })

    valid_votes = sorted(valid_votes, key=lambda k: k['parliamentary'])

    matching_votes_queryset = self.request.user.votes.filter(
        (
            Q(proposition__parliamentary_votes__option='Y') |
            Q(proposition__parliamentary_votes__option='N')
        ),
        Q(proposition__parliamentary_votes__option=F('option'))
    ).annotate(
        parliamentary=F('proposition__parliamentary_votes__parliamentary')
    ).values(
        'parliamentary'
    ).annotate(
        matching_votes=Count('parliamentary')
    ).order_by(
        'parliamentary'
    )

    matching_votes = list()
    matching_votes_parliamentarians_ids = list()
    for valid_vote in matching_votes_queryset:
        matching_votes.append(valid_vote)
        matching_votes_parliamentarians_ids.append(valid_vote['parliamentary'])

    for parliamentary_id in all_parliamentarians_ids:
        if parliamentary_id not in matching_votes_parliamentarians_ids:
            matching_votes.append({
                'parliamentary': parliamentary_id,
                'matching_votes': 0
            })

    matching_votes = sorted(matching_votes, key=lambda k: k['parliamentary'])

    if len(valid_votes) == len(matching_votes):

        compatibilities = list()

        for i in range(len(valid_votes)):

            if valid_votes[i]['parliamentary'] == \
                    matching_votes[i]['parliamentary']:

                compatibility = dict()

                parliamentary = Parliamentary.objects.get(
                    pk=valid_votes[i]['parliamentary']
                )

                compatibility['user'] = self.request.user
                compatibility['parliamentary'] = parliamentary
                compatibility['valid_votes'] = valid_votes[i]['valid_votes']
                compatibility['matching_votes'] = \
                    matching_votes[i]['matching_votes']
                # compatibility['compatibility'] = \
                #     ((compatibility['matching_votes'] /
                #       self.request.user.votes.count()) * 100)
                try:
                    compatibility['compatibility'] = (
                        compatibility['matching_votes'] * (
                            self.request.user.votes.count() +
                            compatibility['valid_votes']
                        ) / (
                            compatibility['valid_votes'] *
                            self.request.user.votes.count() * 2
                        )
                    ) * 100
                except ZeroDivisionError:
                    compatibility['compatibility'] = 0

                compatibility_obj = Compatibility(**compatibility)
                compatibilities.append(compatibility_obj)

        self.request.user.compatibilities.all().delete()

        Compatibility.objects.bulk_create(compatibilities)

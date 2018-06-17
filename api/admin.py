from .models import (
    ExtendedUser, Parliamentary, ParliamentaryVote, Proposition,
    SocialInformation, UserFollowing, UserVote, ContactUs
)
from django.contrib import admin


class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'should_update'
    ]


class ParliamentaryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'gender',
        'political_party',
        'federal_unit',
        'birth_date',
        'education',
        'email'
    ]


class ParliamentaryVoteAdmin(admin.ModelAdmin):
    list_display = [
        'option',
        'proposition',
        'parliamentary'
    ]


class PropositionAdmin(admin.ModelAdmin):
    list_display = [
        'proposition_type',
        'proposition_type_initials',
        'number',
        'year',
        'abstract',
        'processing',
        'situation',
        'last_update'
    ]


class SocialInformationAdmin(admin.ModelAdmin):
    list_display = [
        'owner',
        'region',
        'income',
        'education',
        'race',
        'gender',
        'birth_date',
    ]


class UserFollowingAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'parliamentary'
    ]


class UserVoteAdmin(admin.ModelAdmin):
    list_display = [
        'option',
        'proposition',
        'user'
    ]


class ContactUsAdmin(admin.ModelAdmin):
    list_display = [
        'topic',
        'email',
        'choice',
        'text'
    ]


admin.site.register(ExtendedUser, ExtendedUserAdmin)
admin.site.register(Parliamentary, ParliamentaryAdmin)
admin.site.register(ParliamentaryVote, ParliamentaryVoteAdmin)
admin.site.register(Proposition, PropositionAdmin)
admin.site.register(SocialInformation, SocialInformationAdmin)
admin.site.register(UserFollowing, UserFollowingAdmin)
admin.site.register(UserVote, UserVoteAdmin)
admin.site.register(ContactUs, ContactUsAdmin)

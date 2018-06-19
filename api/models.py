import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
REGION_CHOICES = (
    (None, 'Null'),
    ('N', 'Norte'),
    ('NE', 'Nordeste'),
    ('CO', 'Centro-Oeste'),
    ('SE', 'Sudeste'),
    ('S', 'Sul')
)

INCOME_CHOICES = (
    (None, 'Null'),
    ('E', '0.00-1874.00'),
    ('D', '1874.01-3748.00'),
    ('C', '3748.01-9370.00'),
    ('B', '9370.01-18740.00'),
    ('A', '18740.01+')
)

EDUCATION_CHOICES = (
    (None, 'Null'),
    ('SE', 'Sem Escolaridade'),
    ('EF', 'Ensino Fundamental'),
    ('EM', 'Ensino Médio'),
    ('ES', 'Ensino Superior'),
    ('PG', 'Pós-Graduação')
)

RACE_CHOICES = (
    (None, 'Null'),
    ('B', 'Branca'),
    ('PR', 'Preta'),
    ('A', 'Amarela'),
    ('PA', 'Parda'),
    ('I', 'Indígena')
)

GENDER_CHOICES = (
    (None, 'Null'),
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outros')
)

VOTE_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No'),
    ('A', 'Abstention'),
    ('O', 'Obstruction'),
    ('M', 'Missing'),
)

CONTACT_CHOICES = (
    ('A', 'Dúvida'),
    ('B', 'Sugestão'),
    ('C', 'Reclamação'),
    ('D', 'Outro'),
)


class SocialInformation(models.Model):

    owner = models.OneToOneField(
        User,
        related_name='social_information',
        on_delete=models.CASCADE
    )
    region = models.CharField(
        max_length=10,
        choices=REGION_CHOICES,
        default=None,
        null=True
    )
    income = models.CharField(
        max_length=20,
        choices=INCOME_CHOICES,
        default=None,
        null=True
    )
    education = models.CharField(
        max_length=10,
        choices=EDUCATION_CHOICES,
        default=None,
        null=True
    )
    race = models.CharField(
        max_length=10,
        choices=RACE_CHOICES,
        default=None,
        null=True
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default=None,
        null=True
    )
    birth_date = models.DateField(
        default=None,
        null=True
    )

    def __str__(self):
        return '{owner}'.format(owner=self.owner)

    class Meta:
        verbose_name = "Social Information"
        verbose_name_plural = "Social Informations"


class Parliamentary(models.Model):

    # parliamentary_id  is getted from camara's API parliamentary ID
    parliamentary_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    gender = \
        models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    political_party = models.CharField(max_length=100, blank=True)
    federal_unit = models.CharField(max_length=100, blank=True)
    birth_date = models.CharField(max_length=15, blank=True)
    education = models.CharField(max_length=150, default='N')
    email = models.CharField(max_length=100, blank=True)
    photo = models.URLField(blank=True)

    def __str__(self):
        return '{name}'.format(name=self.name)

    class Meta:
        verbose_name = "Parliamentary"
        verbose_name_plural = "Parliamentarians"


class Proposition(models.Model):

    native_id = models.CharField(max_length=100, unique=True)
    proposition_type = models.CharField(max_length=100, blank=True)
    proposition_type_initials = models.CharField(max_length=20, blank=True)
    number = models.IntegerField(blank=True)
    year = models.IntegerField(blank=True)
    abstract = models.TextField(max_length=2000, blank=True)
    processing = models.CharField(max_length=100, blank=True)
    situation = models.CharField(max_length=100, blank=True)
    url_full = models.URLField(blank=True)
    last_update = models.DateTimeField(blank=True)

    def __str__(self):
        return 'Proposition {native_id}'.format(
            native_id=self.native_id
        )

    class Meta:
        verbose_name = "Proposition"
        verbose_name_plural = "Propositions"


class UserVote(models.Model):

    option = models.CharField(
        max_length=1,
        choices=VOTE_CHOICES,
        blank=True
    )
    proposition = models.ForeignKey(
        Proposition,
        on_delete=models.DO_NOTHING,
        related_name='user_votes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='votes'
    )

    class Meta:
        unique_together = ('proposition', 'user')
        verbose_name = "User Vote"
        verbose_name_plural = "User Votes"


class ParliamentaryVote(models.Model):

    option = models.CharField(
        max_length=1,
        choices=VOTE_CHOICES,
        blank=True
    )
    proposition = models.ForeignKey(
        Proposition,
        on_delete=models.DO_NOTHING,
        related_name='parliamentary_votes'
    )
    parliamentary = models.ForeignKey(
        Parliamentary,
        on_delete=models.DO_NOTHING,
        related_name='votes'
    )

    class Meta:
        unique_together = ('proposition', 'parliamentary')
        verbose_name = "Parliamentary Vote"
        verbose_name_plural = "Parliamentary Votes"


class UserFollowing(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='following'
    )
    parliamentary = models.ForeignKey(
        Parliamentary,
        on_delete=models.DO_NOTHING,
        related_name='followers'
    )

    class Meta:
        verbose_name = "User Following"
        verbose_name_plural = "User Following"


class Compatibility(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='compatibilities'
    )
    parliamentary = models.ForeignKey(
        Parliamentary,
        on_delete=models.DO_NOTHING,
        related_name='user_compatibilities'
    )
    valid_votes = models.IntegerField(blank=True)
    matching_votes = models.IntegerField(blank=True)
    compatibility = models.FloatField(blank=True)

    class Meta:
        verbose_name = "Compatibility"
        verbose_name_plural = "Compatibilities"


class ExtendedUser(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        related_name='extended_user'
    )
    should_update = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Extended User"
        verbose_name_plural = "Extended Users"


class ContactUs(models.Model):
    topic = models.CharField(max_length=150)
    email = models.EmailField(max_length=250, blank=True)
    choice = models.CharField(
        max_length=1,
        choices=CONTACT_CHOICES,
        default='A'
    )
    text = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

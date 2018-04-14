import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
UF_CHOICES = (
    ('N', 'Null'),
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranão'),
    ('MG', 'Minas Gerais'),
    ('MS', 'Mato Grosso do Sul'),
    ('MT', 'Mato Grosso'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PE', 'Pernanbuco'),
    ('PI', 'Piauí'),
    ('PR', 'Paraná'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('RS', 'Rio Grande do Sul'),
    ('SC', 'Santa Catarina'),
    ('SE', 'Sergipe'),
    ('SP', 'São Paulo'),
    ('TO', 'Tocantins')
)

EDUCATION_CHOICES = (
    ('N', 'Null'),
    ('EFC', 'Ensino Fundamental Completo'),
    ('EFI', 'Ensino Fundamental Incompleto'),
    ('EMC', 'Ensino Médio Completo'),
    ('EMI', 'Ensino Médio Incompleto'),
    ('ESC', 'Ensino Superior Completo'),
    ('ESI', 'Ensino Superior Incompleto'),
    ('PG', 'Pós-Graduação'),
    ('ME', 'Mestrado'),
    ('DO', 'Doutorado'),
    ('PD', 'Pós-Doutorado')
)

VOTE_CHOICES = (
    ('SIM', 'Sim'),
    ('NAO', 'Não'),
    ('ABSTENCAO', 'Abstenção'),
    ('OBSTRUCAO', 'Obstrução'),
    ('AUSENTE', 'Ausente'),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class SocialInformation(models.Model):

    owner = models.OneToOneField(
        User,
        related_name='social_information',
        on_delete=models.CASCADE
    )
    federal_unit = models.CharField(max_length=150, choices=UF_CHOICES, default='N')
    city = models.CharField(max_length=150, blank=True)
    income = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    education = models.CharField(
        max_length=150, choices=EDUCATION_CHOICES, default='N'
    )
    job = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(default=datetime.date.today)


class Parliamentary(models.Model):

    # parliamentary_id  is getted from camara's API parliamentary ID
    parliamentary_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    gender = \
        models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    federal_unit = models.CharField(max_length=100, blank=True)
    photo = models.URLField(blank=True)

    def __str__(self):
        return '{name}'.format(name=self.name)

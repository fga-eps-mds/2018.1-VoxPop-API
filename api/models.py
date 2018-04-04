from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
UF_CHOICES = (
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

class Users(User):
    username_validator = UnicodeUsernameValidator()
    email_validator = EmailValidator()
    username_field = models.CharField(
        max_length = 50,
        validators = [username_validator],
    )
    email_field = models.EmailField(
        max_length = 150,
        validators = [email_validator],
    )
    state = models.CharField(max_length=20, choices=UF_CHOICES, default='AC')
    city = models.CharField(max_length=150, blank=True)
    USERNAME_FIELD = 'username_field'
    EMAIL_FIELD = 'email_field'

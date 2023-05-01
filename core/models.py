from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Criando o usuários diferentões
from django.db import models

# from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UsuarioManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)


class CustomUsuario(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    telefone = models.CharField('Telefone', max_length=15)
    is_staff = models.BooleanField('Membro da equipe', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telefone']

    def __str__(self):
        return self.email

    objects = UsuarioManager()

# 3ª Forma
class Postagem(models.Model):
    autor = models.ForeignKey(
        get_user_model(), verbose_name='Autor', on_delete=models.CASCADE
        )
    titulo = models.CharField('Título', max_length=100)
    texto = models.TextField('Texto', max_length=500)

    def __str__(self):
        return self.titulo


# Create your models here.

"""
# Modificando o User que vem no Django
    1ª Forma
from django.contrib.auth.models import User
class Postagem(models.Model):
    autor = models.ForeignKey(
        User, verbose_name='Autor', on_delete=models.CASCADE
        )
    titulo = models.CharField('Título', max_length=100)
    texto = models.TextField('Texto', max_length=500)
    def __str__(self):
        return self.titulo
"""

"""
2ª Forma
from django.conf import settings
class Post(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name='Autor', 
        on_delete=models.CASCADE
        )
    titulo = models.CharField('Título', max_length=100)
    texto = models.TextField('Texto', max_length=500)
    def __str__(self):
        return self.titulo
"""


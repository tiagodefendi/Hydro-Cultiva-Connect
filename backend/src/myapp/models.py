from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # O campo email deve ser único
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'  # Define o campo de login como email


from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_staff = models.BooleanField(default=False)  

from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()


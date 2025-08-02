
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_staff = models.BooleanField(default=False)  # Used to distinguish staff vs normal user

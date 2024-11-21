from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserExtended(models.Model):
    base_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='extended_user')

    def __str__(self):
        return f'{self.base_user.first_name} ({self.base_user.username})'


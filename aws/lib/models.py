from django.db import models

# Create your models here.
class UserAccount(models.Model):
    username = models.CharField(max_length=255)
    temp_password_set = models.BooleanField(default=False)

from django.db import models

# Create your models here.
# class UserAccount(models.Model):
#     username = models.CharField(max_length=255)
#     temp_password_set = models.BooleanField(default=False)


class AWSCommandResponse(models.Model):
    command = models.TextField()
    response = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

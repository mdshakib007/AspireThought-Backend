from django.contrib.auth.models import AbstractUser
from django.db import models 


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.username}"
    
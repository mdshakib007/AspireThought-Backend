from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField  

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    bookmarks = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.username}"

    def add_bookmark(self, slug):
        if slug not in self.bookmarks:
            self.bookmarks.append(slug)
            self.save()

    def remove_bookmark(self, slug):
        if slug in self.bookmarks:
            self.bookmarks.remove(slug)
            self.save()

    def get_bookmarks(self):
        return self.bookmarks

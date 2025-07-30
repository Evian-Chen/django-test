from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords
    display_name = models.CharField(max_length=100, blank=True, null=True)
    profile_picture_url = models.URLField(null=True, blank=True)

    # is_active, is_staff, date_joined (AbstractUser 內建)

    def __str__(self):
        return self.username
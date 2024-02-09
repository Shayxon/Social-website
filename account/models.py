from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    photo = models.ImageField(upload_to='profile/%Y/%m/%d/', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
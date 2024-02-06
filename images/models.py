from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.files.base import ContentFile
import requests

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_images', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def save(self, force_insert = False, force_update = False, commit = True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(self.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f"{name}.{extension}"
        response = requests.get(image_url)

        image.image.save(image_name, ContentFile(response.content), save=False)

        if commit:
            image.save()
        return image        
        

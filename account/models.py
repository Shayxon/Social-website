from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset() \
                                .filter(status=Post.Status.PUBLISHED)
    

class Profile(models.Model):
    photo = models.ImageField(upload_to='profile/%Y/%m/%d/', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)

class Post(models.Model):

    class Status(models.TextChoices):
        PUBLISHED = 'PB', 'Published'
        DRAFT = 'DR', 'Draft'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=250, blank=False)
    image = models.ImageField(upload_to='post_image/%Y/%m/%d/', blank=False)
    body = CKEditor5Field(blank=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self) -> str:
        return f"{self.title} published by {self.author.username}"    
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset() \
                                .filter(status=Post.Status.PUBLISHED)
    

class Profile(models.Model):
    photo = models.ImageField(upload_to='profile/%Y/%m/%d/', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='comment_likes')

    def save(self, *args, **kwargs):
        if not self.id:  # Only set the creation time if the object is being created for the first time
            timezone.activate('Asia/Tashkent')
            self.created = timezone.now()
        super().save(*args, **kwargs)


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
    likes = models.ManyToManyField(User, related_name='likes')
    comments = models.ManyToManyField(Comment, related_name='comments')
    tags = TaggableManager()
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
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="commenter")
    resource = models.ForeignKey("Resource", on_delete=models.CASCADE, related_name="resource")
    comment = models.CharField(max_length=255)


class Language(models.Model):
    LANGUAGE_CHOICES = [
        ("CSS", "CSS"),
        ("HTML", "HTML"),
        ("JS", "JavaScript"),
        ("PY", "Python")
    ]
    language = models.CharField(max_length=4, unique=True, choices=LANGUAGE_CHOICES)

    def __str__(self):
        return self.language


class Resource(models.Model):
    CATEGORY_CHOICES = [
        ("LEARN", "Learn"),
        ("PRACT", "Practice")
    ]
    LEVEL_CHOICES = [
        ("INTR", "Introductory"),
        ("MEDI", "Intermediate"),
        ("ADVC", "Advanced")
    ]
    title = models.CharField(max_length=150)
    description = models.TextField()
    url = models.URLField(max_length=255)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("User", on_delete=models.SET_NULL, related_name="added_by", null=True)
    like = models.ManyToManyField("User", related_name="liker", blank=True)
    favorite = models.ManyToManyField("User", related_name="favoriter", blank=True)
    language = models.ManyToManyField("Language", related_name="lang")
    level = models.CharField(max_length=4, choices=LEVEL_CHOICES)

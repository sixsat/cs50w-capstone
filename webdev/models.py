import requests

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="commenter")
    resource = models.ForeignKey("Resource", on_delete=models.CASCADE, related_name="resource")
    comment = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} {self.user} commented \"{self.comment}\" on Resource_obj ({self.resource.pk})"

    def ftime(self):
        return self.timestamp.strftime("%b %d, %Y, %I:%M %p")


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
        ("BOOK", "Book"),
        ("CODE", "Code"),
        ("CRS", "Course"),
        ("DOC", "Document"),
        ("QUIZ", "Quiz"),
        ("VID", "Video")
    ]
    LEVEL_CHOICES = [
        ("INTR", "Introductory"),
        ("MEDI", "Intermediate"),
        ("ADVC", "Advanced")
    ]
    title = models.CharField(max_length=150)
    description = models.TextField()
    url = models.URLField(max_length=255)
    embeddable = models.BooleanField()
    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("User", on_delete=models.SET_NULL, related_name="added_by", null=True)
    like = models.ManyToManyField("User", related_name="liker", blank=True)
    favorite = models.ManyToManyField("User", related_name="favoriter", blank=True)
    language = models.ManyToManyField("Language", related_name="lang")
    level = models.CharField(max_length=4, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.timestamp} {self.user} added ({self.pk}) {self.title}"

    def save(self, *args, **kwargs):

        # Check if URL is embeddable and assign result to embeddable field
        self.embeddable = not requests.get(self.url).headers.get("X-Frame-Options")

        super().save(*args, **kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "timestamp": self.timestamp.strftime("%b %d, %Y, %I:%M %p"),
            "language": ", ".join([lang.language for lang in self.language.all()]),
            "level": self.level
        }

from django.contrib.auth.models import AbstractUser
from django.db import models

from recipes.constants import CATEGORY_CHOICES, DESCRIPTION_TEMPLATE, NO_PHOTO_PATH


class User(AbstractUser):
    pass


class Recipe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="owner_user")
    category = models.CharField(choices=CATEGORY_CHOICES, blank=False, max_length=64)
    title = models.CharField(blank=False, max_length=64)
    description = models.TextField(default=DESCRIPTION_TEMPLATE, blank=False, max_length=420)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='recipes/images/uploaded', default=NO_PHOTO_PATH)
    favorite = models.BooleanField(default=False, blank=False)


    def serialize(self):
        return {
             "owner": self.user.username,
             "category": self.category,
             "title": self.title,
             "description": self.description,
             "created": self.created.strftime("%b %d %Y, %I:%M %p"),
             "image": self.image.url
        }

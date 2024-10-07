from django.contrib import admin
from recipes.models import User, Recipe


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "category", "title", "description", "favorite", "image", "created")


admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("show_recipes/<str:category>", views.show_recipes, name="show"),
    path("recipes_edit/<int:id>", views.edit, name="edit"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API routs
    path('allrecipes', views.allrecipes, name='recipes'),
]

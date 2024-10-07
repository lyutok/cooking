from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from django.contrib import messages
import json
from recipes.models import User, Recipe
from recipes.constants import CATEGORY_CHOICES, DESCRIPTION_TEMPLATE, NO_PHOTO_PATH


class AddForm(forms.Form):
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    title = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'style': 'width: 100%;',
                                      'class': 'form-control', 'placeholder': 'Recipe name'})
    )

    description = forms.CharField(
    max_length=420,
    widget=forms.Textarea(attrs={'style': 'width: 100%;', 'class': 'form-control'}),
    )

    image = forms.ImageField(
        widget=forms.ClearableFileInput(), required=False
    )

    def __init__(self, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)
        self.fields['description'].initial = DESCRIPTION_TEMPLATE


# for edit view
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['category', 'title', 'description', 'image', 'favorite']
    # Adding Bootstrap classes to the fields
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})


def index(request):
    # form = AddForm()
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = Recipe(
                owner = request.user,
                category = request.POST.get("category"),
                title = request.POST.get("title").strip().capitalize(),
                description = request.POST.get("description"),
                image = request.FILES.get("image") if request.FILES.get("image") else NO_PHOTO_PATH
                )
            recipe.save()
            # form = AddForm()
            message = 'Recipe saved successfully!'
            messages.add_message(request, messages.INFO, message)
            print(request.POST.get("category"))
            return redirect(f'/show_recipes/{request.POST.get("category")}')
        else:
            print(form.errors)
    else:
        form = AddForm()

    return render (request, 'recipes/index.html', {'form': form})


# Edit recipe
def edit(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            message = 'Recipe updated!'
            messages.add_message(request, messages.INFO, message)
            # print(recipe.category)
            return redirect(f'/show_recipes/{recipe.category}')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit.html', {'form': form})


def show_recipes(request, category):
    title = category.capitalize()

    if category == 'breakfast':
        title_message = 'These recipes offer a variety of flavors and nutrition to help you start your day right!'
    elif category == 'main':
        title_message = 'These main course recipes offer a wide range of flavors and cuisines, perfect for a variety of tastes and occasions!'
    elif category == 'dessert':
        title_message = 'These desserts offer a variety of flavors and textures, perfect for satisfying any sweet tooth!'
    else:
        title = ''
        title_message = 'Category not found.'

    return render(request, 'recipes/show_recipes.html', {'title': title, 'title_message': title_message})


# Server
def allrecipes(request):
    filter_id = request.GET.get('id')

    # update like in db
    if request.method == "PUT":
        favorite_status = json.loads(request.body).get('favorite')
        Recipe.objects.filter(id=filter_id).update(favorite=favorite_status)

    if filter_id:
        recipes = Recipe.objects.filter(id=filter_id).values('id', 'owner__username', 'category', 'title', 'description', 'favorite', 'image', 'created')
    else:
        recipes = Recipe.objects.all().order_by("-favorite", "-created").values('id', 'owner__username', 'category', 'title', 'description', 'favorite', 'image', 'created')

    return JsonResponse(list(recipes), safe=False)


# Login, Logout, register
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "recipes/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "recipes/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# registering
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "recipes/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "recipes/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "recipes/register.html")

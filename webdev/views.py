import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Resource, User


def index(request):
    return render(request, "webdev/index.html")


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
            return render(request, "webdev/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "webdev/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "webdev/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "webdev/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "webdev/register.html")


def resource(request, content_type):

    # Ensure valid content type
    if content_type not in ["BOOK", "CODE", "CRS", "DOC", "FAV", "PUB", "QUIZ", "VID"]:
        return JsonResponse({"error": "Invalid content type"}, status=400)

    if content_type == "FAV":
        resources = Resource.objects.filter(favorite__contains=request.user)
    elif content_type == "PUB":
        resources = Resource.objects.filter(user=request.user)
    else:
        resources = Resource.objects.filter(category=content_type)

    resources = resources.order_by("-timestamp")
    return JsonResponse([resource.serialize() for resource in resources], safe=False)


def resource_view(request, resource_id):
    return render(request, "TODO")

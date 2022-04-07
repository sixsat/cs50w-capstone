import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.defaulttags import register
from django.urls import reverse

from .models import Comment, Resource, User

CATEGORY = {
    "book": {
        "cap": "BOOK",
        "view": "learn"
    },
    "code": {
        "cap": "CODE",
        "view": "practice"
    },
    "course": {
        "cap": "CRS",
        "view": "learn"
    },
    "document": {
        "cap": "DOC",
        "view": "learn"
    },
    "favorite": {
        "cap": "FAV",
        "view": "user"
    },
    "published": {
        "cap": "PUB",
        "view": "user"
    },
    "quiz": {
        "cap": "QUIZ",
        "view": "practice"
    },
    "video": {
        "cap": "VID",
        "view": "learn"
    }
}

LEVEL = {
    "INTR": {
        "full": 'Introductory',
        "color": 'text-success'
    },
    "MEDI": {
        "full": 'Intermediate',
        "color": 'text-warning'
    },
    "ADVC": {
        "full": 'Advanced',
        "color": 'text-danger'
    }
}


def index(request):
    return render(request, "webdev/index.html")


@login_required
def comment(request, resource_id):

    # Add a comment must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Attempt to create new comment
    comment = json.loads(request.body)["comment"]
    try:
        comment_obj = Comment(
            user=request.user,
            resource=Resource.objects.get(pk=resource_id),
            comment=comment
        )
        comment_obj.save()
    except Exception as e:
        raise e

    return JsonResponse({
        "message": "Comment added.",
        "username": request.user.username,
        "timestamp": Comment.objects.get(pk=comment_obj.pk).ftime()
    }, status=201)


def content(request, content_type):

    # Ensure valid content type
    if content_type not in CATEGORY.keys():
        return render(request, "webdev/content.html", {
            "message": "Invalid content type."
        }, status=404)

    # To view 'favorite' and 'published', user must logged in
    if not request.user.is_authenticated and content_type in ["favorite", "published"]:
        return render(request, "webdev/content.html", {
            "message": "Login required."
        }, status=401)

    if content_type == "favorite":
        resources = Resource.objects.filter(favorite__pk=request.user.pk)
    elif content_type == "published":
        resources = Resource.objects.filter(user=request.user)
    else:
        resources = Resource.objects.filter(category=CATEGORY[content_type]["cap"])

    # Return resources in reverse chronologial order
    resources = resources.order_by("-timestamp")
    return render(request, "webdev/content.html", {
        "level": LEVEL,
        "resources": resources,
        "category": CATEGORY[content_type]
    })


def get_content(request, content_type):
    if content_type not in CATEGORY.keys():
        return JsonResponse({"error": "Invalid content type."}, status=404)

    if not request.user.is_authenticated and content_type in ["favorite", "published"]:
        return JsonResponse({"error": "Login required."}, status=401)

    if content_type == "favorite":
        resources = Resource.objects.filter(favorite__pk=request.user.pk)
    elif content_type == "published":
        resources = Resource.objects.filter(user=request.user)
    else:
        resources = Resource.objects.filter(category=CATEGORY[content_type]["cap"])

    resources = resources.order_by("-timestamp")
    return JsonResponse([resource.serialize() for resource in resources], safe=False)


@register.filter
def get_item(dictionary, key):
    """Custom template filter to lookup dict with a variable"""
    return dictionary.get(key)


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


def resource(request, resource_id):

    # Query for requested resource
    try:
        resource = Resource.objects.get(pk=resource_id)
        comments = Comment.objects.filter(resource=resource_id).order_by("timestamp")
    except Resource.DoesNotExist:
        return render(request, "webdev/resource.html", {
            "message": "Resource not found."
        }, status=404)

    context = {
        "resource": resource,
        "comments": comments
    }

    if request.user.is_authenticated:
        context["liked"] = resource.like.filter(pk=request.user.pk).exists()
        context["faved"] = resource.favorite.filter(pk=request.user.pk).exists()

    return render(request, "webdev/resource.html", context)


@login_required
def update(request, resource_id):
    """Update resource's like or favorite field"""

    # Update must be via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return JsonResponse({"error": "Resource not found."}, status=404)

    # Attempt to like/unlike or fave/unfave resource
    action = json.loads(request.body)["action"]
    try:
        if action == "like":
            icon = "fa-heart"
            if resource.like.filter(pk=request.user.pk).exists():
                resource.like.remove(request.user)
            else:
                resource.like.add(request.user)
            count = resource.like.all().count()
        elif action == "fave":
            icon = "fa-star"
            if resource.favorite.filter(pk=request.user.pk).exists():
                resource.favorite.remove(request.user)
            else:
                resource.favorite.add(request.user)
            count = resource.favorite.all().count()
        else:
            return JsonResponse({"error": "Invalid action."}, status=400)
    except Exception as e:
        raise e

    return JsonResponse({"icon": icon, "count": count}, status=200)

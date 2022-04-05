from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:content_type>", views.content, name="content"),
    path("resource/<int:resource_id>", views.resource, name="resource"),

    # API Routes
    path("getcontent/<str:content_type>", views.get_content, name="get_content"),
    path("resource/<int:resource_id>/comment", views.comment, name="comment"),
]

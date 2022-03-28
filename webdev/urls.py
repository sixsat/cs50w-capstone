from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("resource/<int:resource_id>", views.resource_view, name="resource_view"),

    # API Route
    path("resource/<str:content_type>", views.resource, name="resource"),
]

from django.urls import path
from .views import index, project, login, logout, auth, register

urlpatterns = [
    path("", index, name="index"),
    path("project", project, name="project"),
    path("logout", logout, name="logout"),
    path("auth", auth, name="auth"),
    path("login", login, name="login"),
    path("register", register, name="register"),
]
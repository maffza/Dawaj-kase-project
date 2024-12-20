from django.urls import path
from .views import index, project, login, logout, auth, register, search, campaign_create, insert_campaign

urlpatterns = [
    path("", index, name="index"),
    path("project/<slug>", project, name="project"),
    path("logout", logout, name="logout"),
    path("auth", auth, name="auth"),
    path("login", login, name="login"),
    path("register", register, name="register"),
    path("search", search, name="search"),
    path("campaign_create", campaign_create, name="campaign_create"),
    path("insert_campaign", insert_campaign, name="insert_campaign"),
]
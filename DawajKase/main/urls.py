from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("project/<slug>", project, name="project"),
    path("logout", logout, name="logout"),
    path("auth", auth, name="auth"),
    path("login", login, name="login"),
    path("register", register, name="register"),
    path("search", search, name="search"),
    path("search_bar", search_bar, name="search_bar"),
    path("campaign_create", campaign_create, name="campaign_create"),
    path("insert_campaign", insert_campaign, name="insert_campaign"),
    path("favourite/<id>", favourite_campaign, name="favourite_campaign"),
    path("donate/<id>", donate, name="donate"),
    path("project_adm/<slug>", project_adm, name="project_adm"),
    path("confirmation_tab", confirmation_tab, name="confirmation_tab"),
    path("become_creator", become_creator, name="become_creator"),
    path("change_role", change_role, name="change_role"),
    path("approve_campaign", approve_campaign, name="approve_campaign"),
]
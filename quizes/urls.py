from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from ninja import NinjaAPI

api = NinjaAPI(urls_namespace="api")

api.add_router("/question", "survey.api.router")

urlpatterns = [
    path("", include(("survey.urls", "survey"), namespace="survey")),
    path("api/", api.urls),
    path("registration/login/", LoginView.as_view(), name="login"),
    path("registration/logout/", LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
]

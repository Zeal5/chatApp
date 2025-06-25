from django.urls import path
from .views import login_or_signup, user_logout


urlpatterns = [
    path("", login_or_signup, name="login_or_signup"),
    path("logout/", user_logout, name="logout"),
]

"""emailotpvarification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from otpvarify import views as otpviews
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", otpviews.Home.as_view(), name="home"),
    path("signup/", otpviews.SignupView.as_view(), name="signup"),
    path("account-varify/<slug:token>/", otpviews.account_verify, name="account_varify"),
    path("login/", otpviews.MylonginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/login/"), name="logout")
]

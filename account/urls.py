from django.urls import path
from .views import Login,VerifyOTP, logout_view, dashboard,change_information

app_name = "account"

urlpatterns = [
    path("login/",Login.as_view(),name="login"),
    path("login/verify",VerifyOTP.as_view(),name="verify_otp"),
    path("logout/",logout_view,name="logout"),
    path("dashboard/",dashboard,name="dashboard"),
    path("change_information/",change_information,name="change_information"),
]
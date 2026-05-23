from django.urls import path
from .views import index, about, contact, project

app_name = "main"

urlpatterns = [
    path('',index,name="index"),
    path('about/',about,name="about"),
    path('contact/',contact,name="contact"),
    path('project/',project,name="project")
]

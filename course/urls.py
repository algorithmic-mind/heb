from django.urls import path , re_path
from .views import courses,course_detail

app_name = "course"


urlpatterns = [
    path("",courses,name="courses"),
    re_path(r'^course/(?P<slug>[-\w]+)/$', course_detail, name='course_detail'),
]
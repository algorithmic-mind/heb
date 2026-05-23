from django.urls import path, re_path
from .views import blog, blog_detail

app_name = "blog"

urlpatterns = [
   
    path('',blog,name="blog"),
    re_path(r'^post/(?P<slug>[-\w]+)/$', blog_detail, name='blog_detail'),
]

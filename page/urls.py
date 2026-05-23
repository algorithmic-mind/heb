from django.urls import path, re_path
from .views import page

app_name = "page"

urlpatterns = [
    re_path(r'^(?P<slug>[-\w]+)/$', page, name='page'),
]

"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog.views import tinymce_upload_image,tinymce_delete_image
from django.conf import settings
from django.views.static import serve
import re

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('account/', include('account.urls')),
    path('courses/', include('course.urls')),
    
    #path('comment/', include('comment.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('tinymce/upload_image/', tinymce_upload_image, name='tinymce_upload_image'),
    path('tinymce/delete_image/', tinymce_delete_image, name='tinymce_delete_image'),
    path('', include('main.urls')),
    path('blog/', include('blog.urls')),
    path('page/', include('page.urls')),
    path('payment/', include('payment.urls')),
    path('account/', include('account.urls')),
] 
# سرو فایل‌ها در حالت DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # برای تست در محیط توسعه با DEBUG=False
    urlpatterns += [
        path('public/static/<path:path>', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
        path('public/media/<path:path>', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

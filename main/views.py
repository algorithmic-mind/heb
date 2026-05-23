from django.shortcuts import render
from .models import Slider, Partner, Source
from course.models import Course
from blog.models import Post
from utils.sms import send_otp
# Create your views here.

def index(request):
    #send_otp("09334751798",code="8992")
    context = {
        "sliders": Slider.objects.filter(is_active=True).all(),
        "partners": Partner.objects.all(),
        "featured_courses": Course.objects.filter(
        is_featured=True,
    ).order_by('-published_at'),
        "featured_posts": Post.objects.filter(
        is_featured=True,
        status='published'
    ).order_by('-published_at'),
    'sources': Source.objects.all(),
    }
    return render(request,'main/index.html',context=context)





def about(request):
   
    return render(request,'main/about.html')



def contact(request):
   
    return render(request,'main/contact.html')



def project(request):
   
    return render(request,'main/project.html')
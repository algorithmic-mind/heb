from django.shortcuts import render,get_object_or_404
from .models import Course


# Create your views here.
def courses(request):

    context = {
        "courses": Course.objects.all()
    }
    return render(request,"course/courses.html",context=context ) 





def course_detail(request, slug):
   
    course = get_object_or_404(Course, slug=slug)
    
   
    
    context = {
        'course': course,
        
    }
    
    return render(request, "course/course_detail.html", context=context)
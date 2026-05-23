from django.shortcuts import get_object_or_404, render
from .models import ContentPage

def page(request, slug):
    page = get_object_or_404(
        ContentPage.objects.filter(status='published'), 
        slug=slug
    )
    
    context = {
        'page': page,
      
    }
    
    return render(request, 'page/content_page_detail.html', context)
from .models import SiteSettings
from page.models import ContentPage

def site_settings(request):
    try:
        settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        settings = None
    return {'site_settings': settings}




def pages(request):
    try:
        all_pages = ContentPage.objects.filter(status='published',show_in_navigation=True)
    except ContentPage.DoesNotExist:
        all_pages = None
    return {'pages': all_pages}
from django.shortcuts import render, get_object_or_404
from .models import Post
import os
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
import json


@csrf_exempt
@require_POST
@login_required  # فقط کاربران وارد شده بتوانند آپلود کنند
def tinymce_upload_image(request):
    """آپلود تصویر برای TinyMCE"""
    
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'فایلی انتخاب نشده است'}, status=400)
    
    file = request.FILES['file']
    
    # بررسی نوع فایل
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    file_extension = os.path.splitext(file.name)[1].lower()
    
    if file_extension not in allowed_extensions:
        return JsonResponse({'error': 'فرمت فایل مجاز نیست'}, status=400)
    
    # بررسی سایز فایل (حداکثر 5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        return JsonResponse({'error': 'سایز فایل بیش از حد مجاز است'}, status=400)
    
    try:
        # تولید نام منحصر به فرد برای فایل
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        
        # مسیر آپلود
        upload_path = os.path.join(
            getattr(settings, 'TINYMCE_UPLOAD_PATH', 'tinymce_uploads/'),
            unique_filename
        )
        
        # ذخیره فایل
        path = default_storage.save(upload_path, ContentFile(file.read()))
        
        # تغییر سایز تصویر اگر بزرگ باشد
        full_path = os.path.join(settings.MEDIA_ROOT, path)
        try:
            with Image.open(full_path) as img:
                # تغییر سایز اگر عرض بیشتر از 800 پیکسل باشد
                if img.width > 800:
                    ratio = 800 / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((800, new_height), Image.Resampling.LANCZOS)
                    img.save(full_path, optimize=True, quality=85)
        except Exception as e:
            print(f"خطا در تغییر سایز تصویر: {e}")
        
        # URL تصویر
        file_url = settings.MEDIA_URL + path
        
        return JsonResponse({
            'location': request.build_absolute_uri(file_url)
        })
        
    except Exception as e:
        return JsonResponse({'error': f'خطا در آپلود فایل: {str(e)}'}, status=500)

# View اختیاری برای حذف تصاویر
@csrf_exempt
@require_POST
@login_required
def tinymce_delete_image(request):
    """حذف تصویر از TinyMCE"""
    try:
        data = json.loads(request.body)
        image_url = data.get('url')
        
        if not image_url:
            return JsonResponse({'error': 'URL تصویر ارسال نشده'}, status=400)
        
        # استخراج مسیر فایل از URL
        if settings.MEDIA_URL in image_url:
            file_path = image_url.split(settings.MEDIA_URL)[1]
            
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'فایل یافت نشد'}, status=404)
        
        return JsonResponse({'error': 'URL نامعتبر'}, status=400)
        
    except Exception as e:
        return JsonResponse({'error': f'خطا در حذف فایل: {str(e)}'}, status=500)


def blog(request):

    context = {
       
        'blogs' : Post.objects.all()
    }

    return render(request,"blog/blog.html",context=context)



def blog_detail(request, slug):
   
    post = get_object_or_404(Post, slug=slug)
    
    related_posts = Post.objects.exclude(slug=slug)[:3]

    comments = post.comments.all().order_by('-created_at')
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
    }
    
    return render(request, "blog/blog_detail.html", context=context)
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from tinymce.models import HTMLField
from django.core.validators import FileExtensionValidator

class ContentPage(models.Model):
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
        ('hidden', 'مخفی'),
    ]
    
    # اطلاعات پایه صفحه
    title = models.CharField(
        verbose_name='عنوان صفحه',
        max_length=200,
        help_text='عنوان صفحه که در هدر و عنوان مرورگر نمایش داده می‌شود'
    )
    
    slug = models.SlugField(
        verbose_name='اسلاگ',
        max_length=200,
        unique=True,
        allow_unicode=True,
        help_text='آدرس صفحه در URL (به صورت خودکار از عنوان ایجاد می‌شود)'
    )
    
    content = HTMLField(
        verbose_name='محتوا',
        help_text='محتوا اصلی صفحه که با ویرایشگر TinyMCE قابل ویرایش است'
    )
    
    # سئو و متا اطلاعات
    meta_title = models.CharField(
        verbose_name='عنوان متا',
        max_length=60,
        blank=True,
        help_text='عنوانی که در نتایج جستجو نمایش داده می‌شود (حداکثر 60 کاراکتر)'
    )
    
    meta_description = models.TextField(
        verbose_name='توضیحات متا',
        max_length=160,
        blank=True,
        help_text='توضیح مختصر برای نمایش در نتایج جستجو (حداکثر 160 کاراکتر)'
    )
    
    meta_keywords = models.CharField(
        verbose_name='کلمات کلیدی متا',
        max_length=200,
        blank=True,
        help_text='کلمات کلیدی مرتبط با صفحه (با کاما جدا شوند)'
    )
    
    # وضعیت و نمایش
    status = models.CharField(
        verbose_name='وضعیت',
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    show_in_navigation = models.BooleanField(
        verbose_name='نمایش در منو',
        default=False,
        help_text='آیا این صفحه در منوی اصلی سایت نمایش داده شود؟'
    )
    
    navigation_order = models.PositiveIntegerField(
        verbose_name='ترتیب در منو',
        default=0,
        help_text='ترتیب نمایش صفحه در منو (اعداد کمتر اولویت بالاتری دارند)'
    )
    
    # تصویر شاخص
    featured_image = models.ImageField(
        verbose_name='تصویر شاخص',
        upload_to='pages/featured_images/',
        blank=True,
        null=True,
        help_text='تصویر مرتبط با صفحه (سایز پیشنهادی: 1200x630 پیکسل)'
    )
    
    image_alt = models.CharField(
        verbose_name='متن جایگزین تصویر',
        max_length=200,
        blank=True,
        help_text='توضیح مختصر درباره تصویر برای موتورهای جستجو'
    )
    
    # تاریخ‌ها
    created_at = models.DateTimeField(
        verbose_name='تاریخ ایجاد',
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        verbose_name='تاریخ بروزرسانی',
        auto_now=True
    )
    
    published_at = models.DateTimeField(
        verbose_name='تاریخ انتشار',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'صفحه محتوایی'
        verbose_name_plural = 'صفحات محتوایی'
        ordering = ['navigation_order', 'title']
        indexes = [
            models.Index(fields=['slug', 'status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # ایجاد اسلاگ خودکار از عنوان
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        
        # تنظیم تاریخ انتشار اگر وضعیت به منتشر شده تغییر کرد
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        
        # اگر عنوان متا مشخص نشده باشد، از عنوان صفحه استفاده می‌کنیم
        if not self.meta_title:
            self.meta_title = self.title[:60]
            
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('page:content_page_detail', args=[self.slug])

    def is_published(self):
        return self.status == 'published'
    
    def get_meta_title(self):
        return self.meta_title or self.title

    def get_meta_description(self):
        return self.meta_description or ""
    
    def get_keywords_list(self):
        if self.meta_keywords:
            return [k.strip() for k in self.meta_keywords.split(',')]
        return []
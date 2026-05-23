from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Category(models.Model):
    name = models.CharField("نام دسته‌بندی", max_length=100, unique=True)
    slug = models.SlugField("اسلاگ", max_length=100, unique=True, allow_unicode=True)
    description = models.TextField("توضیحات", blank=True)
    is_active = models.BooleanField("فعال", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_posts', args=[self.slug])


class Tag(models.Model):
    name = models.CharField("نام تگ", max_length=50, unique=True)
    slug = models.SlugField("اسلاگ", max_length=50, unique=True, allow_unicode=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag_posts', args=[self.slug])

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
        ('archived', 'آرشیو شده'),
    ]

    # اطلاعات پایه پست
    title = models.CharField("عنوان پست", max_length=200)
    slug = models.SlugField("اسلاگ", max_length=200, unique=True, allow_unicode=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts',
        verbose_name="نویسنده"
    )
    content = HTMLField("محتوا")
    excerpt = models.TextField(
        "چکیده", 
        blank=True, 
        help_text="خلاصه کوتاه از محتوای پست (برای نمایش در صفحات لیست پست‌ها)"
    )
    
    # تصاویر
    featured_image = models.ImageField(
        "تصویر شاخص",
        upload_to='blog/featured_images/',
        blank=True,
        null=True,
        help_text="تصویر اصلی مرتبط با پست (سایز پیشنهادی: 1200x630 پیکسل)"
    )
    image_alt = models.CharField(
        "متن جایگزین تصویر",
        max_length=200,
        blank=True,
        help_text="توضیح مختصر درباره تصویر برای موتورهای جستجو و دسترسی‌پذیری"
    )
    
    # فیلدهای SEO
    meta_title = models.CharField(
        "عنوان متا",
        max_length=60,
        blank=True,
        help_text="عنوانی که در نتایج جستجو نمایش داده می‌شود (حداکثر 60 کاراکتر)"
    )
    meta_description = models.TextField(
        "توضیحات متا",
        blank=True,
        max_length=160,
        help_text="توضیح مختصر برای نمایش در نتایج جستجو (حداکثر 160 کاراکتر)"
    )
    meta_keywords = models.CharField(
        "کلمات کلیدی متا",
        max_length=200,
        blank=True,
        help_text=_('با علامت کامای انگلیسی (,) جدا کنید')
    )
    canonical_url = models.URLField(
        "آدرس کانونیکال",
        blank=True,
        help_text="آدرس اصلی پست در صورت وجود محتوای تکراری"
    )
    
    # تنظیمات نمایش
    status = models.CharField(
        "وضعیت",
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    is_featured = models.BooleanField("پست ویژه", default=False)
    allow_comments = models.BooleanField("اجازه دیدگاه", default=True)
    view_count = models.PositiveIntegerField("تعداد بازدید", default=0)
    
    # تاریخ‌ها
    published_at = models.DateTimeField(
        "تاریخ انتشار", 
        null=True, 
        blank=True,
        help_text="تاریخ و زمان انتشار پست"
    )
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ بروزرسانی", auto_now=True)
    
    # روابط
    categories = models.ManyToManyField(
        'Category',
        related_name='posts',
        verbose_name="دسته‌بندی‌ها"
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='posts',
        blank=True,
        verbose_name="تگ‌ها"
    )

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        # اگر عنوان متا مشخص نشده باشد، از عنوان پست استفاده می‌کنیم
        if not self.meta_title:
            self.meta_title = self.title[:60]
        
        # اگر توضیحات متا مشخص نشده باشد، از چکیده پست استفاده می‌کنیم
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]
            
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def increase_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def get_meta_title(self):
        return self.meta_title or self.title

    def get_meta_description(self):
        return self.meta_description or self.excerpt or ""

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="پست"
    )
    name = models.CharField("نام", max_length=100)
    email = models.EmailField("ایمیل", blank=True)
    content = models.TextField("متن دیدگاه")
    is_approved = models.BooleanField("تایید شده", default=False)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name="پاسخ به"
    )
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "دیدگاه"
        verbose_name_plural = "دیدگاه‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return f"دیدگاه {self.name} برای پست {self.post.title}"

    def get_absolute_url(self):
        return f"{self.post.get_absolute_url()}#comment-{self.id}"
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from tinymce.models import HTMLField
from PIL import Image
import os

class Category(models.Model):
    """دسته‌بندی دوره‌ها"""
    name = models.CharField(max_length=100, verbose_name="نام دسته")
    slug = models.SlugField("اسلاگ", max_length=200, unique=True, allow_unicode=True)
    description = models.TextField(blank=True, verbose_name="توضیحات")
    icon = models.CharField(max_length=50, blank=True, verbose_name="آیکون")
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='children',
        verbose_name="دسته والد"
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('courses:category', kwargs={'slug': self.slug})

class Tag(models.Model):
    """برچسب‌های دوره‌ها"""
    name = models.CharField(max_length=50, unique=True, verbose_name="نام برچسب")
    slug = models.SlugField("اسلاگ", max_length=200, unique=True, allow_unicode=True)
    
    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Instructor(models.Model):
    """مدرسین"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    bio = HTMLField("بیوگرافی", blank=True)
    specialization = models.CharField(max_length=200, verbose_name="تخصص")
    experience_years = models.PositiveIntegerField(
        default=0, 
        verbose_name="سال‌های تجربه"
    )
    avatar = models.ImageField(
        upload_to='instructors/', 
        blank=True, 
        null=True,
        verbose_name="تصویر پروفایل"
    )
    website = models.URLField(blank=True, verbose_name="وب‌سایت")
    linkedin = models.URLField(blank=True, verbose_name="لینکدین")
    github = models.URLField(blank=True, verbose_name="گیت‌هاب")
    is_verified = models.BooleanField(default=False, verbose_name="تایید شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "مدرس"
        verbose_name_plural = "مدرسین"
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.avatar.path)

class Course(models.Model):
    """دوره‌های آموزشی"""
    
    LEVEL_CHOICES = [
        ('مبتدی', 'مبتدی'),
        ('متوسط', 'متوسط'),
        ('پیشرفته', 'پیشرفته'),
        ('تخصصی', 'تخصصی'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
        ('archived', 'بایگانی شده'),
    ]
    
    LANGUAGE_CHOICES = [
        ('fa', 'فارسی'),
        ('en', 'انگلیسی'),
        ('ar', 'عربی'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="عنوان دوره")
    slug = models.SlugField("اسلاگ", max_length=200, unique=True, allow_unicode=True)
    short_description = models.TextField(max_length=500, verbose_name="توضیح کوتاه")
    description = HTMLField("توضیحات کامل")
    requirements = HTMLField("پیش‌نیازها", blank=True)
    what_you_learn = HTMLField("آنچه یاد خواهید گرفت", blank=True)
    
    # تصاویر
    thumbnail = models.ImageField(
        upload_to='courses/thumbnails/', 
        verbose_name="تصویر شاخص"
    )
    banner = models.ImageField(
        upload_to='courses/banners/', 
        blank=True, 
        null=True,
        verbose_name="بنر دوره"
    )
    
    # روابط
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT,
        related_name='courses',
        verbose_name="دسته‌بندی"
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="برچسب‌ها")
    instructor = models.ForeignKey(
        Instructor, 
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name="مدرس"
    )
    students = models.ManyToManyField(
        User, 
        through='Enrollment', 
        blank=True,
        verbose_name="دانشجویان"
    )
    
    # جزئیات دوره
    level = models.CharField(
        max_length=20, 
        choices=LEVEL_CHOICES,
        default='beginner',
        verbose_name="سطح دوره"
    )
    language = models.CharField(
        max_length=5, 
        choices=LANGUAGE_CHOICES,
        default='fa',
        verbose_name="زبان دوره"
    )
    duration = models.PositiveIntegerField(
        help_text="مدت زمان به ساعت",
        verbose_name="مدت زمان (ساعت)"
    )
    
    # قیمت‌گذاری
    price = models.PositiveIntegerField(default=0, verbose_name="قیمت (ریال)")
    discount_price = models.DecimalField(
        max_digits=10, 
        decimal_places=0,
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="قیمت با تخفیف (ریال)"
    )
    discount_percent = models.PositiveIntegerField(default=0, verbose_name="درصد تخفیف")
    is_free = models.BooleanField(default=False, verbose_name="رایگان")
    
    # وضعیت
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="وضعیت"
    )
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    is_bestseller = models.BooleanField(default=False, verbose_name="پرفروش")
    
    # تاریخ‌ها
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انتشار")
    
    # آمار
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    
    class Meta:
        verbose_name = "دوره آموزشی"
        verbose_name_plural = "دوره‌های آموزشی"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # تغییر سایز تصویر شاخص
        if self.thumbnail:
            img = Image.open(self.thumbnail.path)
            if img.height > 400 or img.width > 600:
                img.thumbnail((600, 400))
                img.save(self.thumbnail.path)
        
        # تغییر سایز بنر
        if self.banner:
            img = Image.open(self.banner.path)
            if img.height > 300 or img.width > 1200:
                img.thumbnail((1200, 300))
                img.save(self.banner.path)
    
    @property
    def get_price(self):
        """قیمت نهایی دوره"""
        if self.is_free:
            return 0
        if self.discount_price:
            return self.discount_price
        return self.price
    
    @property
    def has_discount(self):
        """آیا دوره تخفیف دارد؟"""
        return self.discount_price and self.discount_price < self.price
    
    @property
    def discount_percentage(self):
        """درصد تخفیف"""
        if self.has_discount:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
    
    @property
    def total_lessons(self):
        """تعداد کل درس‌ها"""
        return self.sections.aggregate(
            total=models.Sum('lessons__id__count')
        )['total'] or 0
    
    @property
    def total_students(self):
        """تعداد کل دانشجویان"""
        return self.enrollments.filter(is_active=True).count()
    
    @property
    def average_rating(self):
        """میانگین امتیاز"""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return reviews.aggregate(avg=models.Avg('rating'))['avg']
        return 0
    
    @property
    def total_reviews(self):
        """تعداد کل نظرات"""
        return self.reviews.filter(is_approved=True).count()
    

    def get_final_price(self):
        """محاسبه قیمت نهایی با احتساب تخفیف"""
        if self.is_free:
            return 0
        
        if self.discount_percent > 0:
            discount_amount = (self.price * self.discount_percent) / 100
            return int(self.price - discount_amount)
        
        return self.price
    
    def get_discount_amount(self):
        """محاسبه مقدار تخفیف"""
        if self.discount_percent > 0:
            return int((self.price * self.discount_percent) / 100)
        return 0
    
    def has_user_enrolled(self, user):
        """بررسی اینکه کاربر در این دوره ثبت‌نام کرده باشد"""
        if not user.is_authenticated:
            return False
        from payment.models import CourseEnrollment
        return CourseEnrollment.objects.filter(
            user=user, 
            course=self, 
            is_active=True
        ).exists()

class Section(models.Model):
    """بخش‌های دوره"""
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name="دوره"
    )
    title = models.CharField(max_length=200, verbose_name="عنوان بخش")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    order = models.PositiveIntegerField(default=1, verbose_name="ترتیب")
    is_free = models.BooleanField(default=False, verbose_name="بخش رایگان")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "بخش"
        verbose_name_plural = "بخش‌ها"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    """درس‌های دوره"""
    
    LESSON_TYPES = [
        ('video', 'ویدیو'),
        ('text', 'متن'),
        ('quiz', 'آزمون'),
        ('assignment', 'تکلیف'),
        ('file', 'فایل'),
    ]
    
    section = models.ForeignKey(
        Section, 
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="بخش"
    )
    title = models.CharField(max_length=200, verbose_name="عنوان درس")
    slug = models.SlugField("اسلاگ", max_length=200, unique=True, allow_unicode=True)
    description = models.TextField(blank=True, verbose_name="توضیحات")
    content = HTMLField("محتوا", blank=True)
    
    lesson_type = models.CharField(
        max_length=20,
        choices=LESSON_TYPES,
        default='video',
        verbose_name="نوع درس"
    )
    
    # فایل‌های درس
    video_file = models.FileField(
        upload_to='courses/videos/', 
        blank=True, 
        null=True,
        verbose_name="فایل ویدیو"
    )
    video_url = models.URLField(blank=True, verbose_name="لینک ویدیو")
    attachment = models.FileField(
        upload_to='courses/attachments/', 
        blank=True, 
        null=True,
        verbose_name="ضمیمه"
    )
    
    duration = models.PositiveIntegerField(
        default=0,
        help_text="مدت زمان به ثانیه",
        verbose_name="مدت زمان (ثانیه)"
    )
    order = models.PositiveIntegerField(default=1, verbose_name="ترتیب")
    is_free = models.BooleanField(default=False, verbose_name="درس رایگان")
    is_published = models.BooleanField(default=True, verbose_name="منتشر شده")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "درس‌ها"
        ordering = ['order']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('courses:lesson', kwargs={
            'course_slug': self.section.course.slug,
            'lesson_slug': self.slug
        })

class Enrollment(models.Model):
    """ثبت‌نام در دوره"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="دوره"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت‌نام")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    progress = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="پیشرفت (درصد)"
    )
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ تکمیل")
    certificate_issued = models.BooleanField(default=False, verbose_name="گواهی صادر شده")
    
    class Meta:
        verbose_name = "ثبت‌نام"
        verbose_name_plural = "ثبت‌نام‌ها"
        unique_together = ['user', 'course']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

class LessonProgress(models.Model):
    """پیشرفت درس"""
    enrollment = models.ForeignKey(
        Enrollment, 
        on_delete=models.CASCADE,
        related_name='lesson_progresses',
        verbose_name="ثبت‌نام"
    )
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.CASCADE,
        verbose_name="درس"
    )
    is_completed = models.BooleanField(default=False, verbose_name="تکمیل شده")
    watched_duration = models.PositiveIntegerField(
        default=0,
        verbose_name="مدت تماشا (ثانیه)"
    )
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ تکمیل")
    last_watched_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بازدید")
    
    class Meta:
        verbose_name = "پیشرفت درس"
        verbose_name_plural = "پیشرفت درس‌ها"
        unique_together = ['enrollment', 'lesson']
    
    def __str__(self):
        return f"{self.enrollment.user.username} - {self.lesson.title}"

class Review(models.Model):
    """نظرات و امتیازدهی دوره‌ها"""
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="دوره"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="امتیاز"
    )
    title = models.CharField(max_length=200, verbose_name="عنوان نظر")
    comment = models.TextField(verbose_name="متن نظر")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "دیدگاه"
        verbose_name_plural = "دیدگاه‌ها"
        unique_together = ['course', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.course.title} - {self.user.username} ({self.rating}⭐)"

class Certificate(models.Model):
    """گواهی‌نامه‌های دوره"""
    enrollment = models.OneToOneField(
        Enrollment, 
        on_delete=models.CASCADE,
        verbose_name="ثبت‌نام"
    )
    certificate_id = models.CharField(max_length=50, unique=True, verbose_name="شماره گواهی")
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ صدور")
    is_valid = models.BooleanField(default=True, verbose_name="معتبر")
    
    class Meta:
        verbose_name = "گواهی‌نامه"
        verbose_name_plural = "گواهی‌نامه‌ها"
    
    def __str__(self):
        return f"گواهی {self.enrollment.course.title} - {self.enrollment.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.certificate_id:
            import uuid
            self.certificate_id = f"CERT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
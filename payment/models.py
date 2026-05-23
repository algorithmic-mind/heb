from django.db import models
from django.contrib.auth.models import User
from course.models import Course


class Payment(models.Model):
    """مدل ثبت پرداخت‌های کاربران"""
    
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('successful', 'پرداخت موفق'),
        ('failed', 'پرداخت ناموفق'),
        ('cancelled', 'لغو شده'),
        ('refunded', 'بازگشت داده شده'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="دوره")
    amount = models.PositiveIntegerField(verbose_name="مبلغ (ریال)")
    authority = models.CharField(max_length=100, verbose_name="کد Authority", blank=True, null=True)
    ref_id = models.CharField(max_length=100, verbose_name="کد رهگیری", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت پرداخت")
    description = models.TextField(verbose_name="توضیحات", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    verified_at = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ تایید")
    
    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.amount}"
    
    @property
    def is_successful(self):
        return self.status == 'successful'


class CourseEnrollment(models.Model):
    """ثبت‌نام کاربران در دوره‌ها"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="دوره")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name="پرداخت مرتبط")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت‌نام")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    class Meta:
        verbose_name = "ثبت‌نام در دوره"
        verbose_name_plural = "ثبت‌نام‌ها در دوره‌ها"
        unique_together = ('user', 'course')
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
# models.py
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='profile_pics/',
        default='default_avatar.jpg',
        blank=True,
        null=True,
        verbose_name='تصویر پروفایل'
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name='بیوگرافی')
    
    
    def __str__(self):
        return f"پروفایل {self.user.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # تغییر سایز تصویر به 300x300 پیکسل
        if self.avatar:
            img = Image.open(self.avatar.path)
            
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
    
    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل‌ها'



class SMSOTP(models.Model):
    phone = models.CharField(max_length=15, verbose_name='شماره موبایل',null=True,blank=True)
    code = models.CharField(max_length=4, verbose_name="کد")
    created_at = models.DateTimeField(verbose_name="تاریخ ایجاد")
    expires_at = models.DateTimeField(verbose_name="تاریخ انقضا",null=True, blank=True)

    class Meta:
        verbose_name = 'کد OTP'
        verbose_name_plural = 'کد های OTP'

    def save(self, *args, **kwargs):
        
        if not self.pk:
            self.created_at = timezone.now()
            self.expires_at = self.created_at + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.phone} - {self.code}"
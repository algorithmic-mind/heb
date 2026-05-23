from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField


class SiteSettings(models.Model):
    # Basic Site Information
    site_name = models.CharField(_('عنوان'), max_length=100)
    site_description = models.TextField(_('توضحیات'), blank=True)
    site_slogan = models.CharField(_('شعار'), max_length=200, blank=True)
    site_logo = models.ImageField(
        _('لوگو'), 
        upload_to='settings/logo/', 
        blank=True, 
        null=True
    )
    site_favicon = models.ImageField(
        _('آیکون'), 
        upload_to='settings/favicon/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(['ico', 'png'])]
    )
    footer_text = models.TextField(_('متن فوتر'), blank=True)
    copyright_text = models.CharField(_('متن کپی رایت'), max_length=200, blank=True)
    

    landing_title = models.CharField(_('عنوان لندینگ'), max_length=200, blank=True)
    landing_content = HTMLField(_("محتوای لندینگ"), blank=True)

    # Contact Information
    contact_email = models.EmailField(_('ایمیل'), blank=True)
    contact_phone = models.CharField(_('تلفن'), max_length=20, blank=True)
    contact_address = models.TextField(_('آدرس'), blank=True)
    
    # Social Media Links
    eitaa_url = models.URLField(_('آدرس ایتا'), blank=True)
    rubika_url = models.URLField(_('آدرس روبیکا'), blank=True)
   

    # typed text
    special_texts = models.TextField(
        _('جملات خاص تایپ شونده'),
        blank=True,
        help_text='جملات را با خط تیره (-) از هم جدا کنید. مثال: جمله اول-جمله دوم-جمله سوم و... - بدون ENTER' 
    )

    # Summary box
    students_count = models.CharField(_('تعداد دانشجو'), max_length=20, blank=True)
    courses_count = models.CharField(_('تعداد دوره آنلاین'), max_length=20, blank=True)
    hours_count = models.CharField(_('تعداد ساعت آموزش '), max_length=20, blank=True)
    blog_count = models.CharField(_('تعداد مقاله  '), max_length=20, blank=True)

    
    # SEO Settings
    meta_title = models.CharField(
        _('عنوان پایه سئو'), 
        max_length=60, 
        blank=True,
        help_text=_('پیشنهاد: بین ۵۰ الی ۶۰ کلمه')
    )
    meta_description = models.TextField(
        _('توضیحات پایه سئو'), 
        blank=True,
        help_text=_('پیشنهاد: بین ۱۵- الی ۱۸۰ کلمه')
    )
    meta_keywords = models.CharField(
        _('کلمات کلیدی پایه سئو'), 
        max_length=200, 
        blank=True,
        help_text=_('با علامت کامای انگلیسی (,) جدا کنید')
    )
    google_analytics_code = models.CharField(
        _('کد گوگل آنالیتیکس'), 
        max_length=50, 
        blank=True
    )
    google_tag_manager_code = models.CharField(
        _('کد گوگل تگ'), 
        max_length=50, 
        blank=True
    )
    
    # Additional Settings
    maintenance_mode = models.BooleanField(
        _('حالت تعمیر'), 
        default=False,
        help_text=_('زمانی که فعال باشد، سایت از دسترس حارج می‌شود')
    )
    custom_css = models.TextField(_('Custom CSS'), blank=True)
    custom_js = models.TextField(_('Custom JavaScript'), blank=True)
    
    # Date Information
    created_at = models.DateTimeField(_('ایجاد شده در'), auto_now_add=True)
    updated_at = models.DateTimeField(_('بروز شده در'), auto_now=True)
    
    class Meta:
        verbose_name = _('تنظیمات')
        verbose_name_plural = _('تنظیمات های سایت')
    
    def __str__(self):
        return self.site_name


    def get_special_texts(self):
        """
        تبدیل جملات جدا شده با خط تیره به لیست
        """
        if self.special_texts:
            return self.special_texts.split("-")
        


class Slider(models.Model):
    title = models.CharField(_('عنوان'), max_length=100)
    image = models.ImageField(
        _('تصویر'), 
        upload_to='sliders/',
        help_text=_('سایز پیشنهادی: ۱۹۲۰ در ۱۰۸۰')
    )
    link = models.URLField(_('لینک اسلاید'), blank=True)
    is_active = models.BooleanField(_('فعال'), default=True)
   
    
    # SEO Fields for Slider
    alt_text = models.CharField(
        _('متن alt جایگزین'), 
        max_length=100, 
        blank=True,
        help_text=_('برای بهبود سئو')
    )
    
    class Meta:
        verbose_name = _('اسلایدر')
        verbose_name_plural = _('اسلایدر ها')
       
    
    def __str__(self):
        return self.title



class Partner(models.Model):
    logo = models.ImageField(
        verbose_name=_('لوگوی همکاران'),
        upload_to='partners/',
        help_text='لوگوی رسمی همکار را با فرمت مناسب (JPG, PNG) آپلود کنید'
    )

    created_at = models.DateTimeField(
        verbose_name='تاریخ ایجاد',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='تاریخ بروزرسانی',
        auto_now=True
    )

    class Meta:
        verbose_name = 'همکار'
        verbose_name_plural = 'همکاران'
        

    

class Source(models.Model):
    image = models.ImageField(
        verbose_name=_('تصویر منبع'),
        upload_to='sources/',
        help_text='تصویر منبع را با فرمت مناسب (JPG, PNG) آپلود کنید'
    )

    created_at = models.DateTimeField(
        verbose_name='تاریخ ایجاد',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='تاریخ بروزرسانی',
        auto_now=True
    )

    class Meta:
        verbose_name = 'منبع/مرجع'
        verbose_name_plural = 'منابع'  
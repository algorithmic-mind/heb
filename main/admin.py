from django.contrib import admin
from .models import SiteSettings, Slider
from django.utils.translation import gettext_lazy as _
from .models import Partner, Source


admin.site.site_header = _('پنل مدیریت آکادمی عبری')  # عنوان بالای پنل
admin.site.site_title = _('مدیریت سایت')       # عنوان تب مرورگر
admin.site.index_title = _('مدیریت آکادمی')     # عنوان صفحه اصلی پنل

admin.site.register(Source)

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', )
    readonly_fields = ('logo_preview',)
    
    fieldsets = (
        (None, {
            'fields': (
                'logo',
                
            )
        }),
    )

    def logo_preview(self, obj):
        from django.utils.html import format_html
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.logo.url)
        return "بدون تصویر"
    logo_preview.short_description = 'پیش‌نمایش لوگو'



@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'maintenance_mode')
    fieldsets = (
        (_('اطلاعات پایه'), {
            'fields': (
                'site_name', 'site_description', 'site_slogan',
                'site_logo', 'site_favicon', 'footer_text', 'copyright_text'
            )
        }),
        (_('باکس خلاصه آمار برای کاربران'), {
            'fields': ('students_count', 'blog_count', 'hours_count','courses_count')
        }),

        (_('لندنیگ'), {
            'fields': ('landing_title', 'landing_content')
        }),


        (_('متون خاص'), {
            'fields': ('special_texts',)
        }),
        (_('اطلاعات تماس'), {
            'fields': ('contact_email', 'contact_phone', 'contact_address')
        }),

        (_('شبکه های اجتماعی'), {
            'fields': (
                'eitaa_url', 'rubika_url',
                
            )
        }),
        (_('سئو پایه'), {
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
                'google_analytics_code', 'google_tag_manager_code'
            )
        }),
        (_('تنظیمات پیشرفته'), {
            'fields': ('maintenance_mode', 'custom_css', 'custom_js')
        }),
    )
    
    def has_add_permission(self, request):
        # Allow only one instance
        return not SiteSettings.objects.exists()


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = (['title', 'is_active'])
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('title',)
    prepopulated_fields = {'alt_text': ('title',)}
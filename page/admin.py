from django.contrib import admin
from django.utils.html import format_html
from .models import ContentPage

@admin.register(ContentPage)
class ContentPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'show_in_navigation', 'navigation_order', 'created_at')
    list_filter = ('status', 'show_in_navigation', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('status', 'show_in_navigation', 'navigation_order')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'published_at', 'featured_image_preview')
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': (
                'title', 'slug', 'content', 'featured_image', 
                'featured_image_preview', 'image_alt'
            )
        }),
        ('تنظیمات سئو', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('تنظیمات نمایش', {
            'fields': ('status', 'show_in_navigation', 'navigation_order')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )

    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />', 
                obj.featured_image.url
            )
        return "بدون تصویر"
    featured_image_preview.short_description = "پیش‌نمایش تصویر"
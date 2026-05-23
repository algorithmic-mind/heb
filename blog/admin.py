from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Post, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'post_count')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "تعداد پست‌ها"

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "تعداد پست‌ها"

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_at', 'is_featured', 'view_count')
    list_filter = ('status', 'categories', 'is_featured', 'published_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories', 'tags')
    date_hierarchy = 'published_at'
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'content', 'excerpt', 'featured_image')
        }),
        ('تنظیمات', {
            'fields': ('status', 'is_featured', 'allow_comments', 'published_at')
        }),
        ('بهینه سازی سئو', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url')
        }),
        ('طبقه‌بندی', {
            'fields': ('categories', 'tags')
        }),
        ('آمار', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.featured_image.url)
        return "بدون تصویر"
    featured_image_preview.short_description = "پیش‌نمایش تصویر شاخص"

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'content_short', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'email', 'content')
    list_editable = ('is_approved',)
    actions = ['approve_comments']

    def content_short(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_short.short_description = "متن دیدگاه"

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "تایید دیدگاه‌های انتخاب شده"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
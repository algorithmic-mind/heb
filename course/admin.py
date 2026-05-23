# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Category, Tag, Instructor, Course, Section, 
    Lesson, Enrollment, LessonProgress, Review, Certificate
)




admin.site.register(Certificate)
admin.site.register(LessonProgress)
admin.site.register(Review)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'courses_count', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    def courses_count(self, obj):
        return obj.courses.count()
    courses_count.short_description = 'تعداد دوره‌ها'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'courses_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def courses_count(self, obj):
        return obj.course_set.count()
    courses_count.short_description = 'تعداد دوره‌ها'

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'specialization', 'experience_years', 'is_verified', 'courses_count']
    list_filter = ['is_verified', 'experience_years', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
    list_editable = ['is_verified']
    readonly_fields = ['avatar_preview']
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user',)
        }),
        ('اطلاعات مدرس', {
            'fields': ('specialization', 'experience_years', 'bio')
        }),
        ('تصویر پروفایل', {
            'fields': ('avatar', 'avatar_preview')
        }),
        ('شبکه‌های اجتماعی', {
            'fields': ('website', 'linkedin', 'github')
        }),
        ('وضعیت', {
            'fields': ('is_verified',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'نام کامل'
    
    def courses_count(self, obj):
        return obj.courses.count()
    courses_count.short_description = 'تعداد دوره‌ها'
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 50%;" />', obj.avatar.url)
        return "تصویری انتخاب نشده"
    avatar_preview.short_description = 'پیش‌نمایش تصویر'

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1
    fields = ['title', 'order', 'is_free']

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ['title', 'lesson_type', 'duration', 'order', 'is_free', 'is_published']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'instructor', 'category', 'level', 'get_price_display', 
        'status', 'is_featured', 'total_students', 'created_at'
    ]
    list_filter = [
        'status', 'level', 'is_featured', 'is_bestseller', 'is_free',
        'category', 'created_at'
    ]
    search_fields = ['title', 'instructor__user__first_name', 'instructor__user__last_name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    readonly_fields = ['thumbnail_preview', 'banner_preview', 'views', 'created_at', 'updated_at']
    filter_horizontal = ['tags']
    inlines = [SectionInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('جزئیات دوره', {
            'fields': ('category', 'tags', 'instructor', 'level', 'language', 'duration')
        }),
        ('تصاویر', {
            'fields': ('thumbnail', 'thumbnail_preview', 'banner', 'banner_preview')
        }),
        ('قیمت‌گذاری', {
            'fields': ('is_free', 'price', 'discount_price')
        }),
        ('محتوای آموزشی', {
            'fields': ('requirements', 'what_you_learn')
        }),
        ('وضعیت و ویژگی‌ها', {
            'fields': ('status', 'is_featured', 'is_bestseller', 'published_at')
        }),
        ('آمار', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_price_display(self, obj):
        if obj.is_free:
            return mark_safe('<span style="color: green; font-weight: bold;">رایگان</span>')
        elif obj.has_discount:
            return format_html(
                '<del>{}</del> <span style="color: red; font-weight: bold;">{}</span>',
                f"{obj.price:,} تومان",
                f"{obj.discount_price:,} تومان"
            )
        else:
            return f"{obj.price:,} تومان"
    get_price_display.short_description = 'قیمت'
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="150" height="100" />', obj.thumbnail.url)
        return "تصویری انتخاب نشده"
    thumbnail_preview.short_description = 'پیش‌نمایش تصویر شاخص'
    
    def banner_preview(self, obj):
        if obj.banner:
            return format_html('<img src="{}" width="300" height="75" />', obj.banner.url)
        return "بنری انتخاب نشده"
    banner_preview.short_description = 'پیش‌نمایش بنر'

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_free', 'lessons_count']
    list_filter = ['is_free', 'course']
    search_fields = ['title', 'course__title']
    list_editable = ['order', 'is_free']
    inlines = [LessonInline]
    
    def lessons_count(self, obj):
        return obj.lessons.count()
    lessons_count.short_description = 'تعداد درس‌ها'

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'section', 'lesson_type', 'duration_display', 
        'order', 'is_free', 'is_published'
    ]
    list_filter = ['lesson_type', 'is_free', 'is_published', 'section__course']
    search_fields = ['title', 'section__title', 'section__course__title']
    list_editable = ['order', 'is_free', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('section', 'title', 'slug', 'description', 'lesson_type')
        }),
        ('محتوا', {
            'fields': ('content',)
        }),
        ('فایل‌ها', {
            'fields': ('video_file', 'video_url', 'attachment')
        }),
        ('تنظیمات', {
            'fields': ('duration', 'order', 'is_free', 'is_published')
        }),
    )
    
    def duration_display(self, obj):
        if obj.duration > 0:
            minutes, seconds = divmod(obj.duration, 60)
            return f"{minutes}:{seconds:02d}"
        return "-"
    duration_display.short_description = 'مدت زمان'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'course', 'enrolled_at', 'progress', 
        'is_active', 'certificate_issued'
    ]
    list_filter = ['is_active', 'certificate_issued', 'enrolled_at', 'course']
    search_fields = ['user__username', 'course__title']
    list_editable = ['is_active']
    readonly_fields = ['enrolled_at', 'progress']
    
    
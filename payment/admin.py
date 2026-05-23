from django.contrib import admin
from .models import Payment, CourseEnrollment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'amount', 'status', 'ref_id', 'created_at']
    list_filter = ['status', 'created_at', 'course']
    search_fields = ['user__username', 'user__email', 'course__title', 'ref_id', 'authority']
    readonly_fields = ['authority', 'ref_id', 'created_at', 'updated_at', 'verified_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('اطلاعات کلی', {
            'fields': ('user', 'course', 'amount', 'status', 'description')
        }),
        ('اطلاعات پرداخت', {
            'fields': ('authority', 'ref_id')
        }),
        ('زمان‌ها', {
            'fields': ('created_at', 'updated_at', 'verified_at')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # فقط ادمین اصلی بتواند پرداخت‌ها را حذف کند
        return request.user.is_superuser


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'payment', 'enrolled_at', 'is_active']
    list_filter = ['is_active', 'enrolled_at', 'course']
    search_fields = ['user__username', 'user__email', 'course__title']
    readonly_fields = ['enrolled_at']
    date_hierarchy = 'enrolled_at'
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
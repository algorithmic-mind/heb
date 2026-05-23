from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('request/<int:course_id>/', views.payment_request, name='payment_request'),
    path('verify/', views.payment_verify, name='payment_verify'),
    path('success/', views.payment_success, name='success'),
    path('error/', views.payment_error, name='error'),
    path('cancel/', views.payment_cancel, name='cancel'),
    path('my-payments/', views.my_payments, name='my_payments'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('test/<int:course_id>/', views.test_payment_request, name='test_payment_request'),  # برای تست
]
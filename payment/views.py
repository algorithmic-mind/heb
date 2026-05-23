import requests
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from course.models import Course
from .models import Payment, CourseEnrollment


@login_required
def payment_request(request, course_id):
    """ارسال درخواست پرداخت برای دوره مشخص"""
    course = get_object_or_404(Course, id=course_id, status='published')
    
    # بررسی اینکه کاربر قبلاً این دوره را خریداری کرده باشد
    if CourseEnrollment.objects.filter(user=request.user, course=course, is_active=True).exists():
        messages.warning(request, 'شما قبلاً این دوره را خریداری کرده‌اید.')
        return redirect('course:course_detail', slug=course.slug)
    
    # بررسی وجود قیمت برای دوره
    if not hasattr(course, 'price') or course.price <= 0:
        messages.error(request, 'این دوره رایگان است یا قیمت تعریف نشده.')
        return redirect('course:course_detail', slug=course.slug)
    
    amount = course.price  # قیمت دوره
    
    # ایجاد رکورد پرداخت
    payment = Payment.objects.create(
        user=request.user,
        course=course,
        amount=amount,
        status='pending',
        description=f'خرید دوره {course.title}'
    )
    
    req_data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": amount,
        "description": f"خرید دوره: {course.title}",
        "callback_url": settings.ZARINPAL_CALLBACK_URL,
        "metadata": {"course_id": course.id, "payment_id": payment.id}
    }
    req_header = {"accept": "application/json", "content-type": "application/json"}

    try:
        res = requests.post(
            settings.ZARINPAL_REQUEST_URL,
            json=req_data,
            headers=req_header,
            timeout=10
        )
        data = res.json()

        if "data" in data and "code" in data["data"]:
            if data["data"]["code"] == 100:
                authority = data["data"]["authority"]
                # ذخیره authority در پرداخت
                payment.authority = authority
                payment.save()
                
                return redirect(f"{settings.ZARINPAL_STARTPAY}{authority}")
            else:
                payment.status = 'failed'
                payment.save()
                messages.error(request, f"خطا در ایجاد پرداخت: کد {data['data']['code']}")
                return redirect('payment:error')
        elif "errors" in data:
            payment.status = 'failed'
            payment.save()
            messages.error(request, f"خطا: {data['errors']['message']}")
            return redirect('payment:error')
        else:
            payment.status = 'failed'
            payment.save()
            messages.error(request, "پاسخ نامعتبر از زرین‌پال دریافت شد.")
            return redirect('payment:error')
            
    except requests.exceptions.RequestException as e:
        payment.status = 'failed'
        payment.save()
        messages.error(request, "خطا در برقراری ارتباط با درگاه پرداخت.")
        return redirect('payment:error')


def payment_verify(request):
    """تایید پرداخت بعد از بازگشت کاربر از زرین‌پال"""
    authority = request.GET.get("Authority")
    status = request.GET.get("Status")
    
    if not authority:
        messages.error(request, "کد Authority یافت نشد.")
        return redirect('payment:error')

    try:
        # پیدا کردن پرداخت مربوطه
        payment = Payment.objects.get(authority=authority)
    except Payment.DoesNotExist:
        messages.error(request, "پرداخت مورد نظر یافت نشد.")
        return redirect('payment:error')

    if status != "OK":
        payment.status = 'cancelled'
        payment.save()
        messages.info(request, "پرداخت توسط کاربر لغو شد.")
        return redirect('payment:cancel')

    req_data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": payment.amount,
        "authority": authority,
    }
    req_header = {"accept": "application/json", "content-type": "application/json"}

    try:
        res = requests.post(
            settings.ZARINPAL_VERIFY_URL,
            json=req_data,
            headers=req_header,
            timeout=10
        )
        data = res.json()

        if "data" in data and "code" in data["data"]:
            if data["data"]["code"] == 100:
                # پرداخت موفق
                payment.status = 'successful'
                payment.ref_id = data["data"]["ref_id"]
                payment.verified_at = timezone.now()
                payment.save()
                
                # ثبت‌نام کاربر در دوره
                enrollment, created = CourseEnrollment.objects.get_or_create(
                    user=payment.user,
                    course=payment.course,
                    defaults={'payment': payment}
                )
                
                if created:
                    messages.success(request, f"پرداخت با موفقیت انجام شد. شما در دوره {payment.course.title} ثبت‌نام شدید.")
                else:
                    messages.info(request, "شما قبلاً در این دوره ثبت‌نام کرده‌اید.")
                
                return redirect('payment:success')
            else:
                payment.status = 'failed'
                payment.save()
                messages.error(request, f"پرداخت ناموفق - کد خطا: {data['data']['code']}")
                return redirect('payment:error')
        elif "errors" in data:
            payment.status = 'failed'
            payment.save()
            messages.error(request, f"خطا در تایید پرداخت: {data['errors']['message']}")
            return redirect('payment:error')
        else:
            payment.status = 'failed'
            payment.save()
            messages.error(request, "پاسخ نامعتبر از زرین‌پال دریافت شد.")
            return redirect('payment:error')
            
    except requests.exceptions.RequestException as e:
        payment.status = 'failed'
        payment.save()
        messages.error(request, "خطا در برقراری ارتباط با درگاه پرداخت.")
        return redirect('payment:error')


def payment_error(request):
    return render(request, 'payment/error.html')


def payment_success(request):
    return render(request, 'payment/success.html')


def payment_cancel(request):
    return render(request, 'payment/cancel.html')


@login_required
def my_payments(request):
    """نمایش تاریخچه پرداخت‌های کاربر"""
    payments = Payment.objects.filter(user=request.user).select_related('course')
    return render(request, 'payment/my_payments.html', {'payments': payments})


@login_required
def my_courses(request):
    """نمایش دوره‌های خریداری شده توسط کاربر"""
    enrollments = CourseEnrollment.objects.filter(
        user=request.user, 
        is_active=True
    ).select_related('course', 'payment')
    return render(request, 'payment/my_courses.html', {'enrollments': enrollments})


@login_required
def test_payment_request(request, course_id):
    """تست ساده برای دیباگ"""
    from django.http import JsonResponse
    
    try:
        course = get_object_or_404(Course, id=course_id)
        
        response_data = {
            'course_id': course.id,
            'course_title': course.title,
            'course_status': course.status,
            'has_price_attr': hasattr(course, 'price'),
            'user': request.user.username,
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'callback_url': settings.ZARINPAL_CALLBACK_URL,
            'request_url': settings.ZARINPAL_REQUEST_URL,
            'sandbox_mode': getattr(settings, 'SANDBOX', None),
        }
        
        # بررسی فیلد قیمت
        if hasattr(course, 'price'):
            response_data['course_price'] = str(course.price)
            response_data['price_type'] = type(course.price).__name__
            
        if hasattr(course, 'get_final_price'):
            try:
                response_data['final_price'] = course.get_final_price()
            except Exception as e:
                response_data['final_price_error'] = str(e)
        
        # بررسی CourseEnrollment
        enrolled = CourseEnrollment.objects.filter(user=request.user, course=course, is_active=True).exists()
        response_data['already_enrolled'] = enrolled
        
        # تست اتصال به زرین‌پال
        test_data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": 1000,  # مبلغ تست
            "description": "تست اتصال",
            "callback_url": settings.ZARINPAL_CALLBACK_URL,
        }
        
        try:
            import requests
            test_response = requests.post(
                settings.ZARINPAL_REQUEST_URL,
                json=test_data,
                headers={"accept": "application/json", "content-type": "application/json"},
                timeout=10
            )
            
            response_data['zarinpal_test'] = {
                'status_code': test_response.status_code,
                'response': test_response.text[:500]  # فقط 500 کاراکتر اول
            }
            
        except Exception as e:
            response_data['zarinpal_test'] = {
                'error': str(e)
            }
        
        return JsonResponse(response_data, json_dumps_params={'indent': 2})
        
    except Exception as e:
        return JsonResponse({'error': str(e), 'error_type': type(e).__name__})
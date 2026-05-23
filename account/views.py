from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
import re
from .models import SMSOTP, Profile
from .utils import generate_otp_for_user
from django.utils import timezone
# Create your views here.

class Login(View):

    #@method_decorator(ratelimit(key='user_or_ip', rate='3/m'))
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account:dashboard')
        return render(request, "authentication/login.html")

    #@method_decorator(ratelimit(key='user_or_ip', rate='2/m'))
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('account:dashboard')

        phone = request.POST.get('phone', '').strip()
        
        # اعتبارسنجی شماره موبایل
        if not phone:
           
            return HttpResponse("<div class='alert alert-danger rounded-4'><small>شماره موبایل را وارد کنید!</small></div>")
        
        # بررسی فرمت شماره موبایل ایران
        phone_pattern = r'^09\d{9}$'
        if not re.match(phone_pattern, phone):
            return HttpResponse("<div class='alert alert-danger rounded-4'><small>شماره موبایل نامعتبر!</small></div>")

        try:
            # ارسال کد تایید
            otp_result = generate_otp_for_user(phone=phone)
            
            if otp_result:  # اگر ارسال موفق بود
                # ذخیره شماره موبایل در session
                request.session['phone_for_otp'] = phone
                request.session['otp_sent_time'] = timezone.now().isoformat()
                
                return HttpResponse('''<div class='alert alert-success rounded-4'><small>در حال ارسال کد...</small></div><script>setTimeout(function() {
    window.location.href = "/account/login/verify";
}, 3000);</script>''')
            else:
               return HttpResponse("<div class='alert alert-danger rounded-4'><small>خطا در ارسال کد. مجدد امتحان کنید!</small></div>")
                
        except Exception as e:
            return HttpResponse("<div class='alert alert-danger rounded-4'><small>خطا در ارسال کد. مجدد امتحان کنید!</small></div>")




class VerifyOTP(View):
    
    #@method_decorator(ratelimit(key='user_or_ip', rate='5/m'))
    def get(self, request):
        # بررسی وجود شماره موبایل در session
        if 'phone_for_otp' not in request.session:
            return redirect('account:login')
        
        # بررسی زمان انقضا (مثلاً 5 دقیقه)
        if not self._is_otp_valid_time(request):
            self._clear_otp_session(request)
            return redirect('account:login')
        
        phone = request.session.get('phone_for_otp')
        return render(request, "authentication/verify.html", {
            'phone': phone,
            'masked_phone': self._mask_phone(phone)
        })

    def post(self, request):
        # بررسی session
        if 'phone_for_otp' not in request.session:
            return redirect('account:login')
        

        c_1 = request.POST.get('c_1', '').strip()
        c_2 = request.POST.get('c_2', '').strip()
        c_3 = request.POST.get('c_3', '').strip()
        c_4 = request.POST.get('c_4', '').strip()
        phone = request.session.get('phone_for_otp')
        otp_code = c_1 + c_2 + c_3 + c_4
        
        # اعتبارسنجی کد
        if not otp_code or len(otp_code) != 4: 
            return HttpResponse("<div class='alert alert-danger rounded-4'><small>کد نامعتبر</small></div>")
        
        try:
            # بررسی کد OTP
            if SMSOTP.objects.filter(phone=phone, code=otp_code).first():
                # پاک کردن session
                self._clear_otp_session(request)
                
                # لاگین کاربر یا ایجاد حساب جدید
                user = self._get_or_create_user(phone)
                if user:
                    login(request, user)
                    
                    # هدایت مناسب بر اساس نوع کاربر
                    if user.is_staff:
                        redirect_url = '''<div class='alert alert-success rounded-4'><small>ورود موفق! در حال هدایت به داشبورد...</small></div><script>setTimeout(function() {
    window.location.href = "/admin";
}, 3000);</script>'''
                    else:
                        redirect_url = '''<div class='alert alert-success rounded-4'><small>ورود موفق! در حال هدایت به داشبورد...</small></div><script>setTimeout(function() {
    window.location.href = "/account/dashboard";
}, 3000);</script>'''
                    
                    return HttpResponse(redirect_url)
               
            else:
                return HttpResponse("<div class='alert alert-danger rounded-4'><small>کد تایید صحیح نمی‌باشد!</small></div>")
                
        except Exception as e:
             return HttpResponse("<div class='alert alert-danger rounded-4'><small>خطا در عملیات ورود یا ساخت حساب!</small></div>")
    
    def _is_otp_valid_time(self, request):
        """بررسی معتبر بودن زمان OTP (5 دقیقه)"""
        
        from datetime import timedelta
        
        otp_time_str = request.session.get('otp_sent_time')
        if not otp_time_str:
            return False
        
        try:
            otp_time = timezone.datetime.fromisoformat(otp_time_str)
            current_time = timezone.now()
            return (current_time - otp_time) < timedelta(minutes=5)
        except:
            return False
    
    def _clear_otp_session(self, request):
        """پاک کردن اطلاعات OTP از session"""
        request.session.pop('phone_for_otp', None)
        request.session.pop('otp_sent_time', None)
    
    def _mask_phone(self, phone):
        """ماسک کردن شماره موبایل برای نمایش"""
        if len(phone) >= 7:
            return phone[:4] + '***' + phone[-3:]
        return phone
    
    def _get_or_create_user(self, phone):
        
        try:
            # جستجو بر اساس username (شماره موبایل)
            user = User.objects.filter(username=phone).first()
            
            if not user:
                # ایجاد کاربر جدید
                user = User.objects.create_user(
                    username=phone,
                    first_name='',
                    last_name='',
                    is_active=True
                )

                
            return user
        except Exception as e:
            return None
        

       


    


def logout_view(request):

    logout(request)
    return redirect('main:index')



def dashboard(request):
    if not request.user.is_authenticated:
            return redirect('account:login')
    return render(request,'authentication/dashboard.html')


def change_information(request):

    fname = request.POST.get('firstName', '').strip()
    lname = request.POST.get('lastName', '').strip()
    user = User.objects.get(pk=request.user.id)
    user.first_name = fname
    user.last_name = lname
    user.save()

    return HttpResponse("<script>location.reload();</script> تغییرات ذخیره شد")
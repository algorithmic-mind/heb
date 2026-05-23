from django import template
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

register = template.Library()

@register.filter
def timesince_fa(value):
    """
    نمایش تاریخ به صورت نسبی به زبان فارسی
    مثال: ۲ روز پیش، ۱ ماه پیش، ۱ سال پیش
    """
    if not value:
        return ""
    
    now = timezone.now()
    diff = now - value
    
    # تبدیل به ثانیه
    seconds = diff.total_seconds()
    
    # محاسبه واحدهای زمانی
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    months = days // 30
    years = days // 365
    
    if years > 0:
        return f"{int(years)} سال پیش"
    elif months > 0:
        return f"{int(months)} ماه پیش"
    elif days > 0:
        return f"{int(days)} روز پیش"
    elif hours > 0:
        return f"{int(hours)} ساعت پیش"
    elif minutes > 0:
        return f"{int(minutes)} دقیقه پیش"
    else:
        return "همین الان"
    




@register.filter
def persian_price_format(value):
    """
    تبدیل قیمت به فرمت فارسی: ۱,۸۰۰,۰۰۰ تومان
    """
    if value is None:
        return "رایگان"
    
    try:
        # تبدیل به عدد
        price = int(value)
        
        if price == 0:
            return "رایگان"
        
        # تبدیل به رشته و جدا کردن با کاما
        price_str = f"{price:,}"
        
        # جایگزینی کاما با ویرگول فارسی
        persian_price = price_str.replace(',', '،')
        
        # تبدیل اعداد انگلیسی به فارسی
        persian_digits = {
            '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
            '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
        }
        
        for eng, per in persian_digits.items():
            persian_price = persian_price.replace(eng, per)
        
        return f"{persian_price} تومان"
        
    except (ValueError, TypeError):
        return "رایگان"
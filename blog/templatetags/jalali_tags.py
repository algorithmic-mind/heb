# blog/templatetags/jalali_tags.py
from django import template
import jdatetime

register = template.Library()

@register.filter
def jalali_date(value):
    """تبدیل تاریخ میلادی به شمسی کامل فارسی"""
    if not value:
        return ""
    
    # تبدیل تاریخ میلادی به شمسی
    if hasattr(value, 'date'):
        jalali_date = jdatetime.date.fromgregorian(date=value.date())
    else:
        jalali_date = jdatetime.date.fromgregorian(date=value)
    
    # نام ماه‌های فارسی
    persian_months = {
        1: 'فروردین', 2: 'اردیبهشت', 3: 'خرداد',
        4: 'تیر', 5: 'مرداد', 6: 'شهریور', 
        7: 'مهر', 8: 'آبان', 9: 'آذر',
        10: 'دی', 11: 'بهمن', 12: 'اسفند'
    }
    
    # تبدیل ارقام انگلیسی به فارسی
    def to_persian_digits(text):
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        english_digits = '0123456789'
        for eng, per in zip(english_digits, persian_digits):
            text = text.replace(eng, per)
        return text
    
    day = to_persian_digits(str(jalali_date.day))
    month = persian_months[jalali_date.month]
    year = to_persian_digits(str(jalali_date.year))
    
    return f"{day} {month} {year}"

@register.filter  
def jalali_short(value):
    """فرمت کوتاه: ۱۴۰۴/۰۵/۲۴"""
    if not value:
        return ""
        
    if hasattr(value, 'date'):
        jalali_date = jdatetime.date.fromgregorian(date=value.date())
    else:
        jalali_date = jdatetime.date.fromgregorian(date=value)
    
    def to_persian_digits(text):
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        english_digits = '0123456789'
        for eng, per in zip(english_digits, persian_digits):
            text = text.replace(eng, per)
        return text
    
    formatted_date = f"{jalali_date.year:04d}/{jalali_date.month:02d}/{jalali_date.day:02d}"
    return to_persian_digits(formatted_date)
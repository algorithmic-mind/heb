# utils.py یا هر جای دیگر
from random import randint
from django.utils import timezone
from datetime import timedelta
from .models import SMSOTP
from sms_ir import SmsIr

sms_ir = SmsIr("tf4HuCeqQfMEJopjE7gmmk63t63JMtOkCXdnhVQ4HPAB5Mx9")


def send_otp_sms(number,code):

    sms_ir.send_verify_code(
        number=number,
        template_id=831888,
        parameters=[
                        {
                            "name" : "CODE",
                            "value": str(code),
            
                        },
                        
                    ],
    )





def generate_otp_for_user(phone):
    otp_code = str(randint(1001, 9999))
    expires_at = timezone.now() + timedelta(minutes=5)  # ۵ دقیقه اعتبار

    # حذف OTPهای قبلی
    SMSOTP.objects.filter(phone=phone).delete()

    otp = SMSOTP.objects.create(
        phone=phone,
        code=otp_code,
        expires_at=expires_at
    )

    send_otp_sms(phone, otp_code)
    return otp_code
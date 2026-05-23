from sms_ir import SmsIr

sms_ir = SmsIr("tf4HuCeqQfMEJopjE7gmmk63t63JMtOkCXdnhVQ4HPAB5Mx9")


def send_otp(number,code):

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
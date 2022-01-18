from django.core.mail import EmailMessage
import random
import math
import string


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']],
        )
        email.send()

    @staticmethod
    def generate_otp(OTP):
        digits = "0123456789"
        OTP = ""
        for i in range(4):
            OTP += digits[math.floor(random.random() * 10)]
        return OTP

    @staticmethod
    def create_account_number(num):
        return '207' + ''.join(random.choice(string.digits) for i in range(num))

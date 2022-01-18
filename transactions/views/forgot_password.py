from rest_framework import generics, status
from serializers import ForgotPasswordSerializer
from ..models import User
from rest_framework.response import Response
from ..utils import Util
from django.core.exceptions import ObjectDoesNotExist


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        OTP = Util.generate_otp(6)
        user.otp = OTP
        email = user.email
        user.save()
        if user.is_active:
            email_body = 'Hi ' + user.username + ' Here is your Otp code to reset your password ' + str(OTP)
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'verify your email'}
            Util.send_email(data)
            return Response({
                "Success": "Check Email for otp code for password reset",
            }, status=status.HTTP_200_OK)

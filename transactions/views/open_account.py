from rest_framework import generics, status
from transactions.models import AccountDetails, User
from serializers import CreateAccountSerializer
from ..utils import Util
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CreateAccountView(generics.GenericAPIView):
    serializer_class = CreateAccountSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(email=request.user.email)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            fullname = serializer.validated_data['fullname']
            account_type = serializer.validated_data['account_type']
            account_number = Util.create_account_number(6)
            age = serializer.validated_data['age']
            employment_status = serializer.validated_data['employment_status']
            try:
                account_creation = AccountDetails.objects.create(
                    user_id=user,
                    fullname=fullname,
                    account_type=account_type,
                    account_number=account_number,
                    age=age,
                    employment_status=employment_status,
                )
                return Response(data={'success': f'Account successfully created,'
                                                 f' your {account_type}'
                                                 f' number is {account_creation.account_number}'},
                                status=status.HTTP_202_ACCEPTED)

            except Exception as error:
                return Response(data={'error': error}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'error': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)

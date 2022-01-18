from rest_framework import generics, status
from rest_framework.response import Response
from ..utils import Util
from ..models import User, UserBalance, AccountDetails
from serializers import AccountBalanceSerializer
from transactions.permissions import IsAdmin


class CreditBalanceView(generics.GenericAPIView):
    serializer_class = AccountBalanceSerializer
    permissions_classes = [IsAdmin]
    queryset = User.objects.all()

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(pk=pk)
        user_id = User.objects.get(email=user.email)
        balance = UserBalance.objects.filter(user=user).first()
        if balance:
            credit_account = serializer.validated_data['account_balance']
            balance.account_balance += credit_account
            balance.save()

            credit_amount = str(credit_account)
            email_body = f'Hi {user.username} your account has been credited with {credit_amount}'
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'credit alert'}
            Util.send_email(data)
            return Response({'success': f'The chosen account has been successfully credited with {credit_amount}'},
                            status=status.HTTP_200_OK)
        else:
            account = AccountDetails.objects.get(user_id=user_id)
            balance = UserBalance.objects.create(
                user=user,
                user_account=account,
                account_balance=0,
            )
            credit_account = serializer.validated_data['account_balance']
            balance.account_balance += credit_account
            balance.save()

            credit_amount = str(credit_account)
            email_body = f'Hi {user.username} your account has been credited with {credit_amount}'
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'credit alert'}
            Util.send_email(data)
            return Response({'success': f'The chosen account has been successfully credited with {credit_amount}'},
                            status=status.HTTP_200_OK)


class DebitBalanceView(generics.GenericAPIView):
    serializer_class = AccountBalanceSerializer
    queryset = User.objects.all()
    permissions_classes = [IsAdmin]

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(pk=pk)
        user_id = User.objects.get(email=user.email)
        balance = UserBalance.objects.filter(user=user).first()
        if balance:
            debit_account = serializer.validated_data['account_balance']
            if balance.account_balance >= debit_account:
                balance.account_balance -= debit_account
                balance.save()

                debit_amount = str(debit_account)
                email_body = f'Hi {user.username} your account has been credited with {debit_amount}'
                data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'debit alert'}
                Util.send_email(data)
                return Response({'success': f'The chosen account has been successfully credited with {debit_amount}'},
                                status=status.HTTP_200_OK)
            else:
                balance.account_balance = balance.account_balance
                balance.save()
                return Response({'Error': f'You account balance '
                                          f'{balance.account_balance} is not enough to make this transaction'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            account = AccountDetails.objects.get(user_id=user_id)
            balance = UserBalance.objects.create(
                user=user,
                user_account=account,
                account_balance=0
            )
            debit_account = serializer.validated_data['account_balance']
            balance.account_balance = balance.account_balance
            balance.save()

            return Response({'Error': f'You account balance '
                                      f'{balance.account_balance} is not enough to make this transaction'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

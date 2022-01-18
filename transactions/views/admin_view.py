from transactions.models import User
from transactions.models import AccountDetails
from rest_framework import status, generics
from serializers import CreateAccountSerializer
from rest_framework.response import Response
from transactions.permissions import IsAdmin
from django.http import Http404


class DeleteView(generics.GenericAPIView):
    permissions_classes = [IsAdmin]
    serializer_class = CreateAccountSerializer
    queryset = User.objects.all()

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({'success': 'successfully deleted'}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)


class DeactivateView(generics.GenericAPIView):
    serializer_class = CreateAccountSerializer
    permissions_classes = [IsAdmin]
    queryset = User.objects.all()

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_verified = False
            user.save()
            return Response({'success': 'successfully deactivated'}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(generics.GenericAPIView):
    serializer_class = CreateAccountSerializer
    permissions_classes = [IsAdmin]
    queryset = User.objects.all()

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_verified = True
            user.save()
            return Response({'success': 'successfully activated'}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)


class AccountListView(generics.GenericAPIView):
    permissions_classes = [IsAdmin]
    queryset = AccountDetails.objects.all()

    def get(self, request):
        account = AccountDetails.objects.all()
        serializer = CreateAccountSerializer(account, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountDetailView(generics.GenericAPIView):
    permissions_classes = [IsAdmin]

    def get_object(self, pk=None):
        try:
            account = AccountDetails.objects.get(pk=pk)
            return account
        except AccountDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        account = self.get_object(pk=pk)
        serializer = CreateAccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

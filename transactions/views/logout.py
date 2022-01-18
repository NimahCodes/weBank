from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import logout


class LogoutView(generics.GenericAPIView):
    def get(self, request):
        logout(request)
        return Response(data={'success': "You've successfully Logged out"}, status=status.HTTP_200_OK)

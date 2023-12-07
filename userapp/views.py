from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

from django.contrib.auth import login, authenticate

class AuthUserApiView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        username_or_email = request.data['username_or_email']
        password = request.data['password']

        if '@' in username_or_email:
            user = authenticate(email=username_or_email, password=password)
        else:
            user = authenticate(username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            data = {'message': 'Welcome!'}
            return Response(data, HTTP_200_OK)
        else:
            data = {'message': 'Username or/and Password is not valid!'}
            return Response(data, HTTP_403_FORBIDDEN)



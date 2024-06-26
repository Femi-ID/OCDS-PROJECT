# from django.shortcuts import render
# from rest_framework.request import Request
# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.response import Response
# from .serializers import CustomTokenSerializer
# from .models import User
# from rest_framework import generics
# from rest_framework_simplejwt.views import TokenObtainPairView


# # Unimportant but anyways: View to add user-data to the /jwt/create route
# class CustomToken(TokenObtainPairView):
#     serializer_class = CustomTokenSerializer

#     def post(self, request: Request, *args, **kwargs) -> Response:
#         try:
#             user = User.objects.get(email=request.data.get('username'))
#             # .exists()
#         except User.DoesNotExist:
#             return Response({'error': 'Invalid email or password inputted.'}, 
#                                 status=status.HTTP_400_BAD_REQUEST)

#         return super().post(request, *args, **kwargs)


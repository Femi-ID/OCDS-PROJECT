from .models import User
from .serializers import CreateAdminUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CreateAdminUser(APIView):
    # def get(self):

    def post(self, request):
        user = User.objects.filter(email=request.data['email'])
        # user_email = []
        # for user in users:
        #     user_email.append([user.email])

        if user:
            return Response({'error': 'User email already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateAdminUserSerializer(data=request.data)
        if serializer.is_valid():
            # user.user_type 
            serializer.save(user_type='admin')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render
from itertools import product
from unicodedata import category
from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions, mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import User, ThongBao, Role, Lop, TinTuc
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from rest_framework import status
from django.http import JsonResponse
import random
from .serializers import UserSerializers, ThongBaoSerializers, LopSerializers, TinTucSerializers
# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializers
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current-user", detail=False)
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def register_user(self, request):
        username = request.data.get('username', None)
        if not username:
            return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is not unique.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThongBaoViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = ThongBao.objects.all()
    serializer_class = ThongBaoSerializers
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False, url_path='thong-bao')
    def get_queryset(self):
        user = self.request.user
        if user.role == Role.Teacher.value:
            return self.queryset.filter(sender=user)
        else:
            return self.queryset.filter(recipients=user)




@api_view(['POST'])
def send_otp(request):
    email = request.data.get('email')

    if email:
        otp = random.randint(100000, 999999)
        message = f"Your OTP is: {otp}"


        send_mail('OTP for Password Reset', message, 'your_email@example.com', [email])
        try:
            user = User.objects.get(email=email)
            user.otp = otp
            user.save()
        except User.DoesNotExist:
            pass  # Người dùng không tồn tại, không lưu mã OTP
        return Response({'message': 'OTP has been sent successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid email.'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def verify_otp(request):
    username = request.data.get('username')
    otp = request.data.get('otp')
    new_password = request.data.get('password')

    try:
        # Kiểm tra OTP và đổi mật khẩu
        user = User.objects.get(username=username)
        if user.otp == otp:
            # Xác thực OTP thành công, cập nhật mật khẩu mới
            user.set_password(new_password)
            user.otp = None
            user.save()


            return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        else:
            # OTP không hợp lệ
            return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        # Người dùng không tồn tại
        return Response({'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class TinTucViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = TinTuc.objects.all()
    serializer_class = TinTucSerializers
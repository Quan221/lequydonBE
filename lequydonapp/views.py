from django.shortcuts import render
from itertools import product
from unicodedata import category
from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions, mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import User, ThongBao, Role, Lop, TinTuc, OTP, ChatMessage, DonTuyenSinh, Quan, QuanvaPhuong, Phuong, DaHocHetLop5, TruongVaQuan, Truong, DangKyHoc
from django.db.models import OuterRef, Subquery
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from rest_framework import status
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import random
from django.shortcuts import get_object_or_404
from .serializers import UserSerializers, ThongBaoSerializers, LopSerializers, TinTucSerializers, MessageSerializers, PhuongSerializers, DonTuyenSinhSerializers, QuanSerializers, TrinhDoSerializers, TruongSerializers, DangKyHocSerializers
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

class MyInbox(generics.ListAPIView):
    serializer_class = MessageSerializers
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user_id = self.kwargs['user_id']

        messages = ChatMessage.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sender__reciever=user_id) |
                    Q(reciever__sender=user_id)
                ).distinct().annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), reciever=user_id) |
                            Q(reciever=OuterRef('id'), sender=user_id)
                        ).order_by('-id')[:1].values_list('id', flat=True)
                    )
                ).values_list('last_msg', flat=True).order_by("-id")
            )
        ).order_by("-id")

        return messages


class GetMessages( generics.ListAPIView):
    serializer_class = MessageSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        reciever_id = self.kwargs['reciever_id']
        messages = ChatMessage.objects.filter(sender__in=[sender_id, reciever_id],
                                              reciever__in=[sender_id, reciever_id])
        return messages


class SendMessages(generics.CreateAPIView):
    serializer_class = MessageSerializers
    permission_classes = [permissions.IsAuthenticated]


class SearchUser( generics.ListAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        logged_in_user = self.request.user
        users = User.objects.filter(Q(user__username__icontains=username) | Q(first_name__icontains=username) | Q(user__email__icontains=username) &
                                       ~Q(user=logged_in_user))

        if not users.exists():
            return Response(
                {"detail": "No users found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

class QuanViewSet(viewsets.ViewSet, generics.ListAPIView):
        queryset = Quan.objects.all()
        serializer_class = QuanSerializers

        @action(methods=['get'], detail=True, url_path='phuong')
        def get_phuong(self, request, pk):
            phuong = Phuong.objects.filter(quanvaphuong__quan_id=pk)

            return Response(PhuongSerializers(phuong, many=True, context={"request": request}).data,
                            status=status.HTTP_200_OK)

        @action(methods=['get'], detail=True, url_path='truong')
        def get_truong(self, request, pk):
            truong = Truong.objects.filter(truongvaquan__quan_id=pk)

            return Response(TruongSerializers(truong, many=True, context={"request": request}).data,
                            status=status.HTTP_200_OK)


class DonTuyenSinhViewSet(viewsets.ViewSet, generics.CreateAPIView):
    serializer_class = DonTuyenSinhSerializers


class TrinhDoViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DaHocHetLop5.objects.all()
    serializer_class = TrinhDoSerializers


class DangKyHocViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DangKyHoc.objects.all()
    serializer_class = DangKyHocSerializers

class LopViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Lop.objects.all()
    serializer_class = LopSerializers
@api_view(['POST'])
def check_otp(request):
        otp = request.data.get('otp')

        try:
            otp_instance = OTP.objects.get(otp=otp)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'OTP không hợp lệ'}, status=400)

        if otp_instance.is_used:
            return JsonResponse({'message': 'OTP đã được sử dụng'}, status=400)

        # Xác thực người dùng (ví dụ: JWT authentication)
        # ...

        # # Tạo đơn tuyển sinh
        # application = DonTuyenSinh.objects.create()

        # Cập nhật trạng thái OTP đã được sử dụng
        otp_instance.is_used = True
        otp_instance.save()

        return JsonResponse({'message': 'OTP đúng.'})

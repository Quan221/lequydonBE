from django.urls import path, include
from . import views
from rest_framework import routers
from .views import check_otp


router = routers.DefaultRouter()
router.register(prefix='users', viewset=views.UserViewSet, basename='user')
router.register(prefix='thongbao', viewset=views.ThongBaoViewSet, basename='thongbao')
router.register(prefix='tintuc', viewset=views.TinTucViewSet,basename='tintuc')
router.register('quan', viewset=views.QuanViewSet, basename='quan')
router.register('dontuyensinh', viewset=views.DonTuyenSinhViewSet, basename='dontuyensinh')
router.register('trinhdo', viewset=views.TrinhDoViewSet, basename='trinhdo')
router.register('dangkyhoc', viewset=views.DangKyHocViewSet, basename='dangkyhoc')
router.register('lop', viewset=views.LopViewSet, basename='lop')
# router.register(prefix='myInbox', viewset=views.MyInbox, basename='my-inbox')
# router.register(prefix='getMessage', viewset=views.GetMessages, basename='get-message')
# router.register(prefix='sendMessage', viewset=views.SendMessages, basename='send-message')
urlpatterns = [
    path('', include(router.urls)),
    path('api/send-otp/', views.send_otp),
    path('api/verify-otp/', views.verify_otp),
    path("my-inbox/<user_id>/", views.MyInbox.as_view()),
    path("get-messages/<sender_id>/<reciever_id>/", views.GetMessages.as_view()),
    path("send-messages/", views.SendMessages.as_view()),
    path("check-otp/", views.check_otp),
]
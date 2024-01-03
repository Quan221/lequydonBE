from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(prefix='users', viewset=views.UserViewSet, basename='user')
router.register(prefix='thongbao', viewset=views.ThongBaoViewSet, basename='thongbao')
router.register(prefix='tintuc', viewset=views.TinTucViewSet,basename='tintuc')

urlpatterns = [
    path('', include(router.urls)),
    path('api/send-otp/', views.send_otp),
    path('api/verify-otp/', views.verify_otp),
]
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import User, OTP, ThongBao, Lop, TinTuc, ChatMessage, DonTuyenSinh, Quan, QuanvaPhuong, Phuong, DaHocHetLop5, TruongVaQuan, Truong, DangKyHoc


class UserSerializers(serializers.ModelSerializer):
    avatar_path = serializers.SerializerMethodField()

    def get_avatar_path(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith("/static"):
            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'password', 'email',
                  'avatar', 'avatar_path', 'role', 'sdt', 'birthday', 'thuongtru']
        extra_kwargs = {
            'password': {
                'write_only': True
            }, ' avatar_path': {
                'read_only': True, 'avatar': {
                    'write_only': True
                }
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user

class ThongBaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ThongBao
        fields = '__all__'

class LopSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lop
        fields = '__all__'


class TinTucSerializers(serializers.ModelSerializer):
    class Meta:
        model = TinTuc
        fields= '__all__'


class MessageSerializers(serializers.ModelSerializer):
    reciever_profile = UserSerializers(read_only=True)
    sender_profile = UserSerializers(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'sender', 'reciever', 'reciever_profile', 'sender_profile', 'message', 'is_read', 'date']

    def __init__(self, *args, **kwargs):
        super(MessageSerializers, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2
class QuanSerializers(serializers.ModelSerializer):
    class Meta:
        model = Quan
        fields = '__all__'

class QuanvaPhuongSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuanvaPhuong
        fields = '__all__'

class PhuongSerializers(serializers.ModelSerializer):
    class Meta:
        model = Phuong
        fields = '__all__'

class DonTuyenSinhSerializers(serializers.ModelSerializer):
    class Meta:
        model = DonTuyenSinh
        fields = '__all__'
        read_only_fields = ('id',)
class TrinhDoSerializers(serializers.ModelSerializer):
    class Meta:
        model = DaHocHetLop5
        fields = '__all__'
class DangKyHocSerializers(serializers.ModelSerializer):
    class Meta:
        model = DangKyHoc
        fields = '__all__'
class TruongVaQuanSerializers(serializers.ModelSerializer):
    class Meta:
        model = TruongVaQuan
        fields = '__all__'
class TruongSerializers(serializers.ModelSerializer):
    class Meta:
        model = Truong
        fields = '__all__'
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'
class LopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lop
        fields = '__all__'
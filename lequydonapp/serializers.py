from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import User, ThongBao, Lop, TinTuc


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
                  'avatar', 'avatar_path', 'role']
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

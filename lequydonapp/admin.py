from django.contrib import admin
from django.forms import fields
from django.template.response import TemplateResponse
from .models import User, ThongBao, Lop, OTP, TinTuc, ChatMessage,  Quan, Phuong, DonTuyenSinh, QuanvaPhuong , DaHocHetLop5, TruongVaQuan, Truong, DangKyHoc
from ckeditor.widgets import CKEditorWidget
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .actions import export_as_csv, export_to_excel
from django.utils.crypto import get_random_string
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name')
class ThongBaoAdmin(admin.ModelAdmin):
    filter_horizontal = ('recipients',)
    # Sử dụng filter_horizontal để hiển thị hộp chọn nhiều phần tử
class LopAdmin(admin.ModelAdmin):
    filter_horizontal = ('siso',)

class TinTucAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = TinTuc
        fields = '__all__'

class TinTucAdmin(admin.ModelAdmin):
    form = TinTucAdminForm
# Register your models here.


class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read', 'message']
    list_display = ['user', 'sender', 'reciever', 'is_read', 'message']
class MyModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DonTuyenSinh._meta.fields]
    actions = [export_to_excel]
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]
    actions = [export_to_excel]
class OTPAdmin(admin.ModelAdmin):
    readonly_fields = ('otp',)  # Không cho phép chỉnh sửa trường otp trong Django Admin
    list_display = ['otp', 'is_used']

    def save_model(self, request, obj, form, change):
        if not obj.otp:
            obj.otp = get_random_string(length=6, allowed_chars='0123456789')
        super().save_model(request, obj, form, change)

admin.site.register(User)
admin.site.register(ThongBao, ThongBaoAdmin)
admin.site.register(Lop, LopAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(TinTuc, TinTucAdmin)
admin.site.register(Quan)
admin.site.register(Phuong)
admin.site.register(DonTuyenSinh,MyModelAdmin)
admin.site.register(QuanvaPhuong)
admin.site.register(DaHocHetLop5)
admin.site.register(Truong)
admin.site.register(TruongVaQuan)
admin.site.register(DangKyHoc)
admin.site.register(OTP, OTPAdmin)
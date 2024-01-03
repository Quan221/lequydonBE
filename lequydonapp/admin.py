from django.contrib import admin
from django.forms import fields
from django.template.response import TemplateResponse
from .models import User, ThongBao, Lop, TinTuc
from ckeditor.widgets import CKEditorWidget
from django import forms


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name')
class ThongBaoAdmin(admin.ModelAdmin):
    filter_horizontal = ('recipients',)
    # Sử dụng filter_horizontal để hiển thị hộp chọn nhiều phần tử
class LopAdmin(admin.ModelAdmin):
    filter_horizontal = ('siso',)

class TinTucAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = TinTuc
        fields = '__all__'

class TinTucAdmin(admin.ModelAdmin):
    form = TinTucAdminForm
# Register your models here.
admin.site.register(User)
admin.site.register(ThongBao, ThongBaoAdmin)
admin.site.register(Lop, LopAdmin)
admin.site.register(TinTuc, TinTucAdmin)
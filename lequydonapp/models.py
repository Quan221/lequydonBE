from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import  Enum
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
# Create your models here.
class Role(Enum):
    Student = 'Student'
    Teacher = 'Teacher'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m', blank=True)
    role = models.CharField(
        max_length=50, choices=Role.choices(), default=Role.Student.value)
    otp = models.CharField(max_length=6, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    thuongtru = models.CharField(max_length=200,blank=True, null=True)
    sdt = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return f"{self.first_name} ({self.username})"

class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ThongBao(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications")
    recipients = models.ManyToManyField(User, related_name="received_notifications")
    tieude = models.CharField(max_length=200)
    noidung = models.CharField(max_length=200)
    updated_date = models.DateTimeField(auto_now=True)


class Lop(models.Model):
    lop = models.CharField(max_length=200)
    siso = models.ManyToManyField(User)


class TinTuc(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()

    def __str__(self):
        return self.title
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')
    message = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['date']
        verbose_name_plural = "Message"

    def __str__(self):
        return f"{self.sender} - {self.reciever}: {self.message}"

    @property
    def sender_profile(self):
        sender_profile = User.objects.get(user=self.sender)
        return sender_profile

    @property
    def reciever_profile(self):
        reciever_profile = User.objects.get(user=self.reciever)
        return reciever_profile

class Quan(models.Model):
    name = models.CharField(max_length=100,
                            unique=True)

    def __str__(self):
        return self.name

class Phuong(models.Model):
    name = models.CharField(max_length=100, unique=True)




    def __str__(self):
        return self.name

class QuanvaPhuong(models.Model):
    quan = models.ForeignKey(Quan, on_delete=models.CASCADE)
    phuong = models.ForeignKey(Phuong, on_delete=models.CASCADE)
class DaHocHetLop5(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Truong(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class TruongVaQuan(models.Model):
    truong = models.ForeignKey(Truong, on_delete=models.CASCADE)
    quan = models.ForeignKey(Quan, on_delete=models.CASCADE)
class DangKyHoc(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return  self.name
class OTP(models.Model):
    otp = models.CharField(max_length=6, unique=True)
    is_used = models.BooleanField(default=False)


class DonTuyenSinh(models.Model):
    ten = models.CharField(max_length=100, unique=False)
    sdt = models.CharField(max_length=100,null=False)
    hokhau = models.CharField(max_length=100)
    choDK = models.CharField(max_length=100)
    cccd = models.IntegerField()
    is_parent = models.CharField(max_length=100)
    trinhdo = models.ForeignKey(DaHocHetLop5, on_delete=models.CASCADE)
    truongtieuhoc = models.CharField(max_length=100)
    tenhs = models.CharField(max_length=100)
    ngaysinh = models.DateField(auto_now=True)
    gioitinh = models.CharField(max_length=100)
    dantoc = models.CharField(max_length=100)
    tongiao = models.CharField(max_length=100)
    noisinh = models.CharField(max_length=100)
    madinhdanh = models.CharField(max_length=100)
    diachi = models.CharField(max_length=100, unique=False)
    quan = models.ForeignKey(Quan, on_delete=models.CASCADE)
    phuong = models.CharField(max_length=100)
    diachithuongtru = models.CharField(max_length=100)
    quanthuongtru = models.CharField(max_length=100)
    phuongthuongtru = models.CharField(max_length=100)
    dienchinhsach = models.CharField(max_length=100, null=True)
    suckhoe = models.CharField(max_length=100)
    tiengviet5 = models.FloatField(max_length=100)
    toan5 = models.FloatField(max_length=100)
    tongdiem = models.FloatField()
    chungchita = models.CharField(max_length=100)
    cambridge = models.IntegerField(null=True)
    toefl = models.IntegerField(null=True)
    pearson = models.FloatField(null=True)
    hocba = models.CharField(max_length=100)
    boi = models.CharField(max_length=100)
    nangkhieu = models.CharField(max_length=100,null=True)
    tdtt = models.CharField(max_length=100, null=True)
    tntp = models.CharField(max_length=100, null=True)
    tencha = models.CharField(max_length=100)
    namsinhcha = models.IntegerField()
    nghenghiep = models.CharField(max_length=100)
    chucvu = models.CharField(max_length=100)
    noicongtac = models.CharField(max_length=100)
    sdtcha = models.IntegerField()
    tenme = models.CharField(max_length=100)
    namsinhme = models.IntegerField()
    nghenghiepme = models.CharField(max_length=100)
    chucvume = models.CharField(max_length=100)
    noicongtacme = models.CharField(max_length=100)
    sdtme = models.CharField(max_length=100)
    chonlop = models.ForeignKey(DangKyHoc, on_delete=models.CASCADE)
from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import  Enum
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
    description = models.TextField()

    def __str__(self):
        return self.title

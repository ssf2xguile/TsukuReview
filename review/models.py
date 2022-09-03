from concurrent.futures import thread
from unicodedata import name
from django.contrib.auth import validators
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils import timezone
import uuid

class Subject(models.Model):
    code = models.CharField(verbose_name="科目番号", max_length=7, primary_key=True)
    name = models.CharField(verbose_name='科目名',blank=False, null=False, max_length=150)
    unit = models.CharField(verbose_name="単位数",blank=False, null=False, default="", max_length=10)
    grade = models.CharField(verbose_name="履修年次",blank=False, null=False, default="", max_length=15)
    semester = models.CharField(verbose_name="学期",blank=False, null=False, default="", max_length=15)
    teachers =  models.TextField(verbose_name='教員名', blank=True, max_length=100, default="")
    overview = models.TextField(verbose_name='概要', blank=True, max_length=200, default="")
    subtype =  models.TextField(verbose_name='種類', blank=True, max_length=32, default="")
    schools = models.CharField(verbose_name="学群等", blank=True,max_length=20, default="")
    colleges = models.CharField(verbose_name="学類等", blank=True, max_length=40, default="")
    star1 = models.IntegerField(verbose_name="星1",blank=False,default=0)
    star2 = models.IntegerField(verbose_name="星2",blank=False,default=0)
    star3 = models.IntegerField(verbose_name="星3",blank=False,default=0)
    star4 = models.IntegerField(verbose_name="星4",blank=False,default=0)
    star5 = models.IntegerField(verbose_name="星5",blank=False,default=0)

    def __str__(self):
        return self.code + " " + self.name

class Review(models.Model):
    lecture  = models.ForeignKey(Subject, on_delete=models.CASCADE, default=0)
    review_id = models.UUIDField(verbose_name='投稿者id', primary_key=True, default=uuid.uuid4, editable=False)
    sender_name = models.CharField(verbose_name='投稿者名', max_length=40, blank=False)
    text = models.TextField(verbose_name='本文', blank=False, max_length=500)
    created_at = models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    

    def __str__(self):
        return str(self.review_id)

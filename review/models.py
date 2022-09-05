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
    YEAR = (
        (2022, '2022年'),
        (2021, '2021年'),
        (2020, '2020年'),
        (2019, '2019年'),
    )

    RATING = (
        (5, '5.0'),
        (4, '4.0'),
        (3, '2.0'),
        (2, '2.0'),
        (1, '1.0'),
    )

    GRADE = (
        (5, 'A+'),
        (4, 'A'),
        (3, 'B'),
        (2, 'C'),
        (1, 'D'),
        (0, '非公開'),
    )

    lecture  = models.ForeignKey(Subject, on_delete=models.CASCADE, default='GA13501')
    review_id = models.UUIDField(verbose_name='口コミid', primary_key=True, default=uuid.uuid4, editable=False)
    # sender_name = models.CharField(verbose_name='投稿者名', blank=False, max_length=40)
    # sender_college = models.CharField(verbose_name='投稿者の所属学類', blank=False, max_length=40)
    title = models.CharField(verbose_name='タイトル', blank=False, null=False,max_length=30)
    year = models.IntegerField(verbose_name='受講した年度', choices=YEAR, default=2022)
    rating = models.IntegerField(verbose_name='星', choices=RATING, default=5)
    grade = models.IntegerField(verbose_name='成績', choices=GRADE, default=5)
    overall = models.TextField(verbose_name='総評', blank=False, null=False,max_length=500)
    difficulty = models.TextField(verbose_name="難易度",blank=False, null=False,max_length=100)
    kadai = models.TextField(verbose_name="課題の量・質",blank=False, null=False,max_length=100)
    evaluation = models.TextField(verbose_name="評価の甘さ",blank=False, null=False,max_length=100)
    created_at = models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    

    def __str__(self):
        return str(self.review_id)

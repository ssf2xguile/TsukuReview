from django.contrib.auth.models import UserManager, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.core.mail import send_mail
from django.utils import timezone


class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    COLLEGE = (
        (1, '人文学類'),
        (2, '比較文化学類'),
        (3, '日本語・日本文化学類'),
        (4, '社会学類'),
        (5, '国際総合学類'),
        (6, '教育学類'),
        (7, '心理学類'),
        (8, '障害科学類'),
        (9, '生物学類'),
        (10, '生物資源学類'),
        (11, '地球学類'),
        (12, '数学類'),
        (13, '物理学類'),
        (14, '化学類'),
        (15, '応用理工学類'),
        (16, '工学システム学類'),
        (17, '社会工学類'),
        (18, '情報科学類'),
        (19, '情報メディア創成学類'),
        (20, '知識情報・図書館学類'),
        (21, '医学類'),
        (22, '看護学類'),
        (23, '医療科学類'),
        (24, '体育専門学群'),
        (25, '芸術専門学群'),
        (26, '総合学域群'),
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField('ユーザー名',max_length=30,
        blank=False,
    )
    email = models.EmailField('メールアドレス', max_length=40,unique=True)
    college = models.IntegerField('学類', choices=COLLEGE, default=1)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    created_at = models.DateTimeField('作成日', default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Notice(models.Model):
    title = models.CharField('タイトル', max_length=100)
    content = models.TextField('内容', max_length=400)
    created_at = models.DateTimeField('作成日', default=timezone.now)
    updated_at = models.DateTimeField('更新日', default=timezone.now)
    
    def __str__(self):
        return self.title
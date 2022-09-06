# Generated by Django 3.2 on 2022-09-06 12:43

import accounts.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=30, verbose_name='ユーザー名')),
                ('email', models.EmailField(max_length=40, unique=True, verbose_name='メールアドレス')),
                ('college', models.IntegerField(choices=[(1, '人文学類'), (2, '比較文化学類'), (3, '日本語・日本文化学類'), (4, '社会学類'), (5, '国際総合学類'), (6, '教育 学類'), (7, '心理学類'), (8, '障害科学類'), (9, '生物学類'), (10, '生物資源学類'), (11, '地球学類'), (12, '数学類'), (13, '物理学類'), (14, '化学類'), (15, '応用理工学類'), (16, '工学システム学類'), (17, '社会工学類'), (18, '情報科学類'), (19, '情報メディア創成学類'), (20, '知識情報・図書館学類'), (21, '医学類'), (22, '看護学類'), (23, '医療科学類'), (24, '体育専門学群'), (25, '芸術専門学群'), (26, '総合学域群')], default=1, verbose_name='学類')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
    ]

# Generated by Django 3.2 on 2022-09-05 09:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='sender_name',
        ),
        migrations.RemoveField(
            model_name='review',
            name='text',
        ),
        migrations.AddField(
            model_name='review',
            name='difficulty',
            field=models.TextField(max_length=100, null=True, verbose_name='難易度'),
        ),
        migrations.AddField(
            model_name='review',
            name='evaluation',
            field=models.TextField(max_length=100, null=True, verbose_name='評価の甘さ'),
        ),
        migrations.AddField(
            model_name='review',
            name='grade',
            field=models.IntegerField(choices=[(5, 'A+'), (4, 'A'), (3, 'B'), (2, 'C'), (1, 'D'), (0, '非公開')], default=5, verbose_name='成績'),
        ),
        migrations.AddField(
            model_name='review',
            name='kadai',
            field=models.TextField(max_length=100, null=True, verbose_name='課題の量・質'),
        ),
        migrations.AddField(
            model_name='review',
            name='overall',
            field=models.TextField(max_length=500, null=True, verbose_name='総評'),
        ),
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(5, '5.0'), (4, '4.0'), (3, '2.0'), (2, '2.0'), (1, '1.0')], default=5, verbose_name='星'),
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=30, null=True, verbose_name='タイトル'),
        ),
        migrations.AddField(
            model_name='review',
            name='year',
            field=models.IntegerField(choices=[(2022, '2022年'), (2021, '2021年'), (2020, '2020年'), (2019, '2019年')], default=2022, verbose_name='受講した年度'),
        ),
        migrations.AlterField(
            model_name='review',
            name='lecture',
            field=models.ForeignKey(default='GA13501', on_delete=django.db.models.deletion.CASCADE, to='review.subject'),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='口コミid'),
        ),
    ]
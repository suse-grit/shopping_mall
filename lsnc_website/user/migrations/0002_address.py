# Generated by Django 2.2.12 on 2020-07-10 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.CharField(max_length=11, verbose_name='收件人')),
                ('province', models.CharField(max_length=11, verbose_name='省')),
                ('city', models.CharField(max_length=11, verbose_name='市')),
                ('county', models.CharField(max_length=11, verbose_name='县')),
                ('detail', models.CharField(max_length=80, verbose_name='详细地址')),
                ('postcode', models.CharField(max_length=6, verbose_name='邮政编码')),
                ('receiver_phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('tag', models.CharField(max_length=10, verbose_name='标签')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否活跃')),
                ('id_default', models.BooleanField(default=False, verbose_name='是否为默认地址')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile')),
            ],
            options={
                'db_table': 'user_address',
            },
        ),
    ]

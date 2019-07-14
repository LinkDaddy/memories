# Generated by Django 2.1.7 on 2019-04-29 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True, verbose_name='文章标题')),
                ('content', models.TextField(verbose_name='正文')),
                ('status', models.CharField(choices=[('0', '草稿'), ('1', '公开')], default='0', max_length=1, verbose_name='状态')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('changed', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
    ]

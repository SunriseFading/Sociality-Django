# Generated by Django 2.2.6 on 2020-11-06 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20201103_2339'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ('title',), 'verbose_name': 'Группа', 'verbose_name_plural': 'Группы'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
    ]

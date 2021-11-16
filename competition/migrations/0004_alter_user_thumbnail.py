# Generated by Django 3.2.9 on 2021-11-15 11:01

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_auto_20211113_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='thumbnail',
            field=imagekit.models.fields.ProcessedImageField(default='user_thumbnail/default.jpg', upload_to='user_thumbnail', verbose_name='Миниатура пользователя'),
        ),
    ]

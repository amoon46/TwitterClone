# Generated by Django 4.0.4 on 2022-05-22 10:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_user_followees_alter_user_introduction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followees',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
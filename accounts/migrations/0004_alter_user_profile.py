# Generated by Django 3.2.9 on 2021-12-04 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.ImageField(upload_to='media/user/profile/'),
        ),
    ]
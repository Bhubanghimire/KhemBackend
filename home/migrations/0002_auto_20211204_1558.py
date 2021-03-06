# Generated by Django 3.2.9 on 2021-12-04 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimation',
            name='logo',
            field=models.ImageField(default='asdf', upload_to='estimation_logo/'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='estimation_logo/')),
                ('value', models.CharField(max_length=200)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.configchoice')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.project')),
            ],
        ),
    ]

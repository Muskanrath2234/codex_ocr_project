# Generated by Django 5.0.4 on 2024-04-24 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_pancard_image_alter_profile_profile_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='Profile_img',
        ),
        migrations.AlterField(
            model_name='profile',
            name='aadhar_Phone',
            field=models.PositiveIntegerField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='aadhar_number',
            field=models.IntegerField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pin',
            field=models.PositiveIntegerField(blank=True, max_length=6, null=True),
        ),
    ]

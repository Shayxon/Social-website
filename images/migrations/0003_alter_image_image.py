# Generated by Django 5.0.1 on 2024-02-06 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/%Y/%m/%d/'),
        ),
    ]

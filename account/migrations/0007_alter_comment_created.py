# Generated by Django 5.0.2 on 2024-02-13 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_comment_post_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(),
        ),
    ]

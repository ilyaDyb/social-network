# Generated by Django 4.2.7 on 2024-06-11 10:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_users_friends_temporaryuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporaryuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

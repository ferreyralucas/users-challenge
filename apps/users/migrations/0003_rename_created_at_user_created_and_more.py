# Generated by Django 4.1.1 on 2023-04-28 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_created_at_user_updated_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='created_at',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='updated_at',
            new_name='updated',
        ),
    ]
# Generated by Django 5.2.3 on 2025-07-07 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='img',
            new_name='item_img',
        ),
    ]

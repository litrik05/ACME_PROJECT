# Generated by Django 5.1.6 on 2025-03-07 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birthday', '0002_birthday_image_alter_birthday_birthday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birthday',
            name='image',
            field=models.ImageField(blank=True, upload_to='birthdays_images', verbose_name='Фото'),
        ),
    ]

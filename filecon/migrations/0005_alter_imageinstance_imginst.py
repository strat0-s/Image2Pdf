# Generated by Django 5.0.7 on 2024-07-16 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filecon', '0004_remove_imageinstance_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageinstance',
            name='imginst',
            field=models.ImageField(upload_to=''),
        ),
    ]
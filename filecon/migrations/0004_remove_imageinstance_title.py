# Generated by Django 5.0.7 on 2024-07-11 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filecon', '0003_remove_imagecollection_collection_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imageinstance',
            name='title',
        ),
    ]
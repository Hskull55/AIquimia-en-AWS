# Generated by Django 3.2.19 on 2024-03-31 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleAIlchemy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='combinaciones',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='static/imagenes/elementos/'),
        ),
    ]

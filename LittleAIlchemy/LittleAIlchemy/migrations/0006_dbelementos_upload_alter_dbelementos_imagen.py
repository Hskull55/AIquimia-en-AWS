# Generated by Django 5.0.4 on 2024-04-15 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleAIlchemy', '0005_alter_dbelementos_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbelementos',
            name='upload',
            field=models.ImageField(blank=True, upload_to='static/imagenes/elementos/'),
        ),
        migrations.AlterField(
            model_name='dbelementos',
            name='imagen',
            field=models.CharField(max_length=500),
        ),
    ]

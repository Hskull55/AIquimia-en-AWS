# Generated by Django 5.0.4 on 2024-04-28 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleAIlchemy', '0007_dbelementos_creadores'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbelementos',
            name='descubiertoPor',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

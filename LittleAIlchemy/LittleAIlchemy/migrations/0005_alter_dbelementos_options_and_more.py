# Generated by Django 5.0.4 on 2024-04-11 20:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleAIlchemy', '0004_auto_20240402_2315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dbelementos',
            options={'verbose_name': 'Elemento', 'verbose_name_plural': 'Elementos'},
        ),
        migrations.RemoveField(
            model_name='dbcombinaciones',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='dbcombinaciones',
            name='imagen',
        ),
        migrations.AddField(
            model_name='dbelementos',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='dbelementos',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='static/imagenes/elementos/'),
        ),
        migrations.AlterField(
            model_name='dbcombinaciones',
            name='elemento1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elemento1Combinaciones', to='LittleAIlchemy.dbelementos'),
        ),
        migrations.AlterField(
            model_name='dbcombinaciones',
            name='elemento2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elemento2Combinaciones', to='LittleAIlchemy.dbelementos'),
        ),
        migrations.AlterField(
            model_name='dbcombinaciones',
            name='resultado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='combinaciones', to='LittleAIlchemy.dbelementos'),
        ),
    ]
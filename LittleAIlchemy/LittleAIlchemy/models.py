from django.db import models

class Prueba(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        app_label = 'LittleAIlchemy'
        db_table = 'prueba'

    def __str__(self):
        return self.nombre

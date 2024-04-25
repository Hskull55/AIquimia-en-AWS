from django.db import models
from django.contrib.auth.models import User

# Modelo para los elementos
class dbElementos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    imagen = models.CharField(max_length=500)
    upload = models.ImageField(upload_to='static/imagenes/elementos/', blank=True)
    creadores = models.ManyToManyField(User, related_name='elementosCreados')

    class Meta:
        app_label = 'LittleAIlchemy'
        db_table = 'elementos'
        verbose_name = "Elemento"
        verbose_name_plural = "Elementos"

    def __str__(self):
        return self.nombre

# Modelo para las combinaciones
class dbCombinaciones(models.Model):
    id = models.AutoField(primary_key=True)
    elemento1 = models.ForeignKey(dbElementos, related_name='elemento1Combinaciones', on_delete=models.CASCADE)
    elemento2 = models.ForeignKey(dbElementos, related_name='elemento2Combinaciones', on_delete=models.CASCADE)
    resultado = models.ForeignKey(dbElementos, related_name='combinaciones', on_delete=models.CASCADE)

    class Meta:
        app_label = 'LittleAIlchemy'
        db_table = 'combinaciones'
        verbose_name = "Combinación"
        verbose_name_plural = "Combinaciones"

    def __str__(self):
        return f"ID: {self.id}, Elemento1: {self.elemento1}, Elemento2: {self.elemento2}, Resultado: {self.resultado}"

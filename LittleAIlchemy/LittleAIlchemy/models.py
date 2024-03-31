from django.db import models

# Modelo de prueba
class Prueba(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        app_label = 'LittleAIlchemy'
        db_table = 'prueba'

    def __str__(self):
        return self.nombre

# Modelo de prueba (real)
class Combinaciones(models.Model):
    id = models.AutoField(primary_key=True)
    elemento1 = models.CharField(max_length=255)
    elemento2 = models.CharField(max_length=255)
    resultado = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='static/imagenes/elementos/', blank=True)

    class Meta:
        app_label = 'LittleAIlchemy'
        db_table = 'combinaciones'
	# Como puse en plural el nombre de la tabla en esta prueba, necesito hacer esto para que aparezca bien
        verbose_name = "Combinación"
        verbose_name_plural = "Combinaciones"

    def __str__(self):
        return f"ID: {self.id}, Elemento1: {self.elemento1}, Elemento2: {self.elemento2}, Resultado: {self.resultado}"    

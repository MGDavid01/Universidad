from django.db import models
from Herramientas.get_ubicacion_mike import get_mike_location

class AnzueloMike(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    direccion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.direccion:
            self.direccion = get_mike_location(self.latitud, self.longitud)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"AnzueloMike {self.id} - {self.direccion or 'Sin dirección'}"
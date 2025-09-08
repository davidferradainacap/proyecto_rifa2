
from django.db import models
import json

class Publicidad(models.Model):
    imagen = models.ImageField(upload_to='publicidad/')
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Publicidad {self.id}"

# Create your models here.


class Premio(models.Model):
    CATEGORIA_CHOICES = [
        ('1er', '1er Lugar'),
        ('2do', '2do Lugar'),
        ('3er', '3er Lugar'),
        ('sec', 'Secundario'),
    ]
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='premios/', blank=True, null=True)
    categoria = models.CharField(max_length=3, choices=CATEGORIA_CHOICES, default='1er')

    def __str__(self):
        return f"{self.get_categoria_display()} - {self.nombre}"



class Numero(models.Model):
    valor = models.IntegerField()
    disponible = models.BooleanField(default=True)
    asistencia = models.BooleanField(default=False)
    nombre_completo = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    gmail = models.EmailField(blank=True, null=True)
    hoja = models.IntegerField(default=1, help_text="Número de hoja a la que pertenece este número")

    class Meta:
        unique_together = ('valor', 'hoja')

    def __str__(self):
        disp = 'Sí' if self.disponible else 'No'
        asis = 'Sí' if self.asistencia else 'No'
        return f"{self.valor} | Disponible: {disp} | Asistencia: {asis}"

class EstadoRuleta(models.Model):
    en_progreso = models.BooleanField(default=False)
    numeros_vendidos = models.TextField(default="[]")
    inicio = models.DateTimeField(null=True, blank=True)
    ganador = models.CharField(max_length=20, null=True, blank=True)

    def set_numeros(self, lista):
        self.numeros_vendidos = json.dumps(lista)

    def get_numeros(self):
        return json.loads(self.numeros_vendidos)

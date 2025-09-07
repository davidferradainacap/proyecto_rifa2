import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rifaed.settings')
django.setup()

from miapp.models import Numero

# Elimina todos los números de la base de datos
def eliminar_todos_los_numeros():
    Numero.objects.all().delete()
    print("Todos los números han sido eliminados.")

if __name__ == "__main__":
    eliminar_todos_los_numeros()

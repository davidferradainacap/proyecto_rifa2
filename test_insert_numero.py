import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rifaed.settings')
django.setup()

from miapp.models import Numero

n = Numero.objects.create(valor=1, hoja=1)
print('Numero creado:', n.valor, 'hoja:', n.hoja)
print('Total en base de datos:', Numero.objects.count())

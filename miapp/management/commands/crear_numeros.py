from django.core.management.base import BaseCommand
from miapp.models import Numero

class Command(BaseCommand):
    help = 'Crea 2000 números de rifa'

    def handle(self, *args, **kwargs):
        bulk = []
        for hoja in range(1, 5):
            for i in range(1, 501):
                bulk.append(Numero(valor=i, disponible=True, hoja=hoja))
        print(f"Intentando crear {len(bulk)} números...")
        Numero.objects.bulk_create(bulk)
        print("Bulk create ejecutado")
        self.stdout.write(self.style.SUCCESS('¡Listo! 500 números por hoja (1-4) creados.'))
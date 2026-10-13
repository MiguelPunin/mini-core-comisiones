from django.core.management import call_command
from django.core.management.base import BaseCommand
from commission_app.models import Vendedor, Regla, Venta


class Command(BaseCommand):
    help = 'Carga los datos de ejemplo solo si las tablas del ejercicio están vacías.'

    def handle(self, *args, **options):
        if any(model.objects.exists() for model in (Vendedor, Regla, Venta)):
            self.stdout.write('Datos existentes: no se cargan los ejemplos.')
            return
        call_command('loaddata', 'initial_data')

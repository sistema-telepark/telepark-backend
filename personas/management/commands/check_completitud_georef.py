"""Comando de gestión ``check_completitud_georef``.

Verifica la completitud del catálogo geográfico en BD: 0 provincias sin
municipios y 0 municipios sin localidades.
Delega en ``personas/georef.verificar_completitud()``; imprime un reporte 
y sale con código ≠ 0 si la completitud falla.
"""
from django.core.management.base import BaseCommand, CommandError

from personas.georef import verificar_completitud


class Command(BaseCommand):
    help = 'Verifica la completitud del catálogo geográfico (0 provincias sin municipios, 0 municipios sin localidades)'

    def handle(self, *args, **options):
        reporte = verificar_completitud()
        prov_sin = reporte['provincias_sin_municipios']
        mun_sin = reporte['municipios_sin_localidades']

        if reporte['ok']:
            self.stdout.write(self.style.SUCCESS(
                f'OK: {prov_sin} provincias sin municipios, '
                f'{mun_sin} municipios sin localidades'
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f'INCOMPLETO: {prov_sin} provincias sin municipios, '
                f'{mun_sin} municipios sin localidades'
            ))
            raise CommandError(
                'Catálogo geográfico incompleto: '
                f'{prov_sin} provincias sin municipios, '
                f'{mun_sin} municipios sin localidades. '
                'Ejecute cargar_georef (o cargar_georef --force en deployments existentes).'
            )
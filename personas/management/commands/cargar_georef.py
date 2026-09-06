"""Comando de gestión ``cargar_georef``.

Carga el catálogo geográfico (provincias, departamentos, localidades) desde los
fixtures locales de forma idempotente. No contiene lógica de carga inline:
delega en ``personas/georef.py``.

Flags:
- ``--force``: recarga el catálogo completo (borra filas y recarga), abortando
  si existe una ``Direccion`` referenciando ``Localidad`` (guard de integridad).
"""
from django.core.management.base import BaseCommand, CommandError

from personas.georef import GeoRefError, cargar_catalogo


class Command(BaseCommand):
    help = 'Carga el catálogo geográfico desde fixtures locales (provincias, departamentos, localidades) de forma idempotente'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Recarga el catálogo completo (borra filas del catálogo y recarga desde fixtures)',
        )

    def handle(self, *args, **options):
        force = options['force']

        try:
            conteos = cargar_catalogo(force=force)
        except GeoRefError as e:
            raise CommandError(f'Error al cargar el catálogo geográfico: {e}')
        except Exception as e:
            raise CommandError(f'Error inesperado al cargar el catálogo geográfico: {e}')

        if conteos is None:
            self.stdout.write(
                'Catálogo geográfico ya cargado — no se modifica la BD (skip idempotente)'
            )
            return

        self.stdout.write(self.style.SUCCESS(
            'Catálogo geográfico cargado desde fixtures locales: '
            f'{conteos["provincias"]} provincias, '
            f'{conteos["departamentos"]} departamentos, '
            f'{conteos["localidades"]} localidades '
            f'({conteos["localidades_duplicadas_eliminadas"]} duplicados eliminados)'
        ))
"""Comando de gestión ``cargar_georef``.

Carga el catálogo geográfico GeoRef (provincias, municipios, localidades) de
forma idempotente. No contiene lógica de descarga/carga inline: delega en
``personas/georef.py``.

Flags:
- ``--solo-descargar``: regenera los fixtures JSON desde la API sin tocar la BD.
- ``--force``: recarga el catálogo completo (borra filas y recarga), abortando
  si existe una ``Direccion`` referenciando ``Localidad`` (guard de integridad).
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from personas.georef import (
    GeoRefError,
    cargar_catalogo,
    descargar_catalogo_completo,
    generar_fixtures,
    leer_fixtures,
)
from personas.models import Direccion, Localidad, Municipio, Provincia


class Command(BaseCommand):
    help = 'Carga el catálogo geográfico GeoRef (provincias, municipios, localidades) de forma idempotente'

    def add_arguments(self, parser):
        parser.add_argument(
            '--solo-descargar',
            action='store_true',
            help='Regenera los fixtures JSON desde la API GeoRef sin tocar la BD',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Recarga el catálogo completo (borra filas del catálogo y recarga desde fixtures/API)',
        )

    def handle(self, *args, **options):
        solo_descargar = options['solo_descargar']
        force = options['force']

        if solo_descargar:
            self._solo_descargar()
            return

        if force:
            self._verificar_guard_integridad()
        elif Localidad.objects.exists():
            self.stdout.write(
                'Catálogo geográfico ya cargado — no se modifica la BD (early-exit)'
            )
            return

        datos = leer_fixtures()
        fuente = 'fixtures locales'
        if datos is None:
            self.stdout.write('Fixtures ausentes o vacíos — usando API GeoRef como fallback')
            datos = self._descargar_todo()
            fuente = 'API GeoRef'

        try:
            with transaction.atomic():
                if force:
                    self._borrar_catalogo()
                conteos = cargar_catalogo(datos)
        except GeoRefError as e:
            raise CommandError(f'Error al cargar el catálogo GeoRef: {e}')
        except Exception as e:
            raise CommandError(f'Error inesperado al cargar el catálogo GeoRef: {e}')

        self.stdout.write(self.style.SUCCESS(
            f'Catálogo geográfico cargado desde {fuente}: '
            f'{conteos["provincias"]} provincias, '
            f'{conteos["municipios"]} municipios, '
            f'{conteos["localidades"]} localidades'
        ))

    def _solo_descargar(self):
        """Regenera los fixtures JSON desde la API sin tocar la BD."""
        try:
            datos = self._descargar_todo()
            generar_fixtures(datos)
        except GeoRefError as e:
            raise CommandError(f'Error al regenerar fixtures GeoRef: {e}')

        self.stdout.write(self.style.SUCCESS(
            'Fixtures GeoRef regenerados: '
            f'{len(datos["provincias"])} provincias, '
            f'{len(datos["municipios"])} municipios, '
            f'{len(datos["localidades"])} localidades'
        ))

    def _descargar_todo(self):
        """Descarga el catálogo completo con completitud aplicada.

        Provincias → municipios (+ departamentos de provincias sin municipios) →
        localidades (+ homónimas sintéticas). Sin tocar BD.
        """
        return descargar_catalogo_completo()

    def _verificar_guard_integridad(self):
        """Aborta ``--force`` si existe una ``Direccion`` referenciando ``Localidad``.

        Sin borrar datos.
        """
        if Direccion.objects.filter(idlocalidad__isnull=False).exists():
            raise CommandError(
                'No se puede forzar la recarga: existen direcciones referenciando localidades. '
                'Elimine o reasigne esas direcciones antes de usar --force.'
            )

    def _borrar_catalogo(self):
        """Borra el catálogo en orden inverso de dependencia (restricciones FK físicas)."""
        Localidad.objects.all().delete()
        Municipio.objects.all().delete()
        Provincia.objects.all().delete()
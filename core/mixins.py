import re

from django.apps import apps
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.exceptions import NotFound, ValidationError

_NUMERIC_RE = re.compile(r'^-?\d+$')


class ModelPKMixin:
    lookup_field = 'pk'
    manager = None
    app_tag = None

    @property
    def queryset(self):
        if self.manager is not None and hasattr(self.manager, 'model'):
            return self.manager.model.objects.none()
        return None

    def get_queryset(self):
        if self.manager is not None:
            return self.manager.listar_ordenado()
        return self.queryset


class NoPaginationMixin:
    pagination_class = None


class PersonaEpSubresourceMixin:
    """Valida la existencia del PersonaEp antes de filtrar sub-recursos."""

    def validar_personaep(self, personaep_pk):
        # `apps.get_model` evita el import circular core → personas.
        PersonaEp = apps.get_model('personas', 'PersonaEp')
        if not PersonaEp.objects.filter(pk=personaep_pk).exists():
            raise NotFound('No encontrado')


class CascadeFilterMixin:
    """Aplica filtros de cascada y desactiva la paginación cuando están activos."""

    cascade_lookups = {}

    def get_queryset(self):
        qs = super().get_queryset()
        request = getattr(self, 'request', None)
        if request is None:
            return qs
        for param, lookup in self.cascade_lookups.items():
            valor = request.query_params.get(param)
            if valor is None or valor == '':
                # Param ausente o vacío → tratado como ausente, sin filtro ni error.
                continue
            if _NUMERIC_RE.match(valor) is None:
                raise ValidationError({
                    'detail': f'El parámetro "{param}" debe ser un ID numérico (recibido: "{valor}").'
                })
            if callable(lookup):
                kwargs = lookup(valor)
            else:
                kwargs = {lookup: valor}
            qs = qs.filter(**kwargs)
        return qs

    def paginate_queryset(self, queryset):
        request = getattr(self, 'request', None)
        if request is not None:
            for param in self.cascade_lookups:
                valor = request.query_params.get(param)
                if valor is not None and valor != '':
                    # Filtro activo → array plano (paginación desactivada).
                    return None
        return super().paginate_queryset(queryset)


def auto_tag_schema_view(cls):
    if hasattr(cls, 'app_tag') and cls.app_tag:
        tag = cls.app_tag
        decorator = extend_schema_view(
            list=extend_schema(tags=[tag]),
            retrieve=extend_schema(tags=[tag]),
            create=extend_schema(tags=[tag]),
            update=extend_schema(tags=[tag]),
            partial_update=extend_schema(tags=[tag]),
            destroy=extend_schema(tags=[tag]),
        )
        cls = decorator(cls)
        # También etiqueta @action methods (los que tienen atributo 'actions')
        for attr_name in dir(cls):
            method = getattr(cls, attr_name)
            if (callable(method) and hasattr(method, 'actions')
                    and not hasattr(method, '_schema')):
                setattr(cls, attr_name, extend_schema(tags=[tag])(method))
        return cls
    return cls

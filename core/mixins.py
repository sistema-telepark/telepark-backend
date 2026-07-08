# ModelPKMixin: exposes model PK type for drf-spectacular path parameter inference.
# Solves W001 warnings when ViewSets use get_queryset() via services
# instead of a class-level queryset attribute.
# Usage:
#     class PersonaViewSet(ModelPKMixin, viewsets.ModelViewSet):
#         service = _persona_service  # must have .model attribute
class ModelPKMixin:
    lookup_field = 'pk'
    service = None

    @property
    def queryset(self):
        # Returns empty queryset for spectacular introspection only.
        # No DB query is executed — just provides model metadata
        # so spectacular can infer the PK type as integer.
        if self.service is not None and self.service.model is not None:
            return self.service.model.objects.none()
        return None

from drf_spectacular.utils import extend_schema_view, extend_schema


class ModelPKMixin:
    lookup_field = 'pk'
    service = None
    app_tag = None

    @property
    def queryset(self):
        if self.service is not None and self.service.model is not None:
            return self.service.model.objects.none()
        return None

    def get_queryset(self):
        if self.service is not None:
            return self.service.listar()
        return self.queryset


class NoPaginationMixin:
    pagination_class = None


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

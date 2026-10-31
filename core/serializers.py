from rest_framework import serializers

DETALLE_CAMPO_DESCONOCIDO = 'Campo desconocido.'


class StrictFieldsMixin:
    def to_internal_value(self, data):
        if hasattr(data, 'keys'):
            desconocidos = sorted(set(data.keys()) - set(self.fields))
            if desconocidos:
                raise serializers.ValidationError({campo: [DETALLE_CAMPO_DESCONOCIDO] for campo in desconocidos})
        return super().to_internal_value(data)


class StrictSerializer(StrictFieldsMixin, serializers.Serializer):
    pass


class StrictModelSerializer(StrictFieldsMixin, serializers.ModelSerializer):
    pass

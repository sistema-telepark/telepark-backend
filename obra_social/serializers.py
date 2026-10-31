from core.fields import StrictBooleanField
from core.serializers import StrictModelSerializer

from .models import Cobertura, ObraSocial


class ObraSocialSerializer(StrictModelSerializer):
    es_estatal = StrictBooleanField(required=False, default=False)

    class Meta:
        model = ObraSocial
        fields = ('id_obra_social', 'nombre', 'es_estatal')


class CoberturaSerializer(StrictModelSerializer):
    class Meta:
        model = Cobertura
        fields = ('id_cobertura', 'persona_ep', 'obra_social')


class CoberturaEPSerializer(CoberturaSerializer):
    obra_social = ObraSocialSerializer(many=False, read_only=True)

    class Meta(CoberturaSerializer.Meta):
        pass

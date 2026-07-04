from rest_framework.routers import DefaultRouter
from .views import EventoViewSet, TipoEventoViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'api/evento', EventoViewSet, basename='evento')
router.register(r'api/tipoevento', TipoEventoViewSet, basename='tipoevento')

urlpatterns = router.urls

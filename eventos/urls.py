from rest_framework.routers import SimpleRouter
from .views import EventoViewSet, TipoEventoViewSet

router = SimpleRouter(trailing_slash=False)

router.register(r'api/v1/eventos', EventoViewSet, basename='eventos')
router.register(r'api/v1/tipos-evento', TipoEventoViewSet, basename='tipos-evento')

urlpatterns = router.urls

from rest_framework.routers import SimpleRouter

from .views import CoberturaViewSet, ObraSocialViewSet

router = SimpleRouter(trailing_slash=False)

router.register(r'api/v1/obras-sociales', ObraSocialViewSet, basename='obras-sociales')
router.register(r'api/v1/coberturas', CoberturaViewSet, basename='coberturas')

urlpatterns = router.urls

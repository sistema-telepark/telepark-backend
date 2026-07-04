from rest_framework.routers import DefaultRouter
from .views import ObraSocialViewSet, OSViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'api/obrasocial', ObraSocialViewSet, basename='obrasocial')
router.register(r'api/os', OSViewSet, basename='os')

urlpatterns = router.urls

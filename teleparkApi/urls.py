from django.conf.urls import url 
from . import views
from . import authentication

app_name = 'teleparkApi'
urlpatterns = [ 
    url(r'^api/auth$', authentication.auth_view),
    url(r'^api/persona$', views.persona_list),
    url(r'^api/personaEp$', views.personaEp_list),
    url(r'^api/direccion$', views.direccion_list),
    url(r'^api/tipoparentesco$', views.tipoParentesco_list),
    
    url(r'^api/localidad$', views.localidad_list),
    url(r'^api/municipio$', views.municipio_list)
]
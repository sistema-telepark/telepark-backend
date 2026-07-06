from django.urls import path
from usuarios import views

urlpatterns = [
    path('api/login', views.auth_view, name='login'),
    path('api/create_user', views.create_user, name='create_user'),
    path('api/refresh_token', views.TokenRefreshViewWrapper.as_view(), name='token_refresh'),
    path('api/users', views.get_users, name='get_users'),
    path('api/update_user', views.update_user, name='update_user'),
    path('api/users/<str:username>/role', views.change_user_role, name='change_user_role'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('token/refresh/', views.refresh_token, name='token_refresh')
]
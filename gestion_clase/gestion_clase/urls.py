from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import root_redirect # Importamos la nueva función

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # El inicio redirige según quién sea el usuario
    path('', root_redirect, name='root'), 
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('', include('core.urls')),
]
"""
URL configuration for ocds project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from accounts.views import CustomToken
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
# from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom-auth/', include('accounts.urls') ),

    # path('auth/jwt/create/', CustomToken.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('community-questions/', include('questions.urls')),
    path('', include('community.urls')),
    path('custom-user/', include('accounts.urls'))
] 
# + debug_toolbar_urls()

# if settings.DEBUG:
#     urlpatterns += path('__debug__/', include(debug_toolbar_urls))

# RAILWAY CONFIG
# media configuration for file uploads and static files
# urlpatterns += static(settings.MEDIA_URL, document=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document=settings.STATIC_ROOT)

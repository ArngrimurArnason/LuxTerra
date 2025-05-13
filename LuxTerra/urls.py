"""
URL configuration for LuxTerra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from LuxTerra import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('', views.home, name='home'),  # Homepage route (LuxTerra views)
    path('about/', views.about, name='about'),  # About page (LuxTerra views)
    path('contact/', views.contact, name='contact'),  # Contact page (LuxTerra views)

    path('user/', include('user.urls')),  # User app URLs
    path('properties/', include('property.urls')),  # Property app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
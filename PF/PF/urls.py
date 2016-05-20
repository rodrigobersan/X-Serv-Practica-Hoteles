"""PF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^login', 'django.contrib.auth.views.login'),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page':'/?offset=0'}),
    url(r'^(header.jpg)$', 'django.views.static.serve', {'document_root': 'templates'}),
    url(r'^(favicon.ico)$', 'django.views.static.serve', {'document_root': 'templates'}),
    url(r'^(style.css)$', 'django.views.static.serve', {'document_root': 'templates'}),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/profile/', 'PFapp.views.loggedin'),
    url(r'^alojamientos/(\d+)', 'PFapp.views.alojamiento'),
    url(r'^alojamientos', 'PFapp.views.alojamientos'),
    url(r'^about', 'PFapp.views.about'),
    url(r'^(\w+)/xml','PFapp.views.usuario_xml'),
    url(r'^(\w+)','PFapp.views.usuario'),
    url(r'^$', 'PFapp.views.main'),
]
#Lista de usuatios y contrasenyas:
#superuser contrasenya0
#usuario1 contrasenya1
#usuario2 contrasenya2
#usuario3 contrasenya3

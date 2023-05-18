"""PqrsdfApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.contrib.auth.decorators import login_required
from apps.pqrsdf.views import Home, Dashboard, CreatePqrsdfUser, GetPqrsdfView
from apps.user.views import Login, logoutUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='index'),
    path('dashboard/', login_required(Dashboard.as_view()), name='dashboard'),
    path('dashboard/pqrsdf/', include(('apps.pqrsdf.urls', 'pqrsdf'))),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout/', login_required(logoutUser), name='logout'),
    path('create_pqrsdf/', CreatePqrsdfUser.as_view(), name='create_pqrsdf'),
    path('get_pqrsdf/<str:radicated>/', GetPqrsdfView.as_view(), name='get_pqrsdf')
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]
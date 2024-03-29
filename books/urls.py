"""books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

from books import settings
from store.views import *

router = DefaultRouter()
router.register('book', BookView)
router.register('user_book_relation', UserBookRelationView)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),
    path('api/', include('article.urls')),

    path('celery/', include('mail.urls')),

    path('random/', get_random_number, name='random-number'),
    path('random/min/<int:min>/max/<int:max>/', RandomNumberView.as_view(), name='random-number-min-max'),

    path('user/registration/', UserRegistrationView.as_view(), name='registration'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns


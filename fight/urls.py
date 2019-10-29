from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from main import settings
from .views import *
from django.contrib.auth import logout
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', fightPage.as_view(), name = 'fightPage'),
    path('<int:heroid>', makeFight.as_view(), name = 'fightPage'),
    
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

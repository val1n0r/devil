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
    path('', kvestPage.as_view(), name ='kPage'),
    path('<str:taskName>', AcceptKvest.as_view(), name ='selectTask'), # Победы в ряд
    path('<str:taskName>', AcceptKvest.as_view(), name ='selectUpTask'), # АпСтат
    
    
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

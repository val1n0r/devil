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
    path('', upPage.as_view(), name = 'upPage'),
    #path('<int:pwr_level>', up_power.as_view(), name = 'uppwr'),
    #path('<str:url>', up_armor.as_view(), name = 'upparm'),
    #path('<str:buffhp>', UpdateHeroHp.as_view(), name = 'uppH'),
    path('<str:buffHero>', ComplexUpgrageHeroForm.as_view(), name = 'upHeroView'),
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
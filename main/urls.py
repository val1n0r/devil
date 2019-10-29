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
    path('', indexPage.as_view(), name = 'indexPage'),
    path('register/', reg, name = 'regPage'),
    path('welcome/',welcomePage.as_view(), name = 'welcomePage'),
    path('welcome/<str:HeroName>',first_hero.as_view(), name='buy_hero'),
    path('main/', mainPage.as_view(), name='mainPage'),
    path('main/<str:add>',addBonusMainPage.as_view(), name='addSameBonus'),
    
    path('store/',include('store.urls')),
    path('rudnik/',include('rudnik.urls')),
    path('fight/',include('fight.urls')),
    path('up-hero/',include('uhero.urls')),
    path('kvest/',include('kvest.urls')),
    path('swap-hero/',swapPage.as_view(), name='swapPage'),
    path('<int:heroid>',select_hero.as_view(), name='selectHero'),
    path('converter/',converterPage.as_view(), name='converterPage'),
    path('converter/<int:SilverCount>',ConvertVal.as_view(), name='ConvertValute'),
    
    
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

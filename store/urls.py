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
    path('', storePage.as_view(), name = 'storePage'),
    path('buy-hero', heroList.as_view(), name = 'heroList'),
    path('<str:HeroName>', buyHero.as_view(),name='buy_hero'),
    path('doublegold/',BuyGoldPage.as_view(), name='GoldPage'),
    path('doublegold/<str:Get_link>',BuyDoubleGoldBonus.as_view(), name='goldbf'),
    path('doublexp/',BuyXpPage.as_view(), name='XpPage'),
    path('doublexp/<str:Get_xp>',BuyDoubleXpBonus.as_view(), name='xp_b'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

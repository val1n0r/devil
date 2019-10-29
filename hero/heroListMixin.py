from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q,F
from django.views.generic import View

import datetime
import decimal

from level.models import UserLVL
from uinfo.models import UserAttribute


from .models import Hero
from uhero.models import UserHero




class get_hero_mixin(object):
    def get_hero(self,  uid, user_level, *args, **kwargs):
        already_have = UserHero.objects.filter(hero_id=uid)
        alh = []
        for t in already_have:
            alh.append(t.heroid)
        
        return Hero.objects.filter(HeroLevel__lte=user_level).exclude(id__in=alh), Hero.objects.filter(HeroLevel__gt=user_level).order_by('HeroLevel')[0:2]
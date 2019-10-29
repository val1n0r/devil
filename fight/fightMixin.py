from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q,F
from django.views.generic import View

import datetime
from datetime import timedelta
import decimal
import time

from level.models import UserLVL
from uinfo.models import UserAttribute
from uhero.models import UserHero


class fightMix(object):
    def get_enemy_list(self,UserLevel,uid,*args,**kwargs):
        return UserHero.objects.filter(herolevel__lte=UserLevel,IsActive=True).exclude(hero_id=uid)[0:3]
    '''
    def startFight(self,heroid,uid,*args,**kwargs):
        select_enemy_data = UserHero.objects.filter(heroid=heroid,IsActive=True)
        for e in select_enemy_data:
            enemy_Power = e.attackPower
            enemy_Armour = e.armour
            enemy_Hp = e.hitPoint
            enemy_hero_level = e.herolevel
        
        enemy_complex_power = (enemy_Armour*10+enemy_Hp)+(enemy_Power*3+enemy_hero_level*2)

'''
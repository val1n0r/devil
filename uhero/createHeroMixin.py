from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q,F
from django.views.generic import View

import datetime
import decimal

from level.models import UserLVL
from uinfo.models import UserAttribute
from hero.models import *
from uhero.models import UserHero


#get_data_from UserAttribute
class create_new_hero(object):
    def buy_a_new_hero(self,  HeroName, uid, silver_coin, knights, user_level, *args, **kwargs):
        get_data = Hero.objects.filter(HeroName=HeroName)# получение инфы о покупаемом герое
        for i in get_data:
            HeroName = i.HeroName
            HeroPower = i.HeroPower
            HeroArmour = i.HeroArmour
            HeroHp = i.HeroHp
            HeroImg = i.HeroImg
            HeroLevel = i.HeroLevel
            price_silver_coin = i.price_silver_coin
            priceKnights = i.priceKnights

        get_hero_id = Hero.objects.filter(HeroName=HeroName)
        for h in get_hero_id:
            hid = h.id
        #already_have_hero = UserHero.objects.filter(heroid=id,hero_id=uid).get(heroid=id)
        #if (already_have_hero):
            # create hero
        if(silver_coin >= price_silver_coin and knights >= priceKnights and user_level >= HeroLevel):
            try:
                UserHero.objects.filter(hero_id=uid,IsActive=True).update(IsActive=False)
            except:
                pass
            UserHero.objects.create(HeroName = HeroName, attackPower = HeroPower, armour = HeroArmour,
                                    hitPoint = HeroHp, imghero = HeroImg, herolevel = HeroLevel,
                                    IsActive=True,win=0,pwr_level=0,armour_level=0, heroid=hid,hero_id=uid, hp_level=0)

            
            UserAttribute.objects.filter(user_id = uid).update(silver_coin=F('silver_coin')-price_silver_coin,
                                             knights=F('knights')-priceKnights,isComplete=True)
            return True
        else: 
            return False
        #else:
            #return False

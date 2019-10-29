from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q,F
from django.views.generic import View

import datetime
import decimal
import re

from level.models import UserLVL
from uinfo.models import UserAttribute
from hero.models import *
from .models import *




class get_up_level(object):
    def get_up(self, uid, *args,**kwargs):
        get_up_data = UserHero.objects.filter(hero_id = uid,IsActive=True)
        for i in get_up_data:
            current_power_level = i.pwr_level
            current_armour_level = i.armour_level
            current_hp_level = i.hp_level

        ####  POWER #######
        pwr_list = {'pwr_level':1,'pwr_price_sc':1500,'pwr_price_knights':15,'pwr_link':None,'sumPower':50}
        pwr_list['pwr_level'] = current_power_level
        total_pwr_upped = up_pwr.objects.filter(pwr_level = current_power_level)
        for pwr in total_pwr_upped:
            pwr_list['sumPower'] = current_power_level * 25

        get_pwr_price = up_pwr.objects.filter(pwr_level=current_power_level+1) # Цена на улучшние

        for pa in get_pwr_price:
            pwr_list['pwr_price_sc'] = pa.price_sc
            pwr_list['pwr_price_knights'] = pa.price_knights
            pwr_list['pwr_link'] = pa.pwr_level
        if not get_pwr_price:
            pwr_list['pwr_price_sc'] = 0
            pwr_list['pwr_price_knights'] = 0

            
        #### END ######

        #### ARMOUR #######
        armour_list = {'armour_level':None,'armour_price_sc':None,'armour_price_knights':None,'armour_link':None,'sumArmour':None}
        armour_list['armour_level'] = current_armour_level 
        armour_list['sumArmour'] = current_armour_level * 25

        get_armour_price = up_armour.objects.filter(armour_level = current_armour_level+1)
        for a in get_armour_price:
            armour_list['armour_price_sc'] = a.price_sc
            armour_list['armour_price_knights'] = a.price_knights
            armour_list['armour_link'] = a.url
        
        if armour_list['armour_link'] == 12 or armour_list['armour_link'] is None:
            armour_list['armour_price_sc'] = 0
            armour_list['armour_price_knights'] = 0
         #### END ######


        #### HP #######
        hp_list = {'hp_level':None,'hp_price_sc':None,'hp_price_knights':None,'hp_link':None,'sumHp':None}
        hp_list['hp_level'] = current_hp_level
        hp_list['sumHp'] = current_hp_level * 50
        
        get_hp_price = up_hp.objects.filter(hp_level = current_hp_level + 1)
        for h in get_hp_price:
            hp_list['hp_price_sc'] = h.price_sc
            hp_list['hp_price_knights'] = h.price_knights
            hp_list['hp_link'] = h.link_hp
        
        
        ## hp_list['hp_price_sc'] = 0
           # hp_list['hp_price_knights'] = 0
         ##### END ######
        #get_up_status = UserHero.objects.filter())
        return pwr_list,armour_list,hp_list
            
        

class upPowerMixin(object):
    def up_pw(self, uid, pwr_level,silver_coin, knights, *args, **kwargs):
        s_hero = UserHero.objects.filter(hero_id = uid,IsActive=True)
        
        for p in s_hero:
            c_pwr_level = p.pwr_level
        

        get_pwr_n = up_pwr.objects.filter(pwr_level = c_pwr_level+1)
        if not get_pwr_n:
            pw_price_sc = 0
            pw_price_knights = 0
        else:
            for i in get_pwr_n:
                pw_price_sc = i.price_sc
                pw_price_knights = i.price_knights
        
            if (silver_coin >=pw_price_sc and knights >=pw_price_knights):
                UserHero.objects.filter(hero_id=uid,IsActive=True).update(pwr_level=F('pwr_level')+1)

                UserAttribute.objects.filter(user_id=uid).update(silver_coin=F('silver_coin') - pw_price_sc,knights=F('knights')-pw_price_knights)
                UserHero.objects.filter(hero_id=uid,IsActive=True).update(attackPower=F('attackPower')+25)
                return True
            else:
                return False





class upArmourMixin(object):
    def up_arm(self, uid, armour_level,silver_coin, knights, *args, **kwargs):
            #### GET armour_level
        a_hero = UserHero.objects.filter(hero_id = uid,IsActive=True)

        for a in a_hero:
            current_armour_level = a.armour_level # current_level
        
        #next_lvl_armour + get price
        get_next_level_armour = up_armour.objects.filter(armour_level = current_armour_level+1) #TODO: if lvl >12
        if not get_next_level_armour:
            ar_price_sc = 0
            ar_price_knights = 0
            return False
        else:
            for k in get_next_level_armour:
                ar_price_sc = k.price_sc
                ar_price_knights = k.price_knights

            if (silver_coin >= ar_price_sc and knights >= ar_price_knights):
                UserHero.objects.filter(hero_id=uid,IsActive=True).update(armour_level=F('armour_level')+1,armour=F('armour')+25)
                UserAttribute.objects.filter(user_id=uid).update(silver_coin=F('silver_coin') - ar_price_sc,knights=F('knights')-ar_price_knights)

                return True


class setMoreHp(object):
    def set_hp(self,uid,silver_coin,knights, *args, **kwargs):
        #get hero info
        hpData = UserHero.objects.filter(hero_id = uid)
        for h in hpData:
            currentHpLevel = h.hp_level
        
        #Получить  цену на апгрейд
        getUpdatePrice = up_hp.objects.filter(hp_level=currentHpLevel+1)
        if not getUpdatePrice:
            hp_price_sc = 0
            hp_price_knights = 0
        else:
            for p in getUpdatePrice:
                hp_price_sc = p.price_sc
                hp_price_knights = p.price_knights
        
            if (silver_coin >= hp_price_sc and knights >= hp_price_knights):
                    UserHero.objects.filter(hero_id=uid,IsActive=True).update(hp_level=F('hp_level')+1,hitPoint=F('hitPoint')+25)
                    UserAttribute.objects.filter(user_id=uid).update(silver_coin=F('silver_coin') - hp_price_sc,knights=F('knights')-hp_price_knights)

            return True
        




        

        





from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q,F
from django.contrib.auth import logout

from datetime import timedelta
import datetime
import re


from bonus.bonusMixin import TimeConverter
from uinfo.models import *
from uinfo.attrmixin import *
from uhero.models import UserHero
from hero.models import Hero
from hero.heroListMixin import get_hero_mixin
from bonus.bonusMixin import get_bonus_info
from bonus.models import DoubleGold,DoubleXp
from uhero.createHeroMixin import create_new_hero


class storePage(GetUserInfo,get_user_info, View):
    def get(self, request,  *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(storePage, self)
        context = logic_data.UserStat(uid)
        return render(request,'store.html',context)


class heroList(GetUserInfo,get_user_info,get_hero_mixin, View):
    def get(self, request,  *args, **kwargs):
        
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(heroList, self)
        context = logic_data.UserStat(uid)
        for q in UserAttribute.objects.filter(user_id=uid):
            user_level = q.level
        av_hero,n_lvl_hero = logic_data.get_hero(uid,user_level)
        if av_hero:
            context['av'] = av_hero
        else:
            context['av'] = False

        context['n_lvl'] = n_lvl_hero
        return render(request,'hero.html',context)

class buyHero(get_user_info, create_new_hero, View):
    def post(self, request, HeroName,  *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(buyHero, self)
        listUserStat = logic_data.get_list_stat(uid)

        for q in UserAttribute.objects.filter(user_id=uid):
            user_level = q.level
            silver_coin = q.silver_coin
            knights= q.knights

        
        res_buy_hero = logic_data.buy_a_new_hero(HeroName, uid, silver_coin, knights, user_level)

        if res_buy_hero:
            messages.add_message(request, messages.INFO, "Успех")
            return redirect('mainPage')
        else:
            messages.add_message(request, messages.INFO, "Что-то не так")
            return redirect('mainPage')




class BuyGoldPage(GetUserInfo,get_user_info,get_bonus_info,TimeConverter, View):
    def get(self, request,  *args, **kwargs):  
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(BuyGoldPage, self)
        context = logic_data.UserStat(uid)
        DoubleGoldStatus = logic_data.get_db_info(uid)
        #TODO: Получение часов,минут и
        #hours, minutes, seconds = logic_data.convert_timedelta(duration)
        get_t = DoubleGold.objects.filter(user_buff_id=uid).only('exp_time')
        
        totalBonus = None
        for i in get_t:
            exp_hour = (i.exp_time-datetime.datetime.now())
            hours, minutes = logic_data.convert_timedelta(exp_hour)
                
            hours = str(hours)
            minutes = str(minutes)

            totalBonus = (i.exp_time-datetime.datetime.now()).days
            if totalBonus >=1:
                totalBonus = str(totalBonus)
                context['have_dg'] = "{} ч.".format(hours) 

            else: 
                
                secs = exp_hour.total_seconds()
                hours = int(secs / 3600)
                minutes = int(secs / 60) % 60
                
                hours = str(hours)
                minutes = str(minutes)
                context['have_dg'] = "{} ч. {} минут".format(hours,minutes)
        
        context['goldLink'] = 'goldBonus'
        return render(request,'double-gold.html',context)


class BuyDoubleGoldBonus(get_user_info, get_bonus_info, View):
    def post(self, request,Get_link,  *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(BuyDoubleGoldBonus, self)
        listUserStat = logic_data.get_list_stat(uid)# Получение данных (серебро,кнайты, уровень)
        silver_coin = listUserStat['silver_coin']
        knights = listUserStat['knights']
        #TODO: exp_time  + Время покупки
        if knights >=4 and ('buy_GoldBuff' in request.POST):
            
            get_t = DoubleGold.objects.filter(user_buff_id=uid).only('exp_time')
            for i in get_t:
                if i.exp_time - datetime.datetime.now():
                    DoubleGold.objects.filter(user_buff_id=uid,Get_link='goldBonus').update(exp_time=F('exp_time')+timedelta(hours=1))
                    UserAttribute.objects.filter(user_id=uid).update(knights=F('knights')-4)
                    messages.add_message(request, messages.INFO, "Успешно купили зелье алхимика")
                    return redirect('GoldPage')
                

                '''else:
                    DoubleGold.objects.filter(user_buff_id=uid,Get_link='goldBonus').update(exp_time=F('exp_time')+timedelta(hours=1))
                    UserAttribute.objects.filter(user_id=uid).update(knights=F('knights')-4)
                    messages.add_message(request, messages.INFO, "Успешно купили зелье алхимика")
                    return redirect('GoldPage')'''

        elif knights >=4 and ('buy_GoldBuff24' in request.POST):
            get_t = DoubleGold.objects.filter(user_buff_id=uid).only('exp_time')
            for i in get_t:
                if i.exp_time >= datetime.datetime.now():
                    DoubleGold.objects.filter(user_buff_id=uid,Get_link='goldBonus').update(exp_time=F('exp_time')+timedelta(days=1))
                    UserAttribute.objects.filter(user_id=uid).update(knights=F('knights')-60)
                    totalBonus = (i.exp_time-datetime.datetime.now()).days
                    messages.add_message(request, messages.INFO, "Активировали зелье алхимика!")
                    messages.add_message(request, messages.INFO, "Купили зелье алхимика Итого бонус на :{} дней".format(totalBonus))
                    #totalBonus = (i.exp_time-datetime.datetime.now()).days
                    #messages.add_message(request, messages.INFO, "Итого бонус на :{} дней".format(totalBonus))
                    return redirect('GoldPage')
        else:
             return redirect('GoldPage')




class BuyXpPage(GetUserInfo,get_bonus_info, View):
    def get(self, request,  *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(BuyXpPage, self)
        context = logic_data.UserStat(uid)
        doubleXpCount = logic_data.get_dx_info(uid)
        if doubleXpCount >0:
            context['currentBuff'] = doubleXpCount
        context['DxLink'] = 'XpBonus'
        return render(request,'double-xp.html',context)

class BuyDoubleXpBonus(get_user_info, get_bonus_info, View):
    def post(self, request, Get_xp,  *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(BuyDoubleXpBonus, self)
        listUserStat = logic_data.get_list_stat(uid)# Получение данных (серебро,кнайты, уровень)
        
        knights = listUserStat['knights']
        dcount = logic_data.get_dx_info(uid)
        #if dcount > 100:
            #DoubleXp.objects.filter(user_buff_id=uid,Get_xp='XpBonus').update(buffCount=100)

        if knights > 4 and dcount < 100:
            if (dcount + 15) > 100:
                DoubleXp.objects.filter(user_buff_id=uid,Get_xp='XpBonus').update(buffCount=100)
                messages.add_message(request, messages.INFO, "Активировали бонус")
            else:
                UserAttribute.objects.filter(user_id=uid).update(knights=F('knights')-4)
                DoubleXp.objects.filter(user_buff_id=uid,Get_xp='XpBonus').update(buffCount=F('buffCount')+15)
                messages.add_message(request, messages.INFO, "Активировали бонус")
        
            
            return redirect('XpPage')
        else:
            messages.add_message(request, messages.INFO, "Ошибка,У вас максимальный бонус")
                    
            return redirect('XpPage')
       





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

from .fightMixin import fightMix

from uinfo.models import *
from uinfo.attrmixin import *
from uhero.models import UserHero
from hero.models import Hero
from uhero.createHeroMixin import *
from bonus.bonusMixin import get_bonus_info,TimeConverter
from bonus.models import DoubleXp


class fightPage(GetUserInfo, get_user_info,fightMix, get_bonus_info,View):
    def get(self, request, *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(fightPage, self)
        context = logic_data.UserStat(uid) # Статы
        listUserStat = logic_data.get_list_stat(uid)
        UserLevel = listUserStat['level']
        enemy = UserHero.objects.filter(herolevel__lte=UserLevel,IsActive=True).exclude(hero_id=uid)[0:3]
        context['enemy'] = enemy

        return render(request,'fight.html',context)

class makeFight(get_user_info,fightMix, get_bonus_info,View):
    def post(self, request,heroid, *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(makeFight, self)
        

        XpWin = 12
        XpLoose = 6
        GoldWin = 250
        GoldLoose = 100


        listUserStat = logic_data.get_list_stat(uid)
        UserLevel = listUserStat['level']
        UserEnergy = listUserStat['energy']

        dx = logic_data.get_dx_info(uid) # Инфа о двойном опыте
        
        if dx:# множитель xp
            XpWin = 24
            XpLoose = 12


        select_enemy_data = UserHero.objects.filter(heroid=heroid,IsActive=True)
        for e in select_enemy_data:
            enemy_Power = e.attackPower
            enemy_Armour = e.armour
            enemy_Hp = e.hitPoint
            enemy_hero_level = e.herolevel
        
        enemy_complex_power = (enemy_Armour*10+enemy_Hp)+(enemy_Power*3+enemy_hero_level*2)

        select_user_data = UserHero.objects.filter(heroid=heroid,IsActive=True,hero_id=uid)
        for u in select_user_data:
            user_Power = u.attackPower
            user_Armour = u.armour
            user_Hp = u.hitPoint
            user_hero_level = u.herolevel

        user_complex_power = (user_Armour*10+user_Hp)+(user_Power*3+user_hero_level*2)

        if(user_complex_power>enemy_complex_power and UserEnergy >=10 ):
            messages.add_message(request, messages.INFO, 'Победа! <br>  Золото:{}<br> Опыт:{}'.format(GoldWin,XpWin),extra_tags='win')
            UserAttribute.objects.filter(user_id = uid).update(silver_coin=F('silver_coin')+GoldWin,xp=F('xp')+(XpWin),energy=F('energy')-10,totalWin=F('totalWin')+1)
            return redirect('fightPage')

        elif(enemy_complex_power>user_complex_power and UserEnergy >=10):
            messages.add_message(request, messages.INFO, 'Поражение! <br>  Золото:{}<br> Опыт:{}'.format(GoldWin,12),extra_tags='loose')
            UserAttribute.objects.filter(user_id = uid).update(silver_coin=F('silver_coin')-GoldWin,xp=F('xp')+(XpWin/2),energy=F('energy')-10)
            
            return redirect('fightPage')

        else:
            messages.add_message(request, messages.INFO, "Ошибка в fight")
            return redirect('fightPage')










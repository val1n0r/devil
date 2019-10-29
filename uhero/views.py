from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q,F
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from uinfo.models import UserAttribute
from uinfo.attrmixin import *




from datetime import datetime, timedelta
from .models import *
from .upMixin import upPowerMixin,upArmourMixin,get_up_level,setMoreHp
from uinfo.attrmixin import get_user_info
import re
from django.middleware.csrf import rotate_token
from django import forms
from django.forms.formsets import formset_factory

class upPage(GetUserInfo,get_up_level, View):
    def get(self, request, *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(upPage, self)
        context = logic_data.UserStat(uid)
        pwr_list,armour_list,hp_list = logic_data.get_up(uid)
        

        #### POWER CONTEXT ############
        if pwr_list['pwr_level'] >=12:
            context['fullPower'] = True
        context['pwr_level'] = pwr_list['pwr_level']
        context['pwr_all'] = pwr_list['sumPower']
        context['pwr_price_sc'] = pwr_list['pwr_price_sc']
        context['pwr_price_knights'] = pwr_list['pwr_price_knights']
        context['pwr_link'] = pwr_list['pwr_link']
        ###### END #######################

        ### armour CONTEXT ####
        if armour_list['armour_level'] >=12:
            context['fullArmor'] = True
        context['armour_level'] = armour_list['armour_level']
        context['armour_all'] = armour_list['sumArmour']
        context['armour_price_sc'] = armour_list['armour_price_sc']
        context['armour_price_knights'] = armour_list['armour_price_knights']
        context['armour_link'] = armour_list['armour_link']
        ########## END ###########

        ####### HP CONTEXT ###########
        if hp_list['hp_level'] >=12:
            context['fullHp'] = True
        context['hp_level'] = hp_list['hp_level']
        uhp_lvl = hp_list['hp_level']
        context['hp_all'] = hp_list['sumHp']
        context['hp_price_sc'] = hp_list['hp_price_sc']
        context['hp_price_knights'] = hp_list['hp_price_knights']
        context['hp_link'] = hp_list['hp_link']
        ########## end ###########

        #context['tk'] = django.middleware.csrf.get_token(request)

        context['buffHero'] = 'buffHero'
       ###########################################################
        
        return render(request,'buff-hero.html',context)


class up_power(GetUserInfo,get_user_info, upPowerMixin, View):
    def post(self, request, pwr_level, *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(up_power, self)
        context = logic_data.UserStat(uid)

        listUserStat = logic_data.get_list_stat(uid)# Получение данных (серебро,кнайты, уровень)
        silver_coin = listUserStat['silver_coin']
        knights = listUserStat['knights']
        res = logic_data.up_pw(uid,pwr_level,silver_coin,knights)


        if res:
            messages.add_message(request, messages.INFO, "Успех")
        else:
            messages.add_message(request, messages.INFO, "Ошибка")


        return redirect('upPage')

class up_armor(get_user_info,upArmourMixin, View):
    def post(self, request, url, *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(up_armor, self)
        

        listUserStat = logic_data.get_list_stat(uid)# Получение данных (серебро,кнайты, уровень)
        silver_coin = listUserStat['silver_coin']
        knights = listUserStat['knights']
        url = re.sub("\D", "", url)
        url = int(url)
        if url <=12:
            res_armour = logic_data.up_arm(uid,url,silver_coin,knights)
            if res_armour:
                messages.add_message(request, messages.INFO, "Успех")
        else:
            messages.add_message(request, messages.INFO, "Ошибка")


        return redirect('upPage')

class UpdateHeroHp(get_user_info, setMoreHp, View):
    def post(self, request, buffhp, *args, **kwargs):
        
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(UpdateHeroHp, self)
        #request= rotate_token(request)
        listUserStat = logic_data.get_list_stat(uid)# Получение данных (серебро,кнайты, уровень)
        silver_coin = listUserStat['silver_coin']
        knights = listUserStat['knights']
        if request.method == 'POST' and 'addHp' in request.POST:
            res_hp = logic_data.set_hp(uid,buffhp,silver_coin,knights)

            if res_hp:
                messages.add_message(request, messages.INFO, "Успех")
                return redirect('upPage')
            else:
                messages.add_message(request, messages.INFO, "fail")
                return redirect('upPage')
        




class ComplexUpgrageHeroForm(get_user_info, upPowerMixin, upArmourMixin, setMoreHp, View):
    def post(self, request, buffHero, *args, **kwargs):
        
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(ComplexUpgrageHeroForm, self)
        listUserStat = logic_data.get_list_stat(uid)# Получение данных (серебро,кнайты, уровень)
        silver_coin = listUserStat['silver_coin']
        knights = listUserStat['knights']

        if request.method == 'POST' and 'addPwr' in request.POST:
            get_pwr_level = UserHero.objects.filter(hero_id=uid)
            for i in get_pwr_level:
                pwr_level = i.pwr_level
            res = logic_data.up_pw(uid,pwr_level,silver_coin,knights)
            if res:
                messages.add_message(request, messages.INFO, "Успех")
                return redirect('upPage')
            else:
                messages.add_message(request, messages.INFO, "Ошибка прокачки силы")
                return redirect('upPage')

        elif (request.method == 'POST' and 'addArmour' in request.POST):
            get_armour_level = UserHero.objects.filter(hero_id=uid)
            for a in get_armour_level:
                armour_level = a.armour_level
            res_armour = logic_data.up_arm(uid,armour_level,silver_coin,knights)

            if res_armour:
                messages.add_message(request, messages.INFO, "Успешно прокачали броню")
                return redirect('upPage')
            else:
                messages.add_message(request, messages.INFO, "Ошибка прокачки брони")
                return redirect('upPage')
        
        elif (request.method == 'POST' and 'addHp' in request.POST):
            get_hp_level = UserHero.objects.filter(hero_id=uid)
            for a in get_hp_level:
                hp_level = a.hp_level
            res_armour = logic_data.set_hp(uid,silver_coin,knights)

            if res_armour:
                messages.add_message(request, messages.INFO, "Успешно прокачали здоровье")
                return redirect('upPage')
            else:
                messages.add_message(request, messages.INFO, "Ошибка прокачки хп")
                return redirect('upPage')
        



                





        

            
        
        

        
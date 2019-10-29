from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import UserRegisterForm
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

from rudnik.models import ConvertKnights
from .forms import *
from uinfo.models import *
from uinfo.attrmixin import *
from uhero.models import UserHero
from hero.models import Hero
from uhero.createHeroMixin import *
from bonus.bonusMixin import get_bonus_info,TimeConverter
from bonus.models import DoubleXp

from hero.heroListMixin import get_hero_mixin


class indexPage(get_status, View):
    def get(self, request, *agrs, **kwargs):
        if request.method == "POST":
            form = AuthenticationForm(request.POST)
            username = form['username']
            password = form['password']
            user = authenticate(username = username, password = password)
            #logic_data = super(indexPage, self)
            #context = logic_data.UserStat(uid) # Статы

            #login(request,user)
            #request.session['username'] = username

            #login = (request,user)
            uid = request.user.id # ид авторизованного пользователя
            logic_data = super(indexPage, self)
            if logic_data.status(uid):
                return redirect('/main')
            else:
                return redirect('/welcome')

            

        else:
            form = AuthenticationForm()
            return render(request,'index.html',{'form':form,'reg_count':User.objects.count(),'d_now':datetime.datetime.now()})




def reg(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request,user)
            UserAttribute.objects.create(silver_coin = 1000, knights = 75, power = 85, level = 1,
                                        xp = 0, energy = 100, totalWin = 0, user_id = user.id,
                                        last_accept_rudnik=datetime.datetime.now(),energy_time=datetime.datetime.now())
            UserAttribute.objects.filter(user_id=user.id).update(last_accept_rudnik=F('last_accept_rudnik')-timedelta(days=1))
            return redirect('/welcome')
    else:
        form  = UserRegisterForm()
    return render(request,'register.html',{'form':form})



class welcomePage(get_status, GetUserInfo,get_hero_mixin,get_user_info, View):
    def get(self, request, *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(welcomePage, self)
        user_status = logic_data.status(uid)
        if user_status==0:
            context = logic_data.UserStat(uid) # Статы
            listUserStat = logic_data.get_list_stat(uid)# Получение данных (кнайты)
            user_level = listUserStat['level']
            list_hero,next_lvl_hero = logic_data.get_hero(uid,user_level)
            context['hero'] = list_hero
      
            return render(request, 'welcome.html', context)
        else:
            return redirect('/main')


class first_hero(GetUserInfo, create_new_hero, get_user_info, View):
    def post(self, request, HeroName,heroid, *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(first_hero, self)
        heroid=None
        listUserStat = logic_data.get_list_stat(uid)# Получение данных (серебро,кнайты, уровень)
        silver_coin = listUserStat['silver_coin']
        knights = listUserStat['knights']
        user_level = listUserStat['level']
        create_hero = logic_data.buy_a_new_hero(HeroName, uid, silver_coin, knights, user_level)
        if create_hero:
            messages.add_message(request, messages.INFO, "Успех",extra_tags='win')
            return redirect('/main')
        else:
            return redirect('/welcome')

class mainPage(GetUserInfo, get_user_info, get_bonus_info,TimeConverter, View):
    def get(self, request, *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(mainPage, self)
        context = logic_data.UserStat(uid) # Статы
        listUserStat = logic_data.get_list_stat(uid)
        dx = logic_data.get_dx_info(uid) # бонусы
        if dx:
            context['dx'] = dx
        
        context['add'] = 'add'
        context['addEnergy'] = 'add60'
        context['addDXP'] = 'addDXP15'
        exp_hour = logic_data.get_db_info(uid)
        if exp_hour:
            hours, minutes = logic_data.convert_timedelta(exp_hour)
            hours = str(hours)
            context['gb'] = "{} ч.".format(hours)
        else:
            pass
        
        #UserAttribute.objects.filter(user_id=uid).update(xp=F('xp')+100)
        '''if gb:
            if re.findall('day',str(gb)) or re.findall('days',str(gb)):
                day_rem = str(gb)[0:1]
                day_rem = int(day_rem)
                if day_rem is 1:
                    context['gb'] = str(gb)[0:5]

                
                elif day_rem > 1 and day_rem < 10:
                    total_hour = day_rem * 24
                    context['gb'] = str(total_hour) + " Ч."

                #TODO:  Добавить еще одно условие
                
            
                
            else:
                context['gb'] = str(gb)[0:7]
                '''
        
        
        context['ActiveHero'] = UserHero.objects.filter(hero_id=uid, IsActive=True)
        return render(request, 'main.html', context)

class swapPage(GetUserInfo, get_user_info,View):
    def get(self, request, *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(swapPage, self)
        context = logic_data.UserStat(uid) # Статы

        # Получаем список user героев
        get_user_hero = UserHero.objects.filter(hero_id=uid).exclude(IsActive=True).order_by('herolevel')
        context['user_hero'] = get_user_hero

        return render(request,'swap-hero.html',context)
        
class select_hero(View):
    def post(self, request, heroid, *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        UserHero.objects.filter(hero_id=uid,IsActive=True).update(IsActive=False)
        UserHero.objects.filter(hero_id=uid,IsActive=False,heroid=heroid).update(IsActive=True)
        messages.add_message(request, messages.INFO, "Сменили героя")
        return redirect('mainPage')



class converterPage(GetUserInfo, get_user_info,View):
    def get(self, request, *args, **kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(converterPage, self)
        context = logic_data.UserStat(uid) # Статы

        # Выбрать данные из таблицы обменника
        get_swap_data = ConvertKnights.objects.all()
        context['convertVal'] = get_swap_data
        return render(request,'converter.html',context)

class ConvertVal(get_user_info,View):
    def post(self, request, SilverCount, *args, **kwargs):
        uid = request.user.id
        logic_data = super(ConvertVal, self)
        listUserStat = logic_data.get_list_stat(uid)# Получение данных (кнайты)
        UserKnights = listUserStat['knights']
        get_swap_data = ConvertKnights.objects.filter(SilverCount=SilverCount)
        for p in get_swap_data:
            if get_swap_data:
                if UserKnights >= p.KnightsPrice:
                    UserAttribute.objects.filter(user_id=uid).update(silver_coin=F('silver_coin')+SilverCount,knights=F('knights')-p.KnightsPrice)
                    messages.add_message(request, messages.INFO, "Обменяли {} на {}".format(p.KnightsPrice,SilverCount))
                    return redirect('converterPage')
            else:
                messages.add_message(request, messages.INFO, "Ошибка")
                return redirect('converterPage')

         
class addBonusMainPage(get_user_info, get_bonus_info, View):
    def post(self, request,add, *args, **kwargs):
        uid = request.user.id
        logic_data = super(addBonusMainPage, self)
        listUserStat = logic_data.get_list_stat(uid)# Получение данных (кнайты)
        UserKnights = listUserStat['knights']
        if request.method == 'POST' and 'addEnergy' in request.POST:# Если добавляем энергию
            UserEnergy = listUserStat['energy']
            if UserKnights >=2:
                if (UserEnergy < 100):
                    UpEnergy = UserAttribute.objects.filter(user_id=uid).update(knights=F('knights')-1,energy=F('energy')+60)
                    for e in UserAttribute.objects.filter(user_id=uid):
                        if e.energy > 100:
                            UserAttribute.objects.filter(user_id=uid).update(energy=100)
                    messages.add_message(request, messages.INFO, "Добавили энергии")
                    return redirect('mainPage')
                elif UserEnergy ==100:
                    UserAttribute.objects.filter(user_id=uid).update(energy=100)
                    messages.add_message(request, messages.INFO, "Максимум энергии")
                    return redirect('mainPage')
                else:
                    messages.add_message(request, messages.INFO, "Хм,ошибка")
                    return redirect('mainPage')
                
        elif (request.method == 'POST' and 'addXp' in request.POST):# Если добавляем двойной опыт
            dx = logic_data.get_dx_info(uid)
            if (UserKnights >=2) and (dx < 100):
                '''totalDxAdd = dx + 15

                if totalDxAdd >100:
                    totalDxAdd=100'''
                UserAttribute.objects.filter(user_id=uid).update(knights=F('knights')-2)
                DoubleXp.objects.filter(user_buff_id=uid).update(buffCount=F('buffCount')+15)
                
                messages.add_message(request, messages.INFO, "Установили двойной опыт")
                return redirect('mainPage')
            else:
                messages.add_message(request, messages.INFO, "Максимальное удвоение уже активировано")
                return redirect('mainPage')
        else:
            messages.add_message(request, messages.INFO, "Где-то закос")
            return redirect('mainPage')


            


            



def logOut(request):
    request(logout)
    return redirect('/')
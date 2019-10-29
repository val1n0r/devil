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

from uinfo.models import *
from uinfo.attrmixin import *
from .models import RudnikModel

class rudnikPage(GetUserInfo,View):
    def get(self,request,*args,**kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(rudnikPage, self)
        context = logic_data.UserStat(uid) # Статы
        getRudnikLevel = UserAttribute.objects.filter(user_id = uid).only('rudnik_level')
        for r in getRudnikLevel:
            rLevel = r.rudnik_level
        context['rudnikLevel']=rLevel

        totalBonus = 10
        
        if rLevel<=5:
            totalBonus+=rLevel*1
            context['TotalBonus'] = totalBonus
        elif rLevel >=6 and rLevel <=10:
            totalBonus+=(rLevel-5)*2+4
        elif rLevel >=11 and rLevel <=15:
            totalBonus+=(rLevel-10)*3+14
        elif rLevel >=16 and rLevel <=19:
            totalBonus+=(rLevel-15)*5+39
       
            
        context['TotalBonus']=totalBonus
        #Получить цену на апгрейд
        getNextUpRudnik = RudnikModel.objects.filter(RudnikLevel = rLevel+1)
        if not getNextUpRudnik:
            context['DoneRudnik']= True
        else:
            for b in getNextUpRudnik:
                RudnikPrice = b.RudnikPrice
                #context['totalBonus'] = b.
                context['link'] = b.RudnikLevel # ссылка
                context['price'] = b.RudnikPrice
                context['bonus'] = b.RudnikBonus
            
            
        infoAboutTime = UserAttribute.objects.filter(user_id=uid)
        for t in infoAboutTime:
            if not t.last_accept_rudnik:
                UserAttribute.objects.filter(user_id=uid).update(last_accept_rudnik=datetime.date.today())
            else:
                if t.last_accept_rudnik < datetime.date.today():
                    UserAttribute.objects.filter(user_id=uid).update(last_accept_rudnik=datetime.date.today())
                    UserAttribute.objects.filter(user_id=uid).update(knights=F('knights')+totalBonus)
                    messages.add_message(request, messages.INFO, "Собрали кнайты")
                    return redirect('rudnikPage')




        return render(request,'rudnik.html',context)

class UpRudnik(get_user_info,View):
    def post(self,request,RudnikLevel,*args,**kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(UpRudnik, self)

        listUserStat = logic_data.get_list_stat(uid)
        Userknights = listUserStat['knights']

        getRudnikLevel = UserAttribute.objects.filter(user_id = uid).only('rudnik_level')
        for r in getRudnikLevel:
            rLevel = r.rudnik_level

        getNextUpRudnik = RudnikModel.objects.filter(RudnikLevel = rLevel+1)
        if not getNextUpRudnik:
            pass
        else:
            for b in getNextUpRudnik:
                RudnikPrice = b.RudnikPrice
                UpPrice = b.RudnikPrice
            
            if Userknights >= RudnikPrice:
                UserAttribute.objects.filter(user_id=uid).update(knights=F('knights')-RudnikPrice,rudnik_level=F('rudnik_level')+1)
                messages.add_message(request, messages.INFO, "Прокачали рудник")
                return redirect('rudnikPage')
            else:
                messages.add_message(request, messages.INFO, "Не хватает валюты")
                return redirect('rudnikPage')






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

from .models import WinRowTask,UpHeroStat

class kvestPage(GetUserInfo,get_user_info,View):
    def get(self,request,*args,**kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(kvestPage, self)
        context = logic_data.UserStat(uid) # Статы
        listUserStat = logic_data.get_list_stat(uid)
        UserLevel = listUserStat['level']
        getAvaliableTask = WinRowTask.objects.filter(taskLevel__lte=UserLevel,winTask_id=uid)
        context['uptask'] = UpHeroStat.objects.filter(UpTask_id=uid,taskLevel__lte=UserLevel)
        context['tasks'] = getAvaliableTask
        return render(request,'task.html',context)


class AcceptKvest(get_user_info,View):
    def post(self,request,taskName,*args,**kwargs):
        uid = request.user.id # ид авторизованного пользователя
        logic_data = super(AcceptKvest, self)
        if 'Первая кровь' in taskName:
            WinRowTask.objects.filter(taskName=taskName,winTask_id=uid).update(taskStatus=True)
            messages.add_message(request, messages.INFO, "Приняли задание:{}".format(taskName))
            return redirect('kPage')
        elif 'Время улучшений' in taskName:
            UpHeroStat.objects.filter(taskName=taskName,UpTask_id=uid).update(taskStatus=True)
            messages.add_message(request, messages.INFO, "Приняли задание:{}".format(taskName))
            return redirect('kPage')


      
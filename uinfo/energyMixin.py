from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q,F
from django.views.generic import View

import datetime
from datetime import timedelta
import decimal
import time

from level.models import UserLVL
from .models import UserAttribute



class EnergyMix(object):
    def energy_reset(self,uid,*args,**kwargs):
        currentDate = time.time() # get_unix time
        get_energy = UserAttribute.objects.filter(user_id=uid)
        for i in get_energy:
            newEnergy = i.energy
            if i.energy < 100 and  i.energy < i.energy_max:
                restoreTime = 60 # in secs


        
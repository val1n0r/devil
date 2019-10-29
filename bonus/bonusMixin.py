from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q,F
from django.views.generic import View


import decimal
from datetime import datetime,timedelta
import re
from .models import DoubleXp,DoubleGold



class get_bonus_info(object):
	def get_dx_info(self, uid, *args, **kwargs):
		get_data = DoubleXp.objects.filter(user_buff_id = uid).only('buffCount')
		if not get_data:
			DoubleXp.objects.create(user_buff_id = uid,buff=1,buffCount=0,priceKnights=2,isActive=False,Get_xp='XpBonus')

		for i in get_data:
				
			if i.buffCount > 0:
				return i.buffCount
			else:
				return 0

	def get_db_info(self, uid, *args, **kwargs):
		get_gb = DoubleGold.objects.filter(user_buff_id = uid).only('exp_time')
		if not get_gb:
			DoubleGold.objects.create(user_buff_id = uid,buff=2,priceKnights=4,accept_time=datetime.now(),exp_time=datetime.now(),isActive=False,Get_link='goldBonus')
		for g in get_gb:
			if (g.exp_time-datetime.now()):
				return g.exp_time-datetime.now()

class TimeConverter(object):
	def convert_timedelta(self,exp_hour,*args,**kwargs):
		secs = exp_hour.total_seconds()
		hours = int(secs / 3600)
		minutes = int(secs / 60) % 60
		return hours, minutes

#td = datetime.timedelta(2, 7743, 12345)
#hours, minutes, seconds = convert_timedelta(td)
#print '{} minutes, {} hours'.format(minutes, hours)

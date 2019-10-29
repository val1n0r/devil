from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q,F
from django.views.generic import View

import datetime
import decimal
import time

from level.models import UserLVL
from .models import UserAttribute

class get_status(object): #TODO: add method "ONLY" for optimize speed
    def status(self, uid, *args, **kwargs):
        GetStatus = UserAttribute.objects.filter(user_id = uid).only('isComplete')
        for i in GetStatus:
            user_status = i.isComplete

        return user_status

#get_data_from UserAttribute
class get_user_info(object):
    def get_list_stat(self, uid, *args, **kwargs):
        get_data = UserAttribute.objects.filter(user_id = uid)

        #create list for extract data 
        data_list = {'silver_coin':None, 'knights':None, 
                     'power':None, 'level':None, 'xp':None, 'energy':None, 
                     'totalWin':None, 'isComplete':None
                    } 
        
        for i in get_data:
            data_list['silver_coin'] = i.silver_coin
            data_list['knights'] = i.knights
            data_list['power'] = i.power
            data_list['level'] = i.level
            data_list['energy'] = i.energy
            data_list['totalWin'] = i.totalWin
            data_list['isComplete'] = i.isComplete

        return data_list



class GetUserInfo(object):
   def UserStat(self, uid, *args, **kwargs):
        currentDate = time.time() # get_unix time
        #currentDate = abs(currentDate)
        get_energy = UserAttribute.objects.filter(user_id=uid)
        for i in get_energy:
            dateDiff = currentDate - i.energy_time.timestamp()
            newEnergy = i.energy
            max_energy = i.energy_max
            energ= i.energy
        if (dateDiff < 6000 and newEnergy < i.energy_max):
            while (dateDiff > 60):
                newEnergy+=1;
                if (newEnergy >=max_energy):
                    break
                dateDiff = dateDiff - 60;
        else:
            newEnergy = max_energy
        if (newEnergy !=energ):
            UserAttribute.objects.filter(user_id=uid).update(energy=newEnergy,energy_time=datetime.datetime.now())

        try:
            GetStat = UserAttribute.objects.filter(user_id = uid)
            if uid:
                for s in GetStat:
                    UserPower = s.power
                    UserSilver = s.silver_coin
                    UserKnights = s.knights
                    UserXp = s.xp
                    UserLevel = s.level
                    UserEnergy = s.energy
                    status = s.isComplete
                    UserWin = s.totalWin

                mylvl =  UserLVL.objects.raw("SELECT lvl FROM level_userlvl WHERE lvlxp - {}<=0".format(UserXp))
                for j in mylvl:
                    cl = j.lvl

                # Показ опыта для след уровня
                xpforlevel = UserLVL.objects.filter(lvl=UserLevel+1)
                for i in xpforlevel:
                    xpfl = i.lvlxp
                    reward = i.lvlreward
                
                '''xpforlevel =  UserLVL.objects.raw("SELECT lvl,lvlxp FROM level_userlvl WHERE lvl={}".format(UserLevel+1))
                for k in xpforlevel:
                    xpfl = k.lvlxp'''
                if UserXp >= xpfl or UserXp==xpfl:
                    UserAttribute.objects.filter(user_id=uid).update(level=F('level')+1,xp=F('xp')-UserXp,knights=F('knights')+reward)
                    #return redirect(request,'mainPage')


                progress = decimal.Decimal(round((UserXp/xpfl)*100,0))
			#dn = datetime.datetime.now()
			#context['dn']=dn

                context = {
					'UserSilver':UserSilver,'UserKnights':UserKnights,'UserXp':UserXp,'UserLevel':UserLevel,
					'UserEnergy':UserEnergy,'UserPower':UserPower,'status':status,
					'xpfl':xpfl,'progress':progress,'UserWin':UserWin,
				  }
            
				  #Время
            timeNow = datetime.datetime.now()
            timeNow = timeNow.strftime("%H:%M:%S")
            context['tn']=timeNow

            dateNow = datetime.datetime.now()
            dateNow = dateNow.strftime("%m/%d/%Y")
            context['dn']= dateNow
			

            return context
        except:
            pass

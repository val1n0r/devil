from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
from django.utils import timezone


class DoubleXp(models.Model): # Бонус двойного опыта
    user_buff = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)# rel with user id
    buff = models.IntegerField(default='1', editable=False) # id for extract and show on template
    buffCount = models.IntegerField(default="15")
    #priceGold = models.IntegerField(default="500")
    priceKnights = models.IntegerField(default="2")
    isActive = models.BooleanField(default=False)
    Get_xp = models.CharField(default='XpBonus', max_length=50)

    def __str__(self):
	    return (str(self.user_buff.username))

    def get_absolute_url(self):
	    return reverse('xp_b', kwargs={'Get_xp' : self.Get_xp})


class DoubleGold(models.Model):
    user_buff = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    buff = models.IntegerField(default='2',editable=False) # id for extract and show on template
    priceKnights = models.IntegerField(default="4")
    accept_time = models.DateTimeField(default=None)
    exp_time = models.DateTimeField(default=None)
    isActive = models.BooleanField(default=False)
    Get_link = models.CharField(default='goldBonus', max_length=50)
    
    def __str__(self):
        return (str(self.user_buff.username))
    

    def get_absolute_url(self):
        return reverse('goldbf',kwargs={'Get_link': self.Get_link})
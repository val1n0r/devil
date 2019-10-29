from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class RudnikModel(models.Model):
    RudnikLevel = models.IntegerField(default=1,primary_key=True)
    RudnikPrice = models.IntegerField(default=50) # price knights
    RudnikBonus = models.IntegerField(default=2)
    

    def __str__(self):
	       return str(str(self.RudnikLevel) +  " Бонус | " + str(self.RudnikBonus))

    def get_absolute_url(self):
        return reverse('upRu',kwargs={'RudnikLevel':self.RudnikLevel})



class ConvertKnights(models.Model):
    SilverCount = models.IntegerField(default=30000,primary_key=True)
    KnightsPrice = models.IntegerField(default=5) # price knights
    
    def __str__(self):
	       return str(str(self.SilverCount) +  " За: " + str(self.KnightsPrice))

    def get_absolute_url(self):
        return reverse('ConvertValute',kwargs={'SilverCount':self.SilverCount})

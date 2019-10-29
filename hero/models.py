from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse




class Hero(models.Model):

	HeroName = models.CharField(max_length = 32,default='Лорд Крестоносец')
	HeroPower = models.IntegerField(default="25")
	HeroArmour = models.IntegerField(default="25")
	HeroHp = models.IntegerField(default="85")
	HeroImg = models.ImageField(upload_to='Hero_image')
	HeroLevel = models.IntegerField(default="1")
	price_silver_coin = models.IntegerField(default="500")
	priceKnights = models.IntegerField(default="25")
	


	def __str__(self):
		return str(self.HeroName + ' | Уровень :' + str(self.HeroLevel))

	def get_abolute_url(self):
		return reverse('buy_hero',kwargs={'HeroName':self.HeroName})
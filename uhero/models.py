from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User




class UserHero(models.Model):
	hero = models.ForeignKey(User,on_delete=models.CASCADE)

	HeroName = models.CharField(max_length = 32,default='Лорд Крестоносец')
	attackPower = models.IntegerField(default="25")
	armour = models.IntegerField(default="25")
	hitPoint = models.IntegerField(default="85")
	imghero = models.ImageField(upload_to='heroimage')
	herolevel = models.IntegerField(default="1")
	IsActive = models.BooleanField(default=False)
	win = models.IntegerField(default="0")
	pwr_level = models.IntegerField(default=1)
	armour_level = models.IntegerField(default=1)
	hp_level = models.IntegerField(default=1)
	heroid = models.IntegerField(default=1)

	def __str__(self):
		#return str(self.HeroName)
		return str(self.HeroName + ' | Аккаунт :' + str(self.hero.username))

	def get_absolute_url(self):
		return reverse('selectHero',kwargs={'heroid':self.heroid})
	
	def get_fight_url(self):
		return reverse('mfight',kwargs={'heroid':self.heroid})


class up_pwr(models.Model):
	pwr_level = models.IntegerField(primary_key=True)
	pwr = models.IntegerField(default=12)
	price_sc = models.IntegerField(default=450)
	price_knights = models.IntegerField(default=3)

	def __str__(self):
		return str(str(self.pwr_level) +  "| Бонус силы: " + str(self.pwr ))

	def get_absolute_url(self):
		return reverse('uppwr',kwargs={'pwr_level':self.pwr_level})


class up_armour(models.Model):
	armour_level = models.IntegerField(primary_key=True)
	armour = models.IntegerField(default=12)
	price_sc = models.IntegerField(default=450)
	price_knights = models.IntegerField(default=3)
	url = models.CharField(max_length=50,default='link')

	def __str__(self):
		return str(str(self.armour_level) +  "| Бонус Брони: " + str(self.armour ))

	def get_absolute_url(self):
		return reverse('upparm',kwargs={'url':self.url})


class up_hp(models.Model):
	hp_level = models.IntegerField(primary_key=True)
	hp = models.IntegerField(default=12)
	price_sc = models.IntegerField(default=450)
	price_knights = models.IntegerField(default=3)
	link_hp = models.CharField(default='link',max_length=50)

	def __str__(self):
		return str(str(self.hp_level) +  "| Бонус Здоровья: " + str(self.hp))
	
	def get_absolute_url(self):
		return reverse('uppH',kwargs={'link_hp':self.link_hp})
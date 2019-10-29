from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# CREATE USER ATTRIBUTE MODEL / Основные атрибуты пользователя
class UserAttribute(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)

	silver_coin = models.IntegerField(default="1000")
	knights = models.IntegerField(default="75")
	power = models.IntegerField(default="85")
	level = models.IntegerField(default="1")
	xp = models.IntegerField(default="0")
	energy = models.IntegerField(default=100)
	energy_max = models.IntegerField(default=100)
	energy_time = models.DateTimeField(default=None)
	totalWin = models.IntegerField(default=0)
	isComplete = models.BooleanField(default=False)
	rudnik_level = models.IntegerField(default=1)
	last_accept_rudnik = models.DateField(default=None)
	

	def __str__(self):
		return str(self.user.username)
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class UserLVL(models.Model):
    lvl = models.IntegerField(default='1',primary_key=True)
    lvlxp = models.IntegerField(default='120')
    lvlreward = models.IntegerField(default='1')

    def __str__(self):
	       return str(str(self.lvl) +  " Уровень | " + str(self.lvlxp))
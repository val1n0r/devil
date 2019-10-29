from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class WinRowTask(models.Model):
    winTask = models.OneToOneField(User,on_delete=models.CASCADE)
    
    taskName = models.CharField(default='Первая кровь',max_length=64)
    taskInfo = models.CharField(default='Проведи 5 боев',max_length=160)
    taskReward_sc = models.IntegerField(default=750)
    taskReward_knights = models.IntegerField(default=5)
    taskReward_xp = models.IntegerField(default=40)
    taskLevel = models.IntegerField(default=1)
    taskAccept = models.BooleanField(default=False)
    taskDone = models.BooleanField(default=False)
    taskWinCount = models.IntegerField(default=5)
    taskCurrentWin = models.IntegerField(default=0)
    
    

    taskImg = models.ImageField(upload_to='taskImg')


    def __str__(self):
        return str(self.taskName + ' |  Инфо: ' + str(self.winTask))

    def get_absolute_url(self):
        return reverse('selectTask',kwargs={'taskName':self.taskName})

class UpHeroStat(models.Model):
    UpTask = models.OneToOneField(User,on_delete=models.CASCADE)
    
    taskName = models.CharField(default='Время улучшений',max_length=64)
    taskInfo = models.CharField(default='Улучши одну из характеристик героя',max_length=160)
    taskReward_sc = models.IntegerField(default=750)
    taskReward_knights = models.IntegerField(default=5)
    taskReward_xp = models.IntegerField(default=40)
    taskLevel = models.IntegerField(default=1)
    task_id = models.IntegerField(default=2)
    taskStatus = models.BooleanField(default=False)
    TaskDone = models.BooleanField(default=False)

    taskImg = models.ImageField(upload_to='taskImg')


    def __str__(self):
        return str(self.taskName + ' |  Инфо: ' + str(self.taskInfo))

    def get_absolute_url(self):
        return reverse('selectUpTask',kwargs={'taskName':self.taskName})





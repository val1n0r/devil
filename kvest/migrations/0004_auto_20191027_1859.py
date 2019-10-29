# Generated by Django 2.2.6 on 2019-10-27 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kvest', '0003_winrowtask_tasklevel'),
    ]

    operations = [
        migrations.AddField(
            model_name='winrowtask',
            name='winTask',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UpHeroStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskName', models.CharField(default='Время улучшений', max_length=64)),
                ('taskInfo', models.CharField(default='Улучши одну из характеристик героя', max_length=160)),
                ('taskReward_sc', models.IntegerField(default=750)),
                ('taskReward_knights', models.IntegerField(default=5)),
                ('taskReward_xp', models.IntegerField(default=40)),
                ('taskLevel', models.IntegerField(default=1)),
                ('task_id', models.IntegerField(default=2)),
                ('taskStatus', models.BooleanField(default=False)),
                ('taskImg', models.ImageField(upload_to='taskImg')),
                ('UpTask', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
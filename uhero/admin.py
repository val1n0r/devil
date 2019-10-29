from django.contrib import admin
from .models import UserHero,up_pwr,up_hp,up_armour
# Register your models here.

admin.site.register(UserHero)
admin.site.register(up_pwr)
admin.site.register(up_hp)
admin.site.register(up_armour)
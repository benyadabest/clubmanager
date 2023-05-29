from django.contrib import admin
from .models import User, Athlete, Groups, Event, Eventsignup, ClassTime, Attendance, Club
# Register your models here.

admin.site.register(User)
admin.site.register(Club)
admin.site.register(Athlete)
admin.site.register(Groups)
admin.site.register(Event)
admin.site.register(Eventsignup)
admin.site.register(ClassTime)
admin.site.register(Attendance)
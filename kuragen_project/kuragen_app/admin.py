from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Concert, Song, Member, Position, RideNumber, Period, Schedule, Participant, Note 

# Register your models here.

admin.site.register(Concert)
admin.site.register(Song)
admin.site.register(Member)
admin.site.register(Position)
admin.site.register(RideNumber)
admin.site.register(Period)
admin.site.register(Schedule)
admin.site.register(Participant)
admin.site.register(Note)
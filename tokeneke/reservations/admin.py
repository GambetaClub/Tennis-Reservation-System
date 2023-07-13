from django.contrib import admin
from .models import Member, Venue, Event, Activity, Participation, Date
from .forms import CreateParticipationForm, CreateActivityForm


class ActivityAdmin(admin.ModelAdmin):
    form = CreateActivityForm


class ParticipationAdmin(admin.ModelAdmin):
    form = CreateParticipationForm


admin.site.register(Member)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Date)
admin.site.register(Participation, ParticipationAdmin)

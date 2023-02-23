from django.contrib import admin
from .models import Member, Venue, Event, Clinic, Participation, Date
from .forms import CreateParticipationForm ,CreateClinicForm

class ClinicAdmin(admin.ModelAdmin):
    form = CreateClinicForm


class ParticipationAdmin(admin.ModelAdmin):
    form = CreateParticipationForm



admin.site.register(Member)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Date)
admin.site.register(Participation, ParticipationAdmin)
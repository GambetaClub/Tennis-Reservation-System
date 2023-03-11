from django.db import models
from .validators import validate_percentage
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import recurrence.fields
from django.utils.timezone import make_aware
from django.utils import timezone
import pytz
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from .constants import *

"""
Helper functions
"""

def make_date_aware(date):
    return make_aware(date, timezone=pytz.timezone("America/New_York"))

def is_today(date):
    aware_date = make_aware(date, timezone=pytz.timezone("America/New_York")).strftime("%d %b, %Y")
    today = timezone.now().date().strftime("%d %b, %Y")
    return aware_date == today

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email.'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff = True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser = True.')

        return self.create_user(email, password, **other_fields)

class Member(AbstractBaseUser, PermissionsMixin):
    TEAM_A = 'A'
    TEAM_B = 'B'
    TEAM_C = 'C'
    NO_TEAM = 'No-Team'
    TEAM_CHOICES = [
        (TEAM_A, 'A-Team'),
        (TEAM_B, 'B-Team'),
        (TEAM_C, 'C-Team'),
        (NO_TEAM, 'No-Team')
    ]
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    ]

    email = models.EmailField(_('Email address'), unique=True)
    member_n = models.CharField(_('Member #'), max_length=10, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    level = models.IntegerField(validators=[validate_percentage], null=True)
    start_date = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES)
    team = models.CharField(max_length=7, choices=TEAM_CHOICES, blank=True)
    profile_pic = models.ImageField(default='profile_pics/default.jpeg', upload_to='profile_pics')
    is_playing = models.BooleanField(default=True)
    is_active =  models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']

    
    
    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name[0] + '.'
        else:
            return str(self.email)

    def get_fut_participations_registered(self):
        # Returns a query set with the future participations registered for
        return Participation.objects.filter(member = self).filter(date__datetime_start__gte=timezone.now()).order_by('date__datetime_start')
    
    def get_fut_events_registered(self):
        # Returns a query set with the future events registered for
        partis = self.get_fut_participations_registered()
        events_ids = set()
        for part in partis:
            events_ids.add(part.get_event().id)
        query_fut_events = Event.objects.filter(id__in=events_ids)
        return query_fut_events

    def get_level(self):
        if self.level:
            return self.level
        else:
            return 0

class Venue(models.Model):
    name = models.CharField("Venue Name", max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField("Zip Code", max_length=10)
    phone = models.CharField("Contact Phone", max_length=30)
    web = models.URLField("Website Address")
    email = models.EmailField("Email Address")
      
    def __str__(self):
        return self.name


class Event(models.Model):
    EVENT_MALE = 'M'
    EVENT_FEMALE = 'F'
    EVENT_MIXED = 'MIXED'

    PART_GENDER_CHOICES = [
        (EVENT_MALE, 'Male'),
        (EVENT_FEMALE, 'Female'),
        (EVENT_MIXED, 'Mixed')]

    TEAM_A = 'A'
    TEAM_B = 'B'
    TEAM_C = 'C'
    NO_TEAM = 'No-Team'

    TEAM_CHOICES = [
        (TEAM_A, 'A-Team'),
        (TEAM_B, 'B-Team'),
        (TEAM_C, 'C-Team'),
        (NO_TEAM, 'No-Team')
    ]

    title = models.CharField('Event Title', max_length=120, blank=False)
    description = models.TextField("Description", blank=True)
    gender = models.CharField("Gender", max_length=7, choices=PART_GENDER_CHOICES)
    team = models.CharField("Team", max_length=12, blank=True, choices=TEAM_CHOICES)

    REQUIRED_FIELDS = ['title', 'gender', 'team']

    def __str__(self):
        return self.title


    def get_clinics(self):
        return Clinic.objects.filter(event = self)

    def get_fut_dates(self, number=40):
        # Returns a list of the future Dates of the Event's Clinics
        clinics = Clinic.objects.filter(event__id = self.id)
        if clinics:
            # Retrieves the future dates
            dates =  Date.objects.filter(clinic__event__id=self.id).filter(datetime_start__gte=timezone.now()).order_by('datetime_start')[:number]
            if not dates:
                # If there are no future dates, then it will return the past dates
                dates = Date.objects.filter(clinic__event__id=self.id).order_by('-datetime_start')
            return dates[:number]
        return []
    
    def get_next_date(self):
        """
        Returns the next single date of the Event. If there are none,
        it returns None.
        """
        try:
            return self.get_fut_dates(1)[0]
        except:
            return None
        
    def print_next_date(self):
        # Returns the future Date formatted date
        try:
            date  = self.get_next_date().get_datetime_start()
            return date.strftime('%A, %b %-d - %I:%M %p')
        except:
            return "No more clinics"

    def get_remaining_days(self):
        # Returns a string of the remaining days for the fut Date
        try:
            remaining = (self.get_next_date().datetime_start - timezone.now()).days 
            if remaining < 0:
                if remaining == -1:
                    remaining = "Yesterday"
                else:
                    remaining = str(abs(remaining)) + " days ago"
            elif remaining == 0:
                remaining = 'Today'
            elif remaining == 1:
                remaining = 'Tomorrow'
            else:
                remaining = str(remaining + 1) + " days"
            return remaining
        except:
            return "No more clinics"

    def get_fullness(self):
        # Returns the fullness of the fut Date
        fut_date = self.get_next_date()
        if fut_date:
            return fut_date.get_cap_pct()
        
    def get_fut_date_rem_spots(self):
        # Returns the remaining spots available
        fut_date = self.get_next_date()
        if fut_date:
            return fut_date.get_rem_spots()
        else:
            return "No future date"
        
    def get_participants(self):
        try:
            return self.get_next_date().get_all_parts()
        except:
            "No next date"

class Clinic(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = title = models.CharField('Clinic Title', max_length=120, blank=True)
    recurrences = recurrence.fields.RecurrenceField()
    start_time = models.TimeField("Start Time", blank=True, null=True)
    end_time = models.TimeField("End Time", blank=True, null=True)
    capacity = models.IntegerField("Capacity", default=12)
    is_active = models.BooleanField("Active", default=True)

    REQUIRED_FIELDS = ['title', 'start_time', 'end_time', 'capacity', 'is_active']    

    def get_event(self):
        try:
            return Event.objects.get(clinic__id=self.id)
        except:
            return None

    def get_all_dates(self):
        return Date.objects.filter(clinic = self).order_by('datetime_start')

    def get_fut_dates(self, number=40):
        # Returns a query list with the "number" amount of future Date instances of the clinic
        try:
            fut_dates = Date.objects.filter(clinic__id=self.id).filter(datetime_start__gte=timezone.now()).order_by('datetime_start')[:number]
            return fut_dates
        except Exception as err:
            print(f"{err=}, {type(err)=}")
            return None
    

    def get_dates_desc(self):
        # Returns a string with the description of the fut date of the clinic
        try:
            return str("On " + self.get_fut_dates(1)[0].print_start_date())
        except:
            return "No More Future Dates"


    def get_date_by_datetime(self, datetime_start):
        # Returns the date instance based on the datetime_start
        try:
            date = Date.objects.get(clinic_id = self.id, datetime_start = datetime_start)
            return date
        except:
            return None

    def update_date_instances(self, old_occurrences = None, limit=30):
        """
        Creates/deletes dates based on the recurrence field. 
        It accepts a list with the old occurrences in order to compare
        if there are dates that should be deleted. It only deletes future
        dates.
        """
        # It will only create future dates
        yesterday = datetime.today() - timedelta(days=1)
        to_create = list(self.recurrences.between(yesterday, date_limit))[:limit]
        dates_instances = []

        # Checks if old_occurrences has been passed as an argument.
        if old_occurrences:    
            # Based on the sets, to_create only has the dates that have been added.
            to_create = list(set(to_create) - set(old_occurrences))[:limit]
            # Based on the sets, to_delete only has the dates that have been removed.
            to_delete = list(set(old_occurrences) - set(self.recurrences.between(yesterday, date_limit)))
            
            for date in to_delete:
                datetime_start = make_date_aware(date.replace(hour=self.start_time.hour, minute=self.start_time.minute, second=0, microsecond=0))
                date = self.get_date_by_datetime(datetime_start)
                if date:
                    date.delete()
        
        # For creating the dates
        for date in to_create:
            datetime_start = make_date_aware(date.replace(hour=self.start_time.hour, minute=self.start_time.minute, second=0, microsecond=0))
            datetime_end = make_date_aware(date.replace(hour=self.end_time.hour, minute=self.end_time.minute, second=0, microsecond=0))
            date = Date(clinic = self, datetime_start = datetime_start, datetime_end = datetime_end, capacity = self.capacity)
            dates_instances.append(date)

        Date.objects.bulk_create(dates_instances)


    def update_dates_capacity(self):
        """
        Updates the capacity of all the Date instances
        that are will happen in the future
        """
        dates = self.get_fut_dates()
        for date in dates:
            date.capacity = self.capacity
            date.save()

    def __str__(self):
        event = self.get_event()
        if event:
            if isinstance(event, Event):
                return str(self.get_event().title +  " - " + self.get_dates_desc())
            elif event.count() > 1:
                return str("Error here because this clinic has many events " + self.get_dates_desc())
        else:
            return str("No event yet - " + self.get_dates_desc())


class Date(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    datetime_start = models.DateTimeField(blank=False, null=False)
    datetime_end = models.DateTimeField(blank=False, null=False)
    participants = models.ManyToManyField(Member, through='Participation', blank=True)
    capacity = models.IntegerField("Capacity", default=12)

    REQUIRED_FIELDS = ['datetime_start', 'datetime_end', 'capacity']

    def __str__(self):
        date = self.get_datetime_start().strftime("%A %-m/%-d, %H:%M")
        return str(self.get_event_name() + ' on ' + date)
    
    def __hash__(self):
        return hash((self.datetime_start,))
         
    # def __eq__(self, other):
    #     return (self.datetime_start, ) == (other.datetime_start, )

    def is_registrable(self):    
        time_until = self.datetime_start - make_aware(datetime.now())
        if time_until < timedelta(hours=24):
            return False
        else:
            return True
        
    def get_clinic(self):
        return Clinic.objects.get(date = self)
    

    def get_all_parts(self):
        # Returns a list with all the participants with the ones that first registered first
        return [(i.member) for i in Participation.objects.filter(date__id = self.id).order_by('date_registered')]

    def get_parts_on_court(self):
        all_parts =  self.get_all_parts()
        on_court = all_parts[:self.capacity]
        # Order the participants by their level
        on_court.sort(key=lambda participant: participant.level, reverse=True)
        return on_court
    
    def get_parts_on_wait(self):
        all_parts =  self.get_all_parts()
        on_wait = all_parts[self.capacity:]
        return on_wait
    

    def get_datetime_start(self):
        return timezone.localtime(self.datetime_start)

    def get_event_name(self):
        try:
            return Event.objects.get(clinic__date__id=self.id).title
        except:
            return "No event yet"

    def print_start_date(self):
        return self.get_datetime_start().strftime(("%-m/%-d, %H:%M"))

    def get_event(self):
        # Returns the event for the corresponding Date
        try:
            event = Event.objects.get(clinic__date__id=self.id)
            return event
        except:
            return "No event found"

    def get_registered_count(self):
        return Participation.objects.filter(date__id=self.id).count()

    def get_capacity(self):
        return self.capacity

    def get_rem_spots(self):
        return self.get_capacity() - self.get_registered_count()
        
        
    def get_cap_pct(self):
        cap_pct = 1 - self.get_rem_spots()/ self.get_capacity()
        if cap_pct > 1:
            return 1
        else:
            return '{:.0%}'.format(1 - self.get_rem_spots()/ self.get_capacity())


class Participation(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    date_registered = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, max_length=100)

    REQUIRED_FIELDS = ['member', 'date']

    def save(self, *args, **kwargs):
        event = Event.objects.get(clinic__date = self.date)
        if event.gender != 'MIXED' and event.gender != self.member.gender:
            raise ValidationError(f"{str(self.member)} can't participate in a event for {event.get_gender_display().lower()}s.")
        else:
            super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['member', 'date'], name='member_can_sign_in_once'
            )
        ]

    def get_event(self):
        try:
            event = Event.objects.get(clinic__date = self.date)
            return event
        except:
            print("Get event in participation exception")
            return None

    def __str__(self):
        return str(self.member) + " for " + str(self.date)
        
        
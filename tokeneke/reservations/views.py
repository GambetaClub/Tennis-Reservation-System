from django.shortcuts import render, redirect
from .forms import CreateMemberForm, MemberAuthForm, CreateEventForm, CreateClinicForm, CreateDateForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from .models import Event, Clinic, Date, Participation
from django.utils import timezone
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .constants import *

@login_required
def home(request):
    # Querying all the events that have a next date after today. The next date field takes
    # care of giving the next date based on todays date. 

    request.user.get_fut_events_registered()
    excl_gen = 'F' if request.user.gender == 'M' else 'M'
    events = Event.objects.filter(clinic__date__datetime_start__gte=timezone.now()).exclude(gender=excl_gen).distinct()
    return render(request, 'main/home.html', {
        'events': events,
        'page_title': 'Events Available',
        'titles':{
                'Registered Dates': request.user.get_fut_participations_registered().count(),
                'Registered Events': request.user.get_fut_events_registered().count(),
                'Events Available': events.count()
                 }
    })


@login_required
def my_events(request):
    user_events =  request.user.get_fut_events_registered()
    try:
        next_event = request.user.get_fut_participations_registered()[0]
    except:
        next_event = None
    return render(request, 'main/home.html', {
        'page_title': 'My Events',
        'events': user_events,
        'next_event': next_event,
        'titles':{
                'Registered Dates': request.user.get_fut_participations_registered().count(),
                'Registered Events': user_events.count(),
                 }
    })

@login_required
@staff_member_required
def edit_all_events(request):
    all_events = Event.objects.all()
    return render(request, 'main/home.html', {
        'page_title': 'All Events',
        'events': all_events,
        'titles':{
                'All Events': all_events.count(),
                 }
    })

def register(request):
    form = CreateMemberForm()
    if request.method == "POST":
        form = CreateMemberForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account created. You will login with your email: ' + email)
            return redirect('login')
    return render(request, 'auth/register.html', {'form': form})

def login_user(request):
    form = MemberAuthForm()
    if request.method == "POST":
        form = MemberAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login")

@login_required
@staff_member_required
def create_event(request):
    if not request.user.is_staff:
        messages.info(request, f"You can't create an event since you are not a staff member.")
        return redirect("home")
    form = CreateEventForm()
    if request.method == "POST":
        form = CreateEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, 'main/create_event.html', {'form': form})

@login_required
@staff_member_required
def create_clinic(request):
    if not request.user.is_staff:
        messages.info(request, f"You can't create an event since you are not a staff member.")
        return redirect("home")
    form = CreateClinicForm()
    if request.method == "POST":
        form = CreateClinicForm(request.POST)
        if form.is_valid():
            form.save()
            form.instance.update_date_instances()
            messages.success(request, 'You created the clinic successfully.')
            return redirect("home")
        else:

            return HttpResponseBadRequest("Something happened")
    return render(request, 'main/create_clinic.html', {'form': form})

@login_required
@staff_member_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    clinics = Clinic.objects.filter(event__id = event.id)
    form = CreateEventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        messages.success(request, f"You edited the event: {event.title}.")
        return redirect('home')
    return render(request, 'main/edit_event.html', {'event': event, 'clinics': clinics, 'form': form})

@login_required
def edit_profile(request):
    member = request.user
    form = CreateMemberForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        messages.success(request, f"You edited your profile.")
        return redirect('home')
    return render(request, 'main/edit_profile.html', {'form': form})  


@login_required
@staff_member_required
def edit_clinic(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    old_occurrences = list(clinic.recurrences.occurrences(dtend = date_limit))
    form = CreateClinicForm(request.POST or None, instance=clinic)
    event = Event.objects.get(clinic = clinic)
    clinic_dates = Date.objects.filter(clinic = clinic)
    if form.is_valid():
        new_occurrences = list(form.instance.recurrences.occurrences(dtend = date_limit))
        # If the time of the clinic it's changed, then all dates should be deleted
        # and ask the members to sign up for the new dates.
        if form.data['start_time'] != str(clinic.start_time) or \
           form.data['end_time']   != str(clinic.end_time):
                for date in event.get_fut_dates():
                    date.delete()
                form.instance.update_date_instances()
        # Instead, if only some dates were added or deleted,
        # then just these would be manage without deleting all
        # the future dates.
        elif old_occurrences != new_occurrences:
            form.instance.update_date_instances(old_occurrences)
        form.save()
        messages.success(request, f"You edited the clinic: {clinic.title}.")
        return redirect('home')
    
    return render(request, 'main/edit_clinic.html',
     {'event': event,
      'clinic': clinic,
      'dates': clinic_dates,
       'form': form})


@login_required
@staff_member_required
def edit_date(request, date_id):
    date = get_object_or_404(Date, id=date_id)
    form = CreateDateForm(request.POST or None, instance=date)
    if form.is_valid():
        form.save()
        messages.info(request, f"You edited the date: {date}.")
        return redirect('home')
    clinic = Clinic.objects.get(date=date)
    participants = date.get_participants()
    return render(request, 'main/edit_date.html',
     {  'date': date,
        'participants': participants,
        'clinic': clinic,
        'form': form})
    
@login_required
def event(request, event_id):
    event = Event.objects.get(id=event_id)
    dates = event.get_fut_dates(20)
    if dates:
        user_dates = Date.objects.filter(participation__member = request.user).filter(clinic__event = event)
        return render(request, 'main/event.html', {'event': event , 'dates': dates, 'user_dates': user_dates})
    else:
        return redirect("home")

@login_required()
def event_participants(request, event_id):
    event = Event.objects.get(id=event_id)
    participants = []
    # Returns the first date on the list, if empty then it returns None
    next_date = next(iter(event.get_fut_dates(1)), None)
    if next_date:
        participants = next_date.get_participants()
    return render(request, 'main/court_assign.html', {'event': event, 'participants': participants})

@login_required
def add_participant(request):
    if request.method == 'POST':
        dates = request.POST.get('dates', None)
        event = Event.objects.get(id=request.POST.get('event_id', None))
        dates = json.loads(dates)
        # If the user selected some dates.
        if dates:
            # Check the event's gender and they user can sign up for it
            if event.gender != 'MIXED' and event.gender != request.user.gender:
                return HttpResponseBadRequest(f"You can't sign up for an event for {event.get_gender_display()}s.")
            
            # Getting the dates the user already sign up for
            old_reg_dates_ids = list(Date.objects.filter(participation__member = request.user).filter(clinic__event = event).values_list('id', flat=True))
            # Assuming that the current selection of dates is the newest one. Since 'dates' contains
            # the dates the user already registered for and the new ones, if any.  
            new_reg_dates_ids = [int(id) for id in dates]

            # The common subset of the old dates registered and the new ones
            # is the one containing the dates to be deleted or created.
            reg_dates = list(set(old_reg_dates_ids).symmetric_difference(set(new_reg_dates_ids)))
            
            for date_id in reg_dates:
                selected_date = Date.objects.get(id = date_id)
                try: 
                    # If the participation exists in the DB, then it gets deleted. 
                    Participation.objects.get(member=request.user, date=selected_date).delete()
                except Participation.DoesNotExist: 
                    # Otherwise, it gets created. 
                    part = Participation.objects.create(member=request.user, date=selected_date)
                    part.save()
            return JsonResponse({'message': "You have successfully registered for the selected dates."})
        # If the the user didn't select any dates it means that they either unregistered 
        # from all dates or they just forgot to register for any. 
        else:
            old_reg_dates_ids = list(Date.objects.filter(participation__member = request.user).filter(clinic__event = event).values_list('id', flat=True))
            # If the user was already registered for some dates and now 
            # there are no selected dates. It means that he wants so sign out for all of them.
            if old_reg_dates_ids:
                # Then, it deletes all the user's participations for this event.
                for date_id in old_reg_dates_ids:
                    unselected_date = Date.objects.get(id = date_id)
                    Participation.objects.get(member=request.user, date=unselected_date).delete()
                return JsonResponse({'message': "You have successfully unregistered for all the dates."})
            # Otherwise, it prompts a message saying they didn't select any date. 
            else:
                return JsonResponse({'message': "You haven't selected any date."}, status=500)
    else:
        return HttpResponseBadRequest("Not a post")


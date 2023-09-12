from django.shortcuts import render, redirect
from .forms import CreateMemberForm, MemberAuthForm, CreateEventForm, CreateActivityForm, CreateDateForm, UpdateMemberForm, CreateParticipationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from .exceptions import *
from django.http import HttpResponse
from .serializers import *
from django.http import JsonResponse
from .models import Event, Activity, Date, Participation, Court, Member
from datetime import date as datetimedate, datetime
from django.utils.timezone import timedelta, make_aware
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def create_courts():
    if Court.objects.all().count() == 0:
        Court.objects.bulk_create([
            Court(name='Stadium Court'),
            Court(name='Court 1'),
            Court(name='Court 2'),
            Court(name='Court 3'),
            Court(name='Court 4'),
            Court(name='Court 5'),
            Court(name='Court 6'),
            Court(name='Court 7'),
        ])


@login_required
def filter_events(request):
    if request.method == "POST":
        string = request.POST.get('input')
        curr_events = json.loads(request.POST.get('curr_events'))
        events = Event.objects.filter(
            title__in=curr_events).filter(title__icontains=string)
        data = [event.title for event in events]
        return JsonResponse({'data': data})


@login_required
def home(request):
    # Querying all the events that have a next date after today. The next date field takes
    # care of giving the next date based on todays date.
    activities = request.user.get_available_activities()
    return render(request, 'main/home.html', {
        'activities': activities,
        'page_title': 'Events Available',
        'titles': {
            'Registered Dates': request.user.get_fut_participations_registered().count(),
            'Registered Events': request.user.get_fut_events_registered().count(),
            'Events Available': activities.count()
        }
    })


@login_required
def my_activities(request):
    user_activities = request.user.get_fut_activities_registered()
    return render(request, 'main/home.html', {
        'page_title': 'My Activities',
        'activities': user_activities,
        'next_activity': request.user.get_next_activity(),
        'titles': {
            'Registered Dates': request.user.get_fut_participations_registered().count(),
            'Registered Activities': user_activities.count(),
        }
    })


@login_required
@staff_member_required
def edit_all_activities(request):
    all_activities = Activity.objects.all()
    return render(request, 'main/home.html', {
        'page_title': 'All Activities',
        'activities': all_activities,
        'titles': {
            'All Activities': len(all_activities)
        }
    })


def register(request):
    form = CreateMemberForm()
    if request.method == "POST":
        form = CreateMemberForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(
                request, 'Account created. You will login with your email: ' + email)
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
        messages.info(
            request, f"You can't create an event since you are not a staff member.")
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
def create_activity(request):
    form = CreateActivityForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        activity = form.save(commit=False)
        try:
            activity.full_clean()
            activity.save()
            messages.success(
                request, 'You created the activity successfully.')
            return redirect('home')
        except ActivityCreationError as e:
            messages.error(request, e)
    return render(request, 'main/create_activity.html', {'form': form})


@login_required
@staff_member_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = CreateEventForm(request.POST or None, instance=event)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"You edited the event: {event.title}.")
        return redirect('home')
    return render(request, 'main/edit_event.html', {'event': event, 'activities': event.get_activities(), 'form': form})


@login_required
def edit_profile(request):
    form = UpdateMemberForm(instance=request.user)
    if request.method == 'POST':
        form = UpdateMemberForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"You edited your profile.")
            return redirect('home')
    return render(request, 'main/edit_profile.html', {'form': form})


@login_required
@staff_member_required
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    # Check for a DELETE request to delete the activity
    if request.method == "DELETE":
        activity.delete()
        messages.success(
            request, f"The activity '{activity.title}' has been deleted.")
        # Return a success response (HTTP 204 No Content)
        return HttpResponse(status=204)

    form = CreateActivityForm(request.POST or None, instance=activity)

    if request.method == "POST" and form.is_valid():
        try:
            form.full_clean()
            activity.save()
            print(form.instance.recurrences)
            messages.success(
                request, f"You edited the activity: {activity.title}.")
            return redirect('home')
        except ActivityUpdateError as e:
            messages.error(request, e)

    return render(request, 'main/edit_activity.html', {
        'event': activity.event,
        'activity': activity,
        'dates': activity.get_all_dates(),
        'form': form
    })


@login_required
@staff_member_required
def edit_date(request, date_id):
    date = get_object_or_404(Date, id=date_id)
    form = CreateDateForm(request.POST or None, instance=date)
    if form.is_valid():
        form.save()
        form.instance.update_courts()
        messages.success(request, f"You edited the date: {date}.")
        return redirect("home")
    return render(request, 'main/edit_date.html',
                  {'date': date,
                   'activity': date.get_activity(),
                   'form': form})


@login_required
def event(request, event_id):
    event = Event.objects.get(id=event_id)
    dates = event.get_fut_dates(20)
    if dates:
        user_dates = Date.objects.filter(
            participation__member=request.user).filter(activity__event=event)
        return render(request, 'main/event.html', {'event': event, 'dates': dates, 'user_dates': user_dates})
    else:
        return redirect("home")


@login_required()
def event_participants(request, event_id):
    event = Event.objects.get(id=event_id)
    on_wait = []
    # Returns the first date on the list, if empty then it returns None
    next_date = event.get_next_date()
    if next_date:
        on_wait = next_date.get_parts_on_wait()
    return render(request, 'main/court_assign.html', {
        'event': event,
        'on_court': next_date.get_parts_on_court(),
        'on_wait': on_wait})


def add_participant(request):
    if request.method == 'POST':
        form = CreateParticipationForm(request.POST)
        if form.is_valid():
            event = get_object_or_404(Event, id=form.cleaned_data['event_id'])
            dates = json.loads(form.cleaned_data['dates'])
            if dates:
                handle_dates(request, event, dates)
            else:
                handle_no_dates(request, event)
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        return HttpResponseBadRequest("Not a post")


def handle_dates(request, event, dates):
    # Check the event's gender and they user can sign up for it
    if event.gender != 'MIXED' and event.gender != request.user.gender:
        return JsonResponse({'message': f"You can't sign up for an event for {event.get_gender_display()}s."}, status=403)

    # Getting the dates the user already sign up for
    old_reg_dates_ids = list(Date.objects.filter(participation__member=request.user).filter(
        activity__event=event).values_list('id', flat=True))
    # Assuming that the current selection of dates is the newest one. Since 'dates' contains
    # the dates the user already registered for and the new ones, if any.
    new_reg_dates_ids = [int(id) for id in dates]

    # The common subset of the old dates registered and the new ones
    # is the one containing the dates to be deleted or created.
    reg_dates = list(set(old_reg_dates_ids).symmetric_difference(
        set(new_reg_dates_ids)))

    for date_id in reg_dates:
        selected_date = Date.objects.get(id=date_id)
        try:
            # If the participation exists in the DB, then it gets deleted.
            Participation.objects.get(
                member=request.user, date=selected_date).delete()
        except Participation.DoesNotExist:
            # Otherwise, it gets created.
            part = Participation.objects.create(
                member=request.user, date=selected_date)
            part.save()
    return JsonResponse({'message': "You have successfully registered for the selected dates."})
    # If the the user didn't select any dates it means that they either unregistered
    # from all dates or they just forgot to register for any.


def handle_no_dates(request, event):
    old_reg_dates_ids = list(Date.objects.filter(participation__member=request.user).filter(
        activity__event=event).values_list('id', flat=True))
    # If the user was already registered for some dates and now
    # there are no selected dates. It means that he wants so sign out for all of them.
    if old_reg_dates_ids:
        # Then, it deletes all the user's participations for this event.
        for date_id in old_reg_dates_ids:
            unselected_date = Date.objects.get(id=date_id)
            Participation.objects.get(
                member=request.user, date=unselected_date).delete()
        return JsonResponse({'message': "You have successfully unregistered for all the dates."})
    # Otherwise, it prompts a message saying they didn't select any date.
    else:
        return JsonResponse({'message': "You haven't selected any date."}, status=500)


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
                return JsonResponse({'message': f"You can't sign up for an event for {event.get_gender_display()}s."}, status=403)

            # Getting the dates the user already sign up for
            old_reg_dates_ids = list(Date.objects.filter(participation__member=request.user).filter(
                activity__event=event).values_list('id', flat=True))
            # Assuming that the current selection of dates is the newest one. Since 'dates' contains
            # the dates the user already registered for and the new ones, if any.
            new_reg_dates_ids = [int(id) for id in dates]

            # The common subset of the old dates registered and the new ones
            # is the one containing the dates to be deleted or created.
            reg_dates = list(set(old_reg_dates_ids).symmetric_difference(
                set(new_reg_dates_ids)))

            for date_id in reg_dates:
                selected_date = Date.objects.get(id=date_id)
                try:
                    # If the participation exists in the DB, then it gets deleted.
                    Participation.objects.get(
                        member=request.user, date=selected_date).delete()
                except Participation.DoesNotExist:
                    # Otherwise, it gets created.
                    part = Participation.objects.create(
                        member=request.user, date=selected_date)
                    part.save()
            return JsonResponse({'message': "You have successfully registered for the selected dates."})
        # If the the user didn't select any dates it means that they either unregistered
        # from all dates or they just forgot to register for any.
        else:
            old_reg_dates_ids = list(Date.objects.filter(participation__member=request.user).filter(
                activity__event=event).values_list('id', flat=True))
            # If the user was already registered for some dates and now
            # there are no selected dates. It means that he wants so sign out for all of them.
            if old_reg_dates_ids:
                # Then, it deletes all the user's participations for this event.
                for date_id in old_reg_dates_ids:
                    unselected_date = Date.objects.get(id=date_id)
                    Participation.objects.get(
                        member=request.user, date=unselected_date).delete()
                return JsonResponse({'message': "You have successfully unregistered for all the dates."})
            # Otherwise, it prompts a message saying they didn't select any date.
            else:
                return JsonResponse({'message': "You haven't selected any date."}, status=500)
    else:
        return HttpResponseBadRequest("Not a post")


def calendar_resolver(request):
    if 'date' in request.GET:
        # Date is provided in the URL, pass it to the filter_activities_by_date view
        date = request.GET['date']
        return redirect(reverse('calendar_view', kwargs={'date': date}))
    else:
        # Date is not provided, redirect to /calendar/<today's date>
        today = datetimedate.today().strftime('%Y-%m-%d')
        return redirect(reverse('calendar_view', kwargs={'date': today}))


def calendar_view(request, date):
    # Convert the provided date string to a datetime object
    try:
        filter_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        # Handle invalid date format
        # Redirect or return an error message
        return render(request, 'main/home.html', {'message': 'Invalid date format'})
    # Filter activities based on the provided date
    dates = Date.objects.filter(
        datetime_start__contains=filter_date).select_related('activity')

    dates_list = []
    for date in dates:
        activity = date.activity
        duration = (date.datetime_end -
                    date.datetime_start).total_seconds() / (30 * 60)
        host = None
        if activity.type == Activity.TYPE_COURT:
            first_participation = date.participation.order_by(
                'date_registered').first()

            if first_participation:
                host = str(first_participation.member)

        # Get the list of court names using values_list()
        courts_list = list(date.court.values_list('name', flat=True))
        pros_list = [serialize_pro(pro) for pro in date.assigned_pros.all()]
        date_dict = {
            'host': host,
            'datetime_start': date.datetime_start.isoformat(),
            'datetime_end': date.datetime_end.isoformat(),
            'pros': pros_list,
            'capacity': date.capacity,
            'court': courts_list,
            'duration': duration,
            'activity': {
                'type': activity.type,
                'title': activity.title,
                'start_time': str(activity.start_time),
                'end_time': str(activity.end_time),
                'capacity': activity.capacity,
                'is_active': activity.is_active,
            }
        }

        dates_list.append(date_dict)

    dates_json = json.dumps(dates_list)
    return render(request, 'main/calendar.html', {'date': filter_date, 'dates': dates_json})


def calculate_datetime_range(date_str, time_str, duration_minutes):
    # Parse the input date and time strings
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    time_obj = datetime.strptime(time_str, '%H:%M')

    # Calculate the datetime_start using the parsed date and time
    datetime_start = date_obj.replace(
        hour=time_obj.hour, minute=time_obj.minute)

    # Calculate the datetime_end by adding the duration in minutes
    datetime_end = datetime_start + timedelta(minutes=int(duration_minutes))

    return datetime_start, datetime_end


def get_available_pros(request):
    # Get the selected time from the request
    date = request.GET.get('date')
    time = request.GET.get('time')
    duration = request.GET.get('duration')
    datetime_start, datetime_end = calculate_datetime_range(
        date, time, duration)
    datetime_start = make_aware(datetime_start)
    datetime_end = make_aware(datetime_end)

    # Find the Pros (Members) who do not have a Participation in overlapping Dates
    available_pros = Member.get_available_pros(datetime_start, datetime_end)

    # Convert the queryset to a list of dictionaries
    pros_list = [{'id': pro.id, 'name': str(
        pro), 'color': pro.color} for pro in available_pros]

    return JsonResponse({'pros': pros_list})


def convert_to_rdate(input_date_str):
    try:
        # Parse the input date string
        input_date = datetime.strptime(input_date_str, "%Y-%m-%d")
        print(input_date)

        # Format the date-time in ISO 8601 with UTC
        iso8601_utc_date_str = input_date.strftime("%Y%m%dT050000Z")

        print(iso8601_utc_date_str)
        # Combine with "RDATE" prefix
        rdate_str = "RDATE:" + iso8601_utc_date_str

        return rdate_str
    except ValueError:
        # Handle invalid input date strings gracefully
        return None


def add_start_end_times(input_dict):
    if 'time' in input_dict and 'duration' in input_dict:
        # Parse the time from the 'time' key
        time_str = input_dict['time']
        start_time = datetime.strptime(time_str, '%H:%M').time()

        # Parse the duration from the 'duration' key and calculate end time
        duration_minutes = int(input_dict['duration'])
        end_time = (datetime.combine(datetime.today(), start_time) +
                    timedelta(minutes=duration_minutes)).time()

        # Add 'start_time' and 'end_time' to the dictionary
        input_dict['start_time'] = start_time
        input_dict['end_time'] = end_time

        keys_to_remove = ['time', 'duration',
                          'pro', 'court', 'date', 'proName']
        for key in keys_to_remove:
            input_dict.pop(key, None)

    return input_dict


def activity_dict_to_data(request, dict):
    data = dict.copy()
    data['title'] = str(request.user)
    try:
        data['recurrences'] = convert_to_rdate(data['date'])
        data = add_start_end_times(data)
    except ValueError:
        print("There was an error with convert")
    return data


def calendar_create_activity(request):
    # It handles activity creation from the calendar view
    if request.method == 'POST':
        try:
            passed_dict = json.loads(json.loads(request.body.decode('utf-8')))
            act_data = activity_dict_to_data(request, passed_dict)
            print(act_data)
            activity = Activity(**act_data)
            activity.save(court=passed_dict['court'])
            date = activity.get_next_date()
            Participation.objects.create(date=date, member=request.user)
            if 'pro' in passed_dict:
                date.assigned_pros.add(
                    Member.objects.get(id=passed_dict['pro']))
            return JsonResponse({'success': 'Activity created!'})
        except:
            return JsonResponse({'error': 'There was an error creating the activity'})
    return JsonResponse({'error': 'Invalid request method'})

from unicodedata import name
from django.test import TestCase
from .models import Event, Venue, Member, Participation
import datetime
from django.utils.timezone import make_aware
from django.db import IntegrityError
import datetime
import pytest

@pytest.mark.parametrize(
    'gender', 
    [
        ('Male')
    ])


def test_event_gender(db, gender):
    date = datetime.datetime.strptime('09/19/18 13:55:26', '%m/%d/%y %H:%M:%S')
    date = make_aware(date)
    tokeneke = Venue.objects.create(name="Tokeneke Club", address="4 Butler Island Rd, Darien", zip_code='06820', phone='(203) 655-1481', web='https://www.tokenekeclub.org/', email='office@tokenekeclub.org')
    mg = Event.objects.create(name="Member Guest", date=date, venue=tokeneke, duration=datetime.timedelta(hours=5), gender=gender)
    faycal = Member.objects.create(
        email="faycal@gmail.com",
        member_n="F120",
        first_name='Faycal',
        last_name='Rhazali',
        gender='Male',
        team='No-Team')
    
    Participation.objects.create(member=faycal, event=mg)
    assert mg.participants.count() == 1





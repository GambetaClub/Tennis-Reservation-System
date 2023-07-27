from django.test import TestCase
from ..models import *
from datetime import datetime, time
from django.utils.timezone import make_aware, get_current_timezone
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone


class TestParticipation(TestCase):
    def setUp(self):
        Member.objects.create(
            email="maj_jalif@gmail.com",
            member_n="M123",
            first_name="Mariano",
            last_name="Jalif",
            gender="M"
        )
        Member.objects.create(
            email="sherine.salem@gmail.com",
            member_n="S123",
            first_name="Sherine",
            last_name="Salem",
            gender="F"
        )

        event = Event.objects.create(
            title="Men's Afternoon Clinic",
            description="Only for Men",
            gender="M",
            team="No Team"
        )

        clinic = Activity.objects.create(
            event=event,
            title="Clinic for Men's Afternoon",
            recurrences="RRULE:FREQ=WEEKLY;BYDAY=TU",
            start_time=datetime.time(8, 30, 00),
            end_time=datetime.time(9, 30, 00),
            capacity=8
        )

        clinic.update_date_instances()

    def test_member_diff_sex_cant_register(self):
        """Identifies the registration for different members gender"""
        mariano = Member.objects.get(first_name="Mariano")
        sherine = Member.objects.get(first_name="Sherine")
        mens_clinic = Activity.objects.get(title="Clinic for Men's Afternoon")
        next_date = mens_clinic.get_fut_dates(1)[0]

        with self.assertRaises(ValidationError):
            Participation.objects.create(member=sherine, date=next_date)

        # Create a participation for Mariano for the next date of Clinic


class ModelsTestCase(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            email='test@example.com', first_name='John', last_name='Doe', gender='M')
        self.event = Event.objects.create(
            title='Test Event', gender='M', team='A')
        self.activity = Activity.objects.create(
            type='private', title='Test Private Lesson', start_time=time(7, 0, 0, 0, tzinfo=get_current_timezone()), end_time=time(8, 30, 0, 0, tzinfo=get_current_timezone()), capacity=4)
        datetime_start = make_aware(datetime(
            2033, 11, 17, 7, 0, 0, 0), get_current_timezone())
        datetime_end = make_aware(datetime(
            2033, 11, 17, 8, 30, 0, 0), get_current_timezone())
        self.date = Date.objects.create(
            activity=self.activity, datetime_start=datetime_start, datetime_end=datetime_end, capacity=4)

    def test_member_str(self):
        self.assertEqual(str(self.member), 'John D.')

    def test_event_str(self):
        self.assertEqual(str(self.event), 'Test Event')

    def test_activity_str(self):
        self.assertEqual(str(self.activity),
                         'Test Private Lesson - On ' + self.date.print_start_date())

    def test_date_str(self):
        self.assertEqual(str(self.date), self.date.print_start_date(
        ) + ' for ' + self.activity.get_title())

    def test_date_get_registered_count(self):
        self.assertEqual(self.date.get_registered_count(), 0)

    def test_date_get_rem_spots(self):
        self.assertEqual(self.date.get_rem_spots(), 4)

    # def test_participation_save(self):
    #     participation = Participation(member=self.member, date=self.date)
    #     with self.assertRaises(ValidationError):
    #         participation.save()

    def test_participation_get_event(self):
        participation = Participation(member=self.member, date=self.date)
        participation.save()
        self.assertEqual(participation.get_greater_parent(), self.event)

    # def test_participation_str(self):
    #     participation = Participation(member=self.member, date=self.date)
    #     self.assertEqual(str(participation), str(
    #         self.member) + ' for ' + str(self.date))

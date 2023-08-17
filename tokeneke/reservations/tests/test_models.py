from django.test import TestCase
from ..models import *
from datetime import datetime, time, timedelta
from django.db.utils import IntegrityError
from django.utils.timezone import make_aware, get_current_timezone
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestParticipation(TestCase):
    def setUp(self):
        self.mariano = Member.objects.create(
            email="maj_jalif@gmail.com",
            member_n="M123",
            first_name="Mariano",
            last_name="Jalif",
            gender=Member.GENDER_MALE,
        )
        self.sherine = Member.objects.create(
            email="sherine.salem@gmail.com",
            member_n="S123",
            first_name="Sherine",
            last_name="Salem",
            gender=Member.GENDER_FEMALE,
        )

        self.event = Event.objects.create(
            title="Men's Afternoon Clinic",
            description="Only for Men",
            gender=Event.EVENT_MALE,
            team=Event.NO_TEAM,
        )

        self.clinic = Activity.objects.create(
            event=self.event,
            title="Clinic for Men's Afternoon",
            type=Activity.TYPE_CLINIC,
            recurrences="RRULE:FREQ=WEEKLY;BYDAY=TU",
            start_time=time(8, 30, 00),
            end_time=time(9, 30, 00),
            capacity=8
        )

        self.next_date = self.clinic.get_next_date()

    def test_member_diff_sex_cant_register(self):
        """Identifies the registration for different members gender"""
        with self.assertRaises(ValidationError):
            Participation.objects.create(
                member=self.sherine, date=self.next_date)
        Participation.objects.create(member=self.mariano, date=self.next_date)


class ModelsTestCase(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            email='test@example.com', first_name='John', last_name='Doe', gender='M')
        self.event = Event.objects.create(
            title='Test Event', gender='M', team='A')
        self.activity = Activity.objects.create(
            type='private', title='Test Private Lesson', recurrences="RRULE:FREQ=WEEKLY;COUNT=2;BYDAY=MO,TH,SA", start_time=time(7, 0, 0, 0, tzinfo=get_current_timezone()), end_time=time(8, 30, 0, 0, tzinfo=get_current_timezone()), capacity=4)
        self.date = self.activity.get_next_date()

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

    def test_participation_save(self):
        participation = Participation(member=self.member, date=self.date)
        participation.save()

    def test_participation_get_event(self):
        participation = Participation(member=self.member, date=self.date)
        participation.save()
        self.assertEqual(participation.get_greater_parent(), self.activity)

    def test_participation_str(self):
        participation = Participation(member=self.member, date=self.date)
        self.assertEqual(str(participation), str(
            self.member) + ' for ' + str(self.date))


class MemberModelGeneralTestCase(TestCase):
    def generate_member_data(self, email_suffix):
        member_data = {
            'email': f'test_{email_suffix}@example.com',
            'member_n': '12345',
            'first_name': 'John',
            'last_name': 'Doe',
            'level': 80,
            'gender': Member.GENDER_MALE,
            'team': Member.TEAM_A,
            'is_playing': True,
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }
        return member_data

    def test_create_member(self):
        email_suffix = 'gambeta'
        member_data = self.generate_member_data(email_suffix=email_suffix)
        member = Member.objects.create(**member_data)
        self.assertEqual(member.email, f'test_{email_suffix}@example.com')
        self.assertEqual(member.member_n, '12345')
        self.assertEqual(member.first_name, 'John')
        self.assertEqual(member.last_name, 'Doe')
        self.assertEqual(member.level, 80)
        self.assertEqual(member.gender, Member.GENDER_MALE)
        self.assertEqual(member.team, Member.TEAM_A)
        self.assertTrue(member.is_playing)
        self.assertTrue(member.is_active)
        self.assertFalse(member.is_staff)
        self.assertFalse(member.is_superuser)

    def test_member_str_representation(self):
        member_data = self.generate_member_data('str_rep')
        member = Member.objects.create(**member_data)
        self.assertEqual(str(member), 'John D.')

    def test_member_default_profile_pic(self):
        member_data = self.generate_member_data('profile_pic')
        member = Member.objects.create(**member_data)
        self.assertEqual(member.profile_pic, 'profile_pics/default.jpeg')

    def test_member_start_date(self):
        member_data = self.generate_member_data('start_date')
        member = Member.objects.create(**member_data)
        self.assertIsNotNone(member.start_date)

    def test_custom_manager(self):
        member_count = Member.objects.count()
        self.assertEqual(member_count, 0)

        member_data = self.generate_member_data('custom_manager')
        Member.objects.create(**member_data)

        self.assertEqual(Member.objects.count(), 1)

    def test_team_choices(self):
        for index, team_choice in enumerate(Member.TEAM_CHOICES):
            member_data = self.generate_member_data(f'team_{index}')
            member_data['team'] = team_choice[0]
            Member.objects.create(**member_data)
        self.assertEqual(Member.objects.count(), len(Member.TEAM_CHOICES))

    def test_gender_choices(self):
        for index, gender_choice in enumerate(Member.GENDER_CHOICES):
            member_data = self.generate_member_data(f'gender_{index}')
            member_data['gender'] = gender_choice[0]
            Member.objects.create(**member_data)
        self.assertEqual(Member.objects.count(), len(Member.GENDER_CHOICES))


class MemberModelSpecificTestCase(TestCase):
    def setUp(self):
        self.member_data = {
            'email': 'test@example.com',
            'member_n': '12345',
            'first_name': 'John',
            'last_name': 'Doe',
            'level': None,
            'gender': Member.GENDER_MALE,
            'team': Member.TEAM_A,
            'is_playing': True,
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }
        self.member = Member.objects.create(**self.member_data)

        self.event = Event.objects.create(
            title="Men's Morning Clinic",
            description="Only for Men",
            gender="M",
            team="No Team"
        )

        self.dates_count = 1000
        self.activity_data = {
            "event": self.event,
            "title": "Clinic for Men's Morning",
            "type": Activity.TYPE_CLINIC,
            "recurrences": f"RRULE:FREQ=WEEKLY;COUNT={self.dates_count};BYDAY=MO,TH,SA",
            "start_time": time(8, 30, 00),
            "end_time": time(9, 30, 00),
            "capacity": 8
        }

        self.activity = Activity.objects.create(**self.activity_data)

        self.courts = Court.objects.bulk_create([
            Court(name='Stadium'),
            Court(name='Court1'),
            Court(name='Court2'),
            Court(name='Court3'),
            Court(name='Court4'),
            Court(name='Court5'),
            Court(name='Court6'),
            Court(name='Court7'),
        ])

        # Creating a participation for the next date of the activity.
        self.next_date = Participation.objects.create(
            member=self.member, date=self.activity.get_next_date())

    def test_str_representation(self):
        self.assertEqual(str(self.member), 'John D.')

    def test_str_representation_no_name(self):
        self.member.first_name = None
        self.member.last_name = 'Jalif'
        self.assertEqual(str(self.member), 'test@example.com')

    def test_str_representation_no_lastname(self):
        self.member.first_name = 'Mariano'
        self.member.last_name = None
        self.assertEqual(str(self.member), 'test@example.com')

    def test_get_fut_participations_registered(self):
        self.assertIn(
            self.next_date, self.member.get_fut_participations_registered())

    def test_get_fut_activities_registered(self):
        self.assertIn(
            self.activity, self.member.get_fut_activities_registered())

    def get_fut_events_registered(self):
        self.assertIn(
            self.event, self.member.get_fut_events_registered())

    def test_double_participation(self):
        with self.assertRaises(IntegrityError):
            duplicate_participation = Participation.objects.create(
                member=self.member, date=self.activity.get_fut_dates(1)[0])

    def test_get_available_activities(self):
        self.assertIn(
            self.activity, self.member.get_available_activities())

    def test_get_level(self):
        self.member.level = 50
        self.assertEqual(self.member.get_level(), 50)

    def test_get_level_default(self):
        self.assertEqual(self.member.get_level(), 0)


class EventModelTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title="Ladies' Morning Clinic",
            description="Only for Women",
            gender=Event.EVENT_FEMALE,
            team=Event.NO_TEAM,
        )
        self.activity_data = {
            "event": self.event,
            "title": "Clinic for Men's Morning",
            "type": Activity.TYPE_CLINIC,
            "recurrences": f"RRULE:FREQ=WEEKLY;BYDAY=MO,TH,SA",
            "start_time": time(8, 30, 00),
            "end_time": time(9, 30, 00),
            "capacity": 8
        }
        self.activity = Activity.objects.create(**self.activity_data)

    def test_str_representation(self):
        self.assertEqual(str(self.event), self.event.title)

    def test_get_activities(self):
        activities = self.event.get_activities()
        self.assertIn(self.activity, activities)

    def test_get_fut_dates(self):
        future_dates = self.event.get_fut_dates()
        self.assertTrue(future_dates)
        for date in future_dates:
            self.assertTrue(date.datetime_start >= timezone.now())

    def test_get_fut_dates_empty(self):
        # Test when there are no future dates
        self.activity.date_set.all().delete()
        future_dates = self.event.get_fut_dates()
        self.assertFalse(future_dates)

    def test_get_next_date(self):
        next_date = self.event.get_next_date()
        self.assertTrue(next_date)
        self.assertTrue(next_date.datetime_start >= timezone.now())

    def test_get_next_date_none(self):
        # Test when there are no future dates
        self.activity.date_set.all().delete()
        next_date = self.event.get_next_date()
        self.assertIsNone(next_date)


class CourtModelTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title="Ladies' Morning Clinic",
            description="Only for Women",
            gender=Event.EVENT_FEMALE,
            team=Event.NO_TEAM,
        )

        self.activity_time_start = time(8, 30, 00)
        self.activity_time_end = time(10, 00, 00)
        self.activity_data = {
            "event": self.event,
            "title": "Clinic for Men's Morning",
            "type": Activity.TYPE_CLINIC,
            "recurrences": f"RRULE:FREQ=WEEKLY;BYDAY=MO",
            "start_time": self.activity_time_start,
            "end_time": self.activity_time_end,
            "capacity": 10
        }
        self.activity = Activity.objects.create(**self.activity_data)
        self.courts = Court.objects.all()

    def get_next_monday(self, time):
        today = datetime.now()
        days_until_next_monday = (7 - today.weekday() + 0) % 7

        if days_until_next_monday == 0:
            days_until_next_monday = 7

        next_monday = today + timedelta(days=days_until_next_monday)
        next_monday = next_monday.replace(
            hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond)

        next_monday = make_aware(next_monday)
        return next_monday

    def test_str_representation(self):
        stadium_court = Court.objects.get(name=Court.STADIUM_COURT)
        self.assertEqual(str(stadium_court), Court.STADIUM_COURT)

    def test_get_open_courts(self):
        datetime_start = self.get_next_monday(self.activity_time_start)
        datetime_end = self.get_next_monday(self.activity_time_end)
        n_courts_used = math.ceil(self.activity.capacity / MAX_P_P_COURT)
        n_courts_available = Court.objects.all().count() - n_courts_used
        print(n_courts_used)
        self.assertEqual(len(Court.get_open_courts(
            datetime_start, datetime_end)), n_courts_available)


class ActivityModelTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title="Ladies' Morning Clinic",
            description="Only for Women",
            gender=Event.EVENT_FEMALE,
            team=Event.NO_TEAM,
        )
        self.dates_count = 10
        self.activity_data = {
            "event": self.event,
            "title": "Clinic for Men's Morning",
            "type": Activity.TYPE_CLINIC,
            "recurrences": f"RRULE:FREQ=WEEKLY;COUNT={self.dates_count};BYDAY=MO",
            "start_time": time(8, 30, 00),
            "end_time": time(9, 30, 00),
            "capacity": 8
        }
        self.activity = Activity.objects.create(**self.activity_data)

    def test_activity_dates_creation(self):
        self.assertIsNotNone(self.activity.date_set.all())

    def test_activity_update_on_capacity(self):
        self.assertEqual(self.activity.get_next_date().capacity, 8)
        self.activity.capacity = 33
        with self.assertRaises(ValueError):
            self.activity.save()
        saved_activity = Activity.objects.get(pk=self.activity.pk)
        self.assertEqual(saved_activity.capacity, 8)
        self.assertEqual(self.activity.get_next_date().capacity, 8)

    def test_activity_save(self):
        activity = Activity.objects.create(**self.activity_data)
        activity.capacity = 12
        activity.save()

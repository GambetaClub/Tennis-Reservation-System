from django.test import TestCase
from ..models import *
import datetime
from django.core.exceptions import ValidationError

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
        
        clinic = Clinic.objects.create(
            event=event, 
            title = "Clinic for Men's Afternoon",
            recurrences="RRULE:FREQ=WEEKLY;BYDAY=TU",
            start_time = datetime.time(8, 30, 00),
            end_time = datetime.time(9, 30, 00),
            capacity = 8
        )

        clinic.update_date_instances()


        

    def test_member_diff_sex_cant_register(self):
        """Identifies the registration for different members gender"""
        mariano = Member.objects.get(first_name="Mariano")
        sherine = Member.objects.get(first_name="Sherine")
        mens_clinic = Clinic.objects.get(title= "Clinic for Men's Afternoon")
        next_date = mens_clinic.get_fut_dates(1)[0]
        
        with self.assertRaises(ValidationError):
            Participation.objects.create(member=sherine, date=next_date)

    
        # Create a participation for Mariano for the next date of Clinic

        
        


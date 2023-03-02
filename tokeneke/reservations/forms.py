from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Member, Event, Participation, Clinic, Date
from django import forms
from django.forms import TextInput, Textarea, Select, CheckboxInput, TimeInput, DateTimeInput, MultipleChoiceField
from django.core.exceptions import ValidationError


class TimePickerInput(forms.TimeInput):
        input_type = 'time'

class CreateMemberForm(UserCreationForm):
    member_n = forms.CharField(max_length=10, widget=forms.TextInput, label="Member Number")
    profile_pic = forms.ImageField(required = False, label="Profile Picture")
    class Meta:
        model = Member
        fields = ['email', 'first_name', 'last_name', 'profile_pic', 'gender', 'member_n', 'password1', 'password2']

class CreateParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['member', 'date']


    def clean(self):
        cleaned_data = super().clean()
        member = cleaned_data.get('member')
        date = cleaned_data.get('date')
        event = date.get_event()
        if event.gender != 'MIXED' and event.gender != member.gender:
            raise ValidationError(f"{str(member)} can't participate in a event for {event.get_gender_display().lower()}s.")
        return cleaned_data

class MemberAuthForm(AuthenticationForm):
    class Meta:
        model = Member
        fields = ['email', 'password']

class CreateDateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = ['clinic', 'datetime_start', 'datetime_end', 'capacity', 'participants']

        widgets = {
            'clinic': Select(attrs={'class': 'form-control'}),
            'datetime_start': DateTimeInput(attrs={'class': 'form-control'}),
            'datetime_end': DateTimeInput(attrs={'class': 'form-control'}),
            'capacity': TextInput(attrs={'type': 'number', 'class': 'form-control'}),
            'participants': forms.CheckboxSelectMultiple(),
        }

class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'gender', 'team']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'gender': Select(attrs={'class': 'form-control'}),
            'team': Select(attrs={'class': 'form-control'})
        }
    

class CreateClinicForm(forms.ModelForm):  
    class Meta:
        model = Clinic
        fields = ['title', 'recurrences', 'start_time', 'end_time', 'capacity', 'event', 'is_active']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'start_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': TextInput(attrs={'type': 'time', 'class': 'form-control'}),
            'capacity': TextInput(attrs={'type': 'number', 'class': 'form-control'}),
            'event': Select(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'form-control'}),
        }


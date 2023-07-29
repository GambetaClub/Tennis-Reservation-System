from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import Member, Event, Participation, Activity, Date
from django import forms
from django.forms import TextInput, Textarea, Select, CheckboxInput, TimeInput, DateTimeField, SplitDateTimeField, DateTimeInput
from django.core.exceptions import ValidationError


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class CreateMemberForm(UserCreationForm):
    member_n = forms.CharField(
        max_length=10, widget=forms.TextInput, label="Member Number")
    profile_pic = forms.ImageField(required=False, label="Profile Picture")

    class Meta:
        model = Member
        fields = ['email', 'first_name',
                  'last_name', 'profile_pic', 'member_n']


class UpdateMemberForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name',
                  'email', 'member_n', 'profile_pic']

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'member_n': TextInput(attrs={'class': 'form-control'}),
        }


class CreateParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['member', 'date']

    def clean(self):
        cleaned_data = super().clean()
        member = cleaned_data.get('member')
        date = cleaned_data.get('date')
        activity = date.get_activity()
        if activity.has_event():
            if activity.event.gender != 'MIXED' and activity.event.gender != member.gender:
                raise ValidationError(
                    f"{str(member)} can't participate in a event for {activity.get_gender_display().lower()}s.")
        return cleaned_data


class MemberAuthForm(AuthenticationForm):
    class Meta:
        model = Member
        fields = ['email', 'password']


class CreateDateAdminForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = ['activity', 'datetime_start', 'datetime_end',
                  'capacity', 'court', 'participants']

    def clean(self):
        cleaned_data = super().clean()

        datetime_start = cleaned_data.get('datetime_start')
        datetime_end = cleaned_data.get('datetime_end')
        court = cleaned_data.get('court')

        # Check for overlapping dates
        overlapping_dates = Date.objects.filter(
            # Dates are for the same court
            court__in=court,
            # The start is before this date's end
            datetime_start__lt=datetime_end,
            # The end is after this date's start
            datetime_end__gt=datetime_start
        )

        if self.instance.pk:  # if instance exists, exclude it from the queryset
            overlapping_dates = overlapping_dates.exclude(pk=self.instance.pk)

        if overlapping_dates.exists():
            raise ValidationError(
                'There is an overlapping date on the same court.')

        return cleaned_data


class CreateDateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = '__all__'

        widgets = {
            'activity': Select(attrs={'class': 'form-control'}),
            'datetime_start': TextInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'datetime_end': TextInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'capacity': TextInput(attrs={'type': 'number', 'class': 'form-control'}),
            'court':  forms.CheckboxSelectMultiple(),
            'participants': forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()

        datetime_start = cleaned_data.get('datetime_start')
        datetime_end = cleaned_data.get('datetime_end')
        court = cleaned_data.get('court')

        # If these variables are None, that means validation failed for these fields. So, we can skip the overlap check.
        if datetime_start is not None and datetime_end is not None and court is not None:
            # Check for overlapping dates
            overlapping_dates = Date.objects.filter(
                # Dates are for the same court
                court__in=court,
                # The start is before this date's end
                datetime_start__lt=datetime_end,
                # The end is after this date's start
                datetime_end__gt=datetime_start
            )

            if self.instance.pk:  # if instance exists, exclude it from the queryset
                overlapping_dates = overlapping_dates.exclude(
                    pk=self.instance.pk)

            if overlapping_dates.exists():
                self.add_error(
                    'court', 'There is an overlapping date on the same court.')

        return cleaned_data


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


class CreateActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'recurrences', 'start_time', 'type',
                  'end_time', 'capacity', 'event', 'is_active']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'start_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': TextInput(attrs={'type': 'time', 'class': 'form-control'}),
            'capacity': TextInput(attrs={'type': 'number', 'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),
            'event': Select(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'form-control'}),
        }

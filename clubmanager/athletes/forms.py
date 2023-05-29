from django.forms import ModelForm
from .models import User, Athlete, Eventsignup, Groups, Event, ClassTime, Attendance
from django.forms.models import inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.forms import modelformset_factory
from email.policy import default
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


class AthleteForm(ModelForm):
    class Meta:
        model = Athlete
        fields = ['first_name', 'last_name', 'group', 'dob', 'year', 'phonenumber', 'weight', 'email', 'gender', 'address', 'school', 'contact', 'contactnumber', 'gpa', 'goals', 'transcript', 'usaw']

class GroupForm(ModelForm):
    class Meta:
        model = Groups
        fields = ['name']

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'location', 'description', 'date_start', 'date_end']

class AthleteEventForm(ModelForm):
    class Meta:
        model = Eventsignup
        fields = ['athlete', 'event', 'transportation']

class AthleteEventForm2(ModelForm):
    class Meta:
        model = Eventsignup
        fields = ['event', 'transportation']

class ClassTimeForm(ModelForm):
    class Meta:
        model = ClassTime
        fields = ['date']

class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ['classtime','athlete_id']

class AttendanceForm2(ModelForm):
    class Meta:
        model = Attendance
        fields = ['mark_attendance'] #'classtime','athlete_id',

class AthleteSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)

    group = forms.ModelChoiceField(
        queryset=Groups.objects.all(),
        required=True
    )

    dob = forms.DateField()
    address = forms.CharField(max_length=250)
    year = forms.IntegerField()
    phonenumber = forms.CharField(max_length=12)
    weight = forms.IntegerField()
    email = forms.CharField(max_length=250)
    gender = forms.ChoiceField(
        choices=(('Male','Male'), ('Female','Female')),
        required=True
    )
    usaw = forms.ImageField(required=False)
    school = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250)
    contactnumber = forms.CharField(max_length=12)
    gpa = forms.DecimalField(decimal_places=2, max_digits=3)
    transcript = forms.ImageField(required=False)
    goals = forms.CharField(max_length=400)



    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_athlete = True
        user.save()
        
        athlete = Athlete(
            user=user,
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name'],
            group = self.cleaned_data['group'],
            dob = self.cleaned_data['dob'],
            address = self.cleaned_data['address'],
            year = self.cleaned_data['year'],
            phonenumber = self.cleaned_data['phonenumber'],
            weight = self.cleaned_data['weight'],
            email = self.cleaned_data['email'],
            gender = self.cleaned_data['gender'],
            usaw = self.cleaned_data['usaw'],
            school = self.cleaned_data['school'],
            contact = self.cleaned_data['contact'],
            contactnumber = self.cleaned_data['contactnumber'],
            gpa = self.cleaned_data['gpa'],
            transcript = self.cleaned_data['transcript'],
            goals = self.cleaned_data['goals'],
        )
        # athlete.first_name = self.cleaned_data['first_name']
        # athlete.last_name = self.cleaned_data['last_name']
        # athlete.group = self.cleaned_data['group']
        # athlete.dob = self.cleaned_data['dob']
        # athlete.address = self.cleaned_data['address']
        # athlete.year = self.cleaned_data['year']
        # athlete.phonenumber = self.cleaned_data['phonenumber']
        # athlete.weight = self.cleaned_data['weight']
        # athlete.email = self.cleaned_data['email']
        # athlete.gender = self.cleaned_data['gender']
        # athlete.usaw = self.cleaned_data['usaw']
        # athlete.school = self.cleaned_data['school']
        # athlete.contact = self.cleaned_data['contact']
        # athlete.contactnumber = self.cleaned_data['contactnumber']
        # athlete.gpa = self.cleaned_data['gpa']
        # athlete.transcript = self.cleaned_data['transcript']
        # athlete.goals = self.cleaned_data['goals']
        athlete.save()
        return user

class CoachSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)
    phonenumber = forms.CharField(max_length=12)
    group = forms.ModelChoiceField(
        queryset=Groups.objects.all(),
        required=True,
    )
    email = forms.CharField(max_length=250)
    code = forms.CharField(max_length=200)

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        coachcode = 'a423s98'
        if coachcode == self.cleaned_data['code']:
            user.is_coach = True
            if commit:
                user.save()
                athlete = Athlete(user=user, group=self.cleaned_data['group'], first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'], phonenumber=self.cleaned_data['phonenumber'], email=self.cleaned_data['email'])
                # athlete.first_name = self.cleaned_data['first_name']
                # athlete.last_name = self.cleaned_data['last_name']
                # athlete.phonenumber = self.cleaned_data['phonenumber']
                # athlete.email = self.cleaned_data['email']
                athlete.save()
            return user
        return user
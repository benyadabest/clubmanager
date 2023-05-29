from asyncio import events
from inspect import Attribute
import datetime
import logging
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from .models import User, Athlete, Groups, Event, Eventsignup, ClassTime, Attendance
from .forms import AthleteForm, GroupForm, EventForm, AthleteEventForm, ClassTimeForm, AttendanceForm, AttendanceForm2, AthleteSignUpForm, CoachSignUpForm, AthleteEventForm2
from .filters import AthleteFilter, paginateAthletes, EventsignupFilter, AttendanceFilter
from django.views.generic import CreateView
from uuid import UUID
import cv2
from pyzbar import pyzbar
from pyzbar.pyzbar import decode

def home(request):
    # if request.user.is_authenticated:
    #     if request.user.is_coach:
    #         return redirect('athletes')
    #     else:
    #         try:
    #             return redirect('profile', request.user.id)
    #         except:
    #             return redirect('logout')
    return render(request, 'athletes/home.html')

def athletes(request):
    group = Groups.objects.get(name='Coaches')
    athletes = Athlete.objects.exclude(group=group)
    groups = Groups.objects.all()
    events = Event.objects.all()
    
    attendance = []
    for a in athletes:
        attendance.append((a.attendance(), a.name(), a.get_present(), a.get_late(), a.get_absent(), a.id))
    
    def sort_key(report):
        return report[0]

    attendance.sort(key=sort_key, reverse=True)
    custom_range2, attendance = paginateAthletes(request, attendance, 8)

    myFilter = AthleteFilter(request.GET, queryset=athletes)
    athletes = myFilter.qs

    custom_range, athletes = paginateAthletes(request, athletes, 20)

    context = {'athletes': athletes, 'groups': groups, 'events': events, 'filter': myFilter, 'custom_range': custom_range, 'custom_range2': custom_range2, 'attendance': attendance}
    return render(request, 'athletes/athletes.html', context)


def attendance(request):
    attendance = Attendance.objects.all()

    myFilter = AttendanceFilter(request.GET, queryset=attendance)
    attendance = myFilter.qs

    custom_range, attendance = paginateAthletes(request, attendance, 20)

    context = {'attendance': attendance, 'filter': myFilter, 'custom_range': custom_range}
    return render(request, 'athletes/attendance.html', context)


def group(request, num):
    group = Groups.objects.get(id=num)
    athletes = Athlete.objects.filter(group=group)
    context = {'group': group, 'athletes': athletes,}
    return render(request, 'athletes/group.html', context)



def event(request, num):
    event = Event.objects.get(id=num)
    eventsignups = Eventsignup.objects.filter(event=event)

    myFilter = EventsignupFilter(request.GET, queryset=eventsignups)
    eventsignups = myFilter.qs

    context = {'event': event, 'eventsignups':eventsignups, 'filter': myFilter}
    return render(request, 'athletes/event.html', context)


def athlete(request, num):
    athlete = Athlete.objects.get(id=num)
    events = Eventsignup.objects.filter(athlete=athlete)
    context = {'athlete': athlete, 'events':events}
    return render(request, 'athletes/athlete.html', context)

def BarcodeReader(image):
     
    img = cv2.imread(image)
    detectedBarcodes = decode(img)
      
    if not detectedBarcodes:
        print("Barcode Not Detected or your barcode is blank/corrupted!")
        return None
    else:
        for barcode in detectedBarcodes:            
            (x, y, w, h) = barcode.rect
            cv2.rectangle(img, (x-10, y-10),
                          (x + w+10, y + h+10),
                          (255, 0, 0), 2)
             
            if barcode.data!="":
                return(barcode.data)

def selfattendance(request, num, num2):
    classtime = ClassTime.objects.get(id=num)
    group = Groups.objects.get(id=num2)
    data = {'classtime': classtime}
    form = AttendanceForm(initial=data)

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.cleaned_data['classtime'] = classtime

            try:
                a = Athlete.objects.get(group=group, id=form.cleaned_data['athlete_id'])
                print('yay')
                attObject = Attendance.objects.get(classtime=classtime, athlete_id=form.cleaned_data['athlete_id'])
                attObject.mark_attendance = 'Present'
                attObject.save()
                return redirect('self-attendance', num, num2)
            except:
                print('failed')
                return redirect('self-attendance', num, num2)

    context = {'form': form}
    return render(request, 'athletes/attendance_form.html', context)


def events(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'athletes/events.html', context)


def groupattendance(request, num, num2):
    classtime = ClassTime.objects.get(id=num)
    group = Groups.objects.get(id=num2)
    attendences = Attendance.objects.filter(group=group, classtime=classtime)
    context = {'classtime': classtime, 'group': group, 'attendances': attendences}


    return render(request, 'athletes/groupattendance.html', context)


def updateattendance(request, num, num2, num3):
    att = Attendance.objects.get(id=num3)
    data = {'mark_attendance': att.mark_attendance} #'athlete_id': att.athlete_id, 'group': att.group, 'classtime': att.classtime,
    form = AttendanceForm2(initial=data)

    if request.method == 'POST':
        form = AttendanceForm2(request.POST, instance=att)
        if form.is_valid():
            # form.cleaned_data['athlete_id'] = data.athlete_id
            # form.cleaned_data['group'] = data.group
            # form.cleaned_data['classtime'] = data.classtime
            attObject = Attendance.objects.get(classtime=att.classtime, athlete_id=att.athlete_id)
            attObject.mark_attendance = form.cleaned_data['mark_attendance']
            attObject.save()

            return redirect('group-attendance', num, num2)
            
    context = {'form': form}
    return render(request, 'athletes/attendance_form.html', context)


def deleteattendance(request, num, num2, num3):
    attendance = ClassTime.objects.get(id=num3)

    if request.method == 'POST':
        attendance.delete()
        return redirect('group-attendance', num, num2)

    context = {'object': attendance}
    return render(request, 'athletes/delete.html', context)


def createClassTime(request, num):
    group = Groups.objects.get(id=num)
    form = ClassTimeForm()

    if request.method == 'POST':
        form = ClassTimeForm(request.POST)
        if form.is_valid():
            ct = form.save()

            group.addClass(ct)
            athletes = Athlete.objects.filter(group=group)

            for i in athletes:
               at = Attendance(athlete_id=i.id, group=group, classtime=ct, mark_attendance='Absent')
               at.save()
            return redirect('group', num)
    
    context = {'form': form}
    return render(request, 'athletes/classtime_form.html', context)
    

def updateClassTime(request, num, num2):
    classtime = ClassTime.objects.get(id=num)
    form = AthleteForm(instance=athlete)

    if request.method == 'POST':
        form = ClassTimeForm(request.POST, instance=classtime)
        if form.is_valid():
            form.save()
            return redirect('group', num2)
            
    context = {'form': form}
    return render(request, 'athletes/classtime_form.html', context)


def deleteClassTime(request, num, num2):
    classtime = ClassTime.objects.get(id=num)

    if request.method == 'POST':
        classtime.delete()
        return redirect('group', num2)

    context = {'object': classtime}
    return render(request, 'athletes/delete.html', context)


def createAthlete(request):
    form = AthleteForm()

    if request.method == 'POST':
        form = AthleteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('athletes')

    context = {'form': form}
    return render(request, 'athletes/athlete_form.html', context)


def updateAthlete(request, num):
    athlete = Athlete.objects.get(id=num)
    form = AthleteForm(instance=athlete)

    if request.method == 'POST':
        form = AthleteForm(request.POST, request.FILES, instance=athlete)
        if form.is_valid():
            form.save()
            return redirect('athletes')
            
    context = {'form': form}
    return render(request, 'athletes/athlete_form.html', context)


def deleteAthlete(request, num):
    athlete = Athlete.objects.get(id=num)

    if request.method == 'POST':
        athlete.delete()
        return redirect('athletes')

    context = {'object': athlete.name}
    return render(request, 'athletes/delete.html', context)


def createGroup(request):
    form = GroupForm()

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('athletes')

    context = {'form': form}
    return render(request, 'athletes/group_form.html', context)


def updateGroup(request, num):
    group = Groups.objects.get(id=num)
    form = GroupForm(instance=group)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('athletes')
            
    context = {'form': form}
    return render(request, 'athletes/group_form.html', context)


def deleteGroup(request, num):
    group = Groups.objects.get(id=num)

    if request.method == 'POST':
        group.delete()
        return redirect('athletes')

    context = {'object': group.name}
    return render(request, 'athletes/delete.html', context)


def createEvent(request):
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('athletes')

    context = {'form': form}
    return render(request, 'athletes/event_form.html', context)


def updateEvent(request, num):
    event = Event.objects.get(id=num)
    form = EventForm(instance=event)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('athletes')
            
    context = {'form': form}
    return render(request, 'athletes/event_form.html', context)


def deleteEvent(request, num):
    event = Event.objects.get(id=num)

    if request.method == 'POST':
        event.delete()
        return redirect('athletes')

    context = {'object': event.name}
    return render(request, 'athletes/delete.html', context)


def athleteEventSignup(request):
    form = AthleteEventForm()

    if request.method == 'POST':
        form = AthleteEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('athletes')

    context = {'form': form}
    return render(request, 'athletes/athleteEvent_form.html', context)


def updateathleteEventSignup(request, num, num2):
    event = Event.objects.get(id=num)
    athlete = Athlete.objects.get(id=num2)
    ae = Eventsignup.objects.get(event=event, athlete=athlete)
    form = AthleteEventForm(instance=ae)

    if request.method == 'POST':
        form = AthleteEventForm(request.POST, instance=ae)
        if form.is_valid():
            form.save()
            if request.user.is_athlete:
                return redirect('profile', num2)
            else:
                return redirect('athletes')
            
    context = {'form': form}
    return render(request, 'athletes/athleteEvent_form.html', context)


def deleteathleteEventSignup(request, num, num2):
    event = Event.objects.get(id=num)
    athlete = Athlete.objects.get(id=num2)
    ae = Eventsignup.objects.get(event=event, athlete=athlete)

    if request.method == 'POST':
        ae.delete()
        if request.user.is_athlete:
            return redirect('profile', num2)
        else:
            return redirect('athletes')

    context = {'object': ae}
    return render(request, 'athletes/delete.html', context)

def athleteEventSignup2(request, num):
    user = User.objects.get(id=num)
    athlete = Athlete.objects.get(user=user)
    form = AthleteEventForm2()

    if request.method == 'POST':
        form = AthleteEventForm2(request.POST)
        if form.is_valid():
            ae = form.save(commit=False)
            ae = Eventsignup(athlete=athlete, event=form.cleaned_data['event'], transportation=form.cleaned_data['transportation'])
            try:
                ae.save()
                return redirect('profile', num)
            except:
                return redirect('profile', num)

    context = {'form': form}
    return render(request, 'athletes/athleteEvent_form.html', context)

def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

def profile(request, num):
    # user = User.objects.get(id=num)
    if is_valid_uuid(num):
        a = Athlete.objects.get(id=num)
    else:
        user = User.objects.get(id=num)
        a = Athlete.objects.get(user=user)
    events = Eventsignup.objects.filter(athlete=a)
    context = {'athlete': a, 'events':events}
    return render(request, 'athletes/profile.html', context)

def updateprofile(request, num):
    # user = User.objects.get(id=num)
    athlete = Athlete.objects.get(id=num)
    form = AthleteForm(instance=athlete)

    if request.method == 'POST':
        form = AthleteForm(request.POST, request.FILES, instance=athlete)
        if form.is_valid():
            form.save()
            return redirect('profile', num)
            
    context = {'form': form}
    return render(request, 'athletes/athlete_form.html', context)

def signup(request):
    return render(request, 'athletes/signup.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            messages.info(request, f'You are now logged in as {username}!')
            return redirect('profile', request.user.id)
        else:
            messages.error(request, 'Invalid username or password')

    form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'athletes/login.html', context)

def logout(request):
    django_logout(request)
    messages.info(request, 'Successfully logged out!')
    return redirect('login')



class AthleteSignUpView(CreateView):
    model = User
    form_class = AthleteSignUpForm
    template_name = 'athletes/signup_form.html'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'athlete'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        a = Athlete.objects.get(user=user)
        return redirect('profile', a.id)

class CoachSignUpView(CreateView):
    model = User
    form_class = CoachSignUpForm
    template_name = 'athletes/signup_form.html'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'coach'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        #a = Athlete.objects.get(user=user)
        return redirect('athletes')


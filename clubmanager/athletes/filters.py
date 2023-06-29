from dataclasses import field
import django_filters
from django_filters import CharFilter
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from operator import attrgetter


class AthleteFilter(django_filters.FilterSet):
    first_name = CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = CharFilter(field_name='last_name', lookup_expr='icontains')


    class Meta:
        model = Athlete
        fields = ['group', 'first_name', 'last_name', 'year', 'gender', 'school']

class AttendanceFilter(django_filters.FilterSet):

    class Meta:
        model = Attendance
        fields = ['athlete_id', 'group', 'classtime', 'mark_attendance']

class EventsignupFilter(django_filters.FilterSet):

    class Meta:
        model = Eventsignup
        fields = ['transportation', 'athlete']

def paginateAthletes(request, athletes, results):
    page = request.GET.get('page')
    paginator = Paginator(athletes, results)

    try:
        athletes = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        athletes = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        athletes = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, athletes
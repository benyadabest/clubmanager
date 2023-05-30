from django.db import models

# Create your models here.
from datetime import datetime
from distutils.command.upload import upload
from enum import unique
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import barcode                      # additional imports
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import datetime

# Create your models here.
class User(AbstractUser):
    #     # class Role(models.TextChoices):
#     #     COACH = "COACH", 'Coach'
#     #     ATHLETE = "ATHLETE", 'Athlete'

#     # base_role = Role.COACH
#     # role = models.CharField(max_length=50, choices=Role.choices)

#     # def save(self, *args, **kwargs):
#     #     if not self.pk:
#     #         self.role = self.base_role
#     #         return super().save(*args, **kwargs)
    is_athlete = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)

class Club(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=250, unique=True)
    delete_flag = models.IntegerField(default = 0)

    class Meta:
        verbose_name_plural = "Clubs"

    def __str__(self):
        return str(self.name)


class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=250, unique=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    date_start = models.DateField()
    date_end = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    delete_flag = models.IntegerField(default = 0)
    barcode = models.ImageField(upload_to='barcodes/', blank=True)

    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self._state.adding:
            COD128 = barcode.get_barcode_class('code128')
            rv = BytesIO()
            code = COD128(f'{self.id}', writer=ImageWriter()).write(rv)
            self.barcode.save(f'{self.name}.png', File(rv), save=False)
            return super().save(*args, **kwargs)
        else:
            return super()

class ClassTime(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Classes"

    def __str__(self):
        return str(self.date)


class Groups(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    classes = models.ManyToManyField(ClassTime, blank=True)
    name = models.CharField(max_length=250, unique=True)
    delete_flag = models.IntegerField(default = 0)
    barcode = models.ImageField(upload_to='barcodes/', blank=True)

    class Meta:
        verbose_name_plural = "Groups"

    def __str__(self):
        return str(self.name)

    def addClass(self, ct):
        self.classes.add(ct)

    def save(self, *args, **kwargs):
        if self._state.adding:
            COD128 = barcode.get_barcode_class('code128')
            rv = BytesIO()
            code = COD128(f'{self.id}', writer=ImageWriter()).write(rv)
            self.barcode.save(f'{self.name}.png', File(rv), save=False)
            return super().save(*args, **kwargs)
        else:
            return super()


class Athlete(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, default='')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, blank=True)
    events = models.ManyToManyField(Event, blank=True)
    delete_flag = models.IntegerField(default = 0)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    address = models.TextField(blank=True, null= True)
    dob = models.DateField(blank=True, null=True)
    year = models.IntegerField(default=0)
    phonenumber = models.CharField(max_length=12)
    weight = models.IntegerField(default=0)
    email = models.CharField(max_length=250)
    gender = models.CharField(max_length=20, choices=(('Male','Male'), ('Female','Female')), default = "Male")
    usaw = models.ImageField(upload_to="", null=True, blank=True, default="")
    school = models.CharField(max_length=250)
    contact = models.CharField(max_length=250)
    contactnumber = models.CharField(max_length=12)
    gpa = models.DecimalField(default=2.0, decimal_places=2, max_digits=3)
    transcript = models.ImageField(upload_to="", null=True, blank=True, default="")
    goals = models.CharField(max_length=400, blank=True, null=True)
    barcode = models.ImageField(upload_to='barcodes/', blank=True, default="")

    def get_present(self):
        try:
            present = Attendance.objects.filter(athlete_id=self.id, mark_attendance='Present').count()
            return present
        except:
            return 0
    
    def get_late(self):
        try:
            late = Attendance.objects.filter(athlete_id=self.id, mark_attendance='Late').count()
            return late
        except:
            return 0

    def get_absent(self):
        try:
            absent = Attendance.objects.filter(athlete_id=self.id, mark_attendance='Absent').count()
            return absent
        except:
            return 0

    def attendance(self):
        try:
            total = Attendance.objects.filter(athlete_id=self.id).count()
            present = Attendance.objects.filter(athlete_id=self.id, mark_attendance='Present').count()
            report = present/total * 100
            if total != 0:
                return str(report)
            else:
                return 'Did not attend yet'
        except:
            return '0'

    def __str__(self):
        name = str(self.first_name) + " " + str(self.last_name)
        return name
    
    def name(self):
        name = str(self.first_name) + " " + str(self.last_name)
        return name

    def name2(self):
        name = str(self.first_name) + "_" + str(self.last_name)
        return name

    def save(self, *args, **kwargs):
        if self._state.adding:
            COD128 = barcode.get_barcode_class('code128')
            rv = BytesIO()
            code = COD128(f'{self.user.id}', writer=ImageWriter()).write(rv)
            self.barcode.save(f'{self.first_name + " " + self.last_name}.png', File(rv), save=False)
            return super().save(*args, **kwargs)
        else:
            return super()

class Eventsignup(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    transportOptions = [('Team', 'Travel with the Team'), ('Parents', 'Travel with Parents')]
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    transportation = models.CharField(max_length=250, choices = transportOptions)

    class Meta:
        unique_together = ['athlete', 'event']

    def __str__(self):
        name = str(self.event) + "_" + str(self.athlete)
        return name

    def athletename(self):
        return self.athlete.name

class Attendance(models.Model):
    attendance = [('Present', 'Present'), ('Late', 'Late'), ('Absent', 'Absent')]
    athlete_id = models.CharField(max_length=200, default='0')
    group = models.ForeignKey(Groups, on_delete= models.CASCADE, null=True, blank=True)
    classtime = models.ForeignKey(ClassTime, on_delete= models.CASCADE)
    date = models.DateField(auto_now=datetime.date)
    time = models.TimeField(auto_now=datetime.time)
    mark_attendance = models.CharField(max_length=50, choices=attendance, default='Absent')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    class Meta:
        verbose_name_plural = "Attendance"
        unique_together = ['athlete_id', 'classtime', 'date']

    def __str__(self):
        a = Athlete.objects.get(id=self.athlete_id)
        return str(a.first_name) + " " + str(a.last_name) + "_" + str(self.classtime) + "__" + str(self.mark_attendance) + "__"+ str(self.time)
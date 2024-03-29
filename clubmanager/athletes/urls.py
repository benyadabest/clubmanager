from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.athletes, name='athletes'),
    path('dashboard/athlete/<str:num>/', views.athlete, name="athlete"),
    path('dashboard/group/<str:num>/', views.group, name="group"),
    path('dashboard/event/<str:num>/', views.event, name="event"),
    path('dashboard/add-athlete/', views.addAthlete, name="add-athlete"),
    path('dashboard/update-athlete/<str:num>/', views.updateAthlete, name="update-athlete"),
    path('dashboard/delete-athlete/<str:num>', views.deleteAthlete, name="delete-athlete"),
    path('dashboard/create-group/', views.createGroup, name="create-group"),
    path('dashboard/update-group/<str:num>/', views.updateGroup, name="update-group"),
    path('dashboard/delete-group/<str:num>/', views.deleteGroup, name="delete-group"),
    path('dashboard/create-event/', views.createEvent, name="create-event"),
    path('dashboard/update-event/<str:num>/', views.updateEvent, name="update-event"),
    path('dashboard/delete-event/<str:num>/', views.deleteEvent, name="delete-event"),
    path('dashboard/athlete-to-event/', views.athleteEventSignup, name="athlete-event-signup"),
    path('dashboard/update-athlete-to-event/<str:num>/<str:num2>/', views.updateathleteEventSignup, name="update-athlete-to-event"),
    path('dashboard/delete-athlete-to-event/<str:num>/<str:num2>/', views.deleteathleteEventSignup, name="delete-athlete-to-event"),
    path('dashboard/create-classtime/<str:num>/', views.createClassTime, name="create-classtime"),
    path('dashboard/update-classtime/<str:num>/<str:num2>/', views.updateClassTime, name="update-classtime"),
    path('dashboard/delete-classtime/<str:num>/<str:num2>/', views.deleteClassTime, name="delete-classtime"),
    path('dashboard/selfattendance/<str:num>/<str:num2>/', views.selfattendance, name='self-attendance'),
    path('dashboard/groupattendance/<str:num>/<str:num2>/', views.groupattendance, name='group-attendance'),
    path('dashboard/update-attendance/<str:num>/<str:num2>/<str:num3>/', views.updateattendance, name="update-attendance"),
    path('dashboard/delete-attendance/<str:num>/<str:num2>/<str:num3>/', views.deleteattendance, name="delete-attendance"),
    path('dashboard/attendance/', views.attendance, name='attendance'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name= 'logout'),
    path('profile/<str:num>', views.profile, name='profile'),
    path('profile/events/', views.events, name='events'),
    path('profile/events/signup/<str:num>/', views.athleteEventSignup2, name='athlete-event-signup2'),
    path('update-profile/<str:num>/', views.updateprofile, name='update-profile'),
    path('signup/athlete/', views.AthleteSignUpView.as_view(), name='athlete-signup'),
    path('signup/coach/', views.CoachSignUpView.as_view(), name='coach-signup'),
    path('cancel/', views.cancel, name="cancel"),
    path('success/', views.success, name="success"),
    path('message/', views.email, name="message"),

]
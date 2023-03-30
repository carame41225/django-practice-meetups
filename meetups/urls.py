from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='all-meetups'),
    path('mymeetups', views.mymeetups, name='MyMeetups'),
    path('register', views.sign_up, name='Register'),
    path('login', views.sign_in, name='Login'),
    path('logout', views.log_out, name='Logout'),
    path('<slug:meetup_slug>/success', views.confirm_registration,
         name='confirm-registration'),
    path('<slug:meetup_slug>',
         views.meetup_details, name='meetup-detail'),
    path('<slug:meetup_slug>/cancel', views.cancel, name="cancel"),
]

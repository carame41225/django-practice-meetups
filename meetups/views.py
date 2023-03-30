from django.shortcuts import render, redirect
from .models import Meetup, Participant
from .forms import RegistrationForm, RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):     # 首頁
    meetups = Meetup.objects.all()
    return render(request, 'meetups/index.html', {
        'meetups': meetups,
    })


@login_required
def mymeetups(request):     # 我的聚會
    user_name = request.user.username
    meetups = Meetup.objects.all()
    my_meetups = Meetup.objects.none()
    for i in range(1, len(meetups)+1):  # 資料比對
        my_meetup = Meetup.objects.filter(id=i)
        for name in Meetup.objects.get(id=i).participants.all().values():
            if user_name == name['name']:
                my_meetups = my_meetup.union(my_meetups)

    return render(request, 'meetups/mymeetups.html', {
        'meetups': my_meetups,
    })


def meetup_details(request, meetup_slug):       # 詳細資料
    try:
        selected_meetup = Meetup.objects.get(slug=meetup_slug)
        if request.method == 'GET':
            excist = False
            if request.user.is_authenticated:  # 判斷是否已報名
                user_name = request.user.username
                for i in selected_meetup.participants.all().values():
                    if i['name'] == user_name:
                        excist = True
            registration_form = RegistrationForm()
            return render(request, 'meetups/meetup-details.html', {
                'meetup_found': True,
                'meetup': selected_meetup,
                'excist': excist,
            })
        else:
            if request.method == 'POST':
                registration_form = RegistrationForm(request.POST)
                user_name = request.user.username
                participant, _ = Participant.objects.get_or_create(
                    name=user_name)
                selected_meetup.participants.add(participant)
                return redirect('confirm-registration', meetup_slug=meetup_slug)
            else:
                return render(request, 'meetups/meetup-details.html', {
                    'meetup_found': True,
                    'meetup': selected_meetup,
                    'form': registration_form
                })
    except Exception as exc:
        print(exc)
        return render(request, 'meetups/meetup-details.html', {
            'meetup_found': False
        })


@login_required
def confirm_registration(request, meetup_slug):     # 註冊成功頁面
    meetup = Meetup.objects.get(slug=meetup_slug)
    return render(request, 'meetups/registration-success.html', {
        'organizer_email': meetup.organizer_email
    })


def sign_up(request):       # 註冊
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/meetups/login')
    context = {
        'form': form
    }
    return render(request, 'meetups/register.html', context)


def sign_in(request):       # 登入
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successed!')
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'meetups/login.html', context)


def log_out(request):       # 登出
    logout(request)
    messages.success(request, 'Logout successed!')
    return redirect('/meetups/')

@login_required
def cancel(request, meetup_slug):
    if request.method == "POST":
        selected_meetup = Meetup.objects.get(slug=meetup_slug)
        user_name = request.user.username
        participant, _ = Participant.objects.get_or_create(
                        name=user_name)
        selected_meetup.participants.remove(participant)
    return render (request, 'meetups/cancel.html')
    
    

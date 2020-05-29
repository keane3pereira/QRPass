from .forms import PassCreationForm, RegistrationForm, AddUserForm
from .models import Event, EventUser, Customer, Pass, Transaction
from .emails import send_register_mail, send_undo_register_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from user.models import CustomUser
from django.db.models import Sum
from django.conf import settings
from os import listdir
from PIL import Image
import pyqrcode
import hashlib
import random

L = list('abcdefghijklmnopqrstuvwxyz')
N = list('1234567890')
S = list('!@#$%^&*()')

def generate_code():
    while True:
        x = random.sample(L, 4) + random.sample(N, 3) + random.sample(S,2)
        random.shuffle(x)
        m = ''
        for i in x:
            m += i
        if not Customer.objects.filter(code = m).exists():
            return m

def get_qr_filepath(C):
    file = C.code + ".png"
    if file not in listdir(settings.QR_FOLDER):
        print(listdir(settings.QR_FOLDER))
        path = settings.QR_FOLDER + file
        try:
            qr = pyqrcode.create(C.code)
            qr.png(path, scale = 4)
        except Exception as e: print(e)
    return settings.QR_FOLDER + file

# Create your views here.

def home(request):
    if request.method =='POST':
        event_name = request.POST.get('event', False)
        if event_name != False:
            request.session[request.user.email] = event_name
            return redirect(event_details)
    
    EU = EventUser.objects.filter(user = request.user)
    return render(request, 'home.html', {'userevents': EU})

@login_required(login_url='/login/')
def event_details(request):
    pass_create_result = ''
    event_name = request.session[request.user.email]
    E = Event.objects.get(name = event_name)
    if request.method =='POST':
        ''' create a new pass type'''
        name = request.POST.get('name', False)
        if not Pass.objects.filter(event = E, name = name).exists():
            cost = request.POST.get('cost', False)
            Pass(
                event = E,
                name = name,
                cost = cost
            ).save()
            pass_create_result = 'Success'
        else: 
            pass_create_result = 'Pass already exists'

    T = Transaction.objects.filter(event = E).order_by('-datetime')[:10]
    P = Pass.objects.filter(event = E)
    return render(request, 'event.html',{
        'pass_create_result': pass_create_result,
        'event_name': E.name,
        'transactions': T,
        'passes': P
    })

def event_users(request):
    event_name = request.session[request.user.email]
    E = Event.objects.get(name = event_name)
    if request.method == 'POST':
        email = request.POST.get('users', False)
        if email:
            user = CustomUser.objects.get(email = email)
            if not EventUser.objects.filter(user = user).exists():
                EventUser(
                    event = E,
                    user = user
                ).save()

    EU = EventUser.objects.filter(event = E)
    return render(request, 'event_users.html', {
        'event_users': EU,
        'event_name': E.name,
        'form': AddUserForm()
    })

@login_required(login_url='/login/')
def create_event(request):
    if request.method == 'POST':
        event_name = request.POST.get('name', False)
        if not Event.objects.filter(name = event_name).exists():
            E = Event(
                name = event_name,
                created_by = request.user
            )
            E.save()
            EventUser(
                event = E,
                user = request.user
            ).save()

            return redirect(home)

    return render(request, 'create_event.html', {
        'form': PassCreationForm()
    })

@login_required(login_url='/login/')
def register(request):
    message = ''
    event_name = request.session[request.user.email]
    E = Event.objects.get(name = event_name)
    if request.method == 'POST':
        email = request.POST.get('email', False)
        count = request.POST.get('count', 0)
        pass_type = request.POST.get('pass_type', False)
        PASS = Pass.objects.get(id = pass_type)
        if Customer.objects.filter(event = PASS.event, email = email).exists():
            C = Customer.objects.get(event = PASS.event, email = email)
        else:                        
            name = request.POST.get('name', "")
            code = generate_code()
            C = Customer(
                event = PASS.event,
                email = email,
                name = name,
                code = code
            )
            C.save()

        Transaction(
            customer = C,
            event = E,
            PASS = PASS,
            count = count,
            created_by = request.user
        ).save()
        print(settings.QR_FOLDER + get_qr_filepath(C))

        file = get_qr_filepath(C)
        ''' send email to customer '''
        send_register_mail(C, file)
        message = 'Success'

    T = Transaction.objects.filter(event = E, created_by = request.user).order_by('-datetime')[:5]
    return render(request, 'register.html', {
        'form': RegistrationForm(event = E.id),
        'event_name': event_name,
        'message': message,
        'transactions': T
    })

@login_required(login_url='/login/')
def undo_register(request):
    event_name = request.session[request.user.email]
    E = Event.objects.get(name = event_name)
    if request.method == 'POST':
        t_id = request.POST.get('t_id', False)
        T = Transaction.objects.get(id = int(t_id), event = E)
        C = T.customer
        dt = T.datetime
        T.delete()

        ''' send email to customer '''
        send_undo_register_mail(C, dt)

    return redirect(event_details)

@login_required(login_url='/login/')
def delete_data(request):
    test_name = request.POST.get('event2', False)
    event_name = request.session[request.user.email]
    if test_name == event_name:
        E = Event.objects.get(name = event_name)
        T = Transaction.objects.filter(event = E)
        C = Customer.objects.filter(event = E)
        P = Pass.objects.filter(event = E)
        EU = EventUser.objects.filter(event = E)
        T.delete(); C.delete(); EU.delete(); E.delete()

    return redirect(home)

def customer(request):
    if request.method == 'POST':
        email = request.POST.get('email', False)
        if email:
            if Customer.objects.filter(email = email).exists():
                C = Customer.objects.get(email = email)
                T = Transaction.objects.filter(customer = C)
                PASS = Pass.objects.filter(event = C.event)
                BALANCE = {}
                for P in PASS:
                    t = T.filter(event_pass = P)
                    total = t.aggregate(Sum('count'))
                    BALANCE[P.name] = total['count__sum']
                file = str(C.event.id) + str(C.email) + ".png"
                if file not in listdir(settings.QR_FOLDER):
                    pass
                return render(request, 'customer.html',
                    {'customer': C, 'passes': BALANCE})
    return redirect(create_event)

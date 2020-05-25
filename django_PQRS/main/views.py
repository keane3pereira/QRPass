from .forms import PassCreationForm, RegistrationForm, AddUserForm
from .models import Event, EventUser, Customer, Pass, Transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from pyqrcode import create as qrcreate
from user.models import CustomUser
from django.db.models import Sum
from django.conf import settings
from os import listdir
from PIL import Image
import hashlib

QR_FOLDER = settings.BASE_DIR + "\\media\\qrs\\"

def create_qr_image(path, code):
    try:
        qr = qrcreate(code)
        qr.png(path, scale = 4)
        #print("saved")
        return True
    except Exception as e:
        #print(e)
        return False

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
            P = Pass(
                event = E,
                name = name,
                cost = cost
            )
            P.save()
            pass_create_result = 'Success'
        else:
            pass_create_result = 'Pass already exists'
    T = Transaction.objects.filter(event = E)
    P = Pass.objects.filter(event = E)
    return render(request, 'event.html', {'event_name': E.name, 'passes': P, 'pass_create_result': pass_create_result, 'transactions': T})

def event_users(request):
    event_name = request.session[request.user.email]
    E = Event.objects.get(name = event_name)
    if request.method == 'POST':
        email = request.POST.get('users', False)
        print(email)
        if email:
            user = CustomUser.objects.get(email = email)
            if not EventUser.objects.filter(user = user).exists():
                EU = EventUser(
                    event = E,
                    user = user
                )
                EU.save()
    EU = EventUser.objects.filter(event = E)
    form = AddUserForm()
    return render(request, 'event_users.html', {'event_users': EU, 'form': form})

@login_required(login_url='/login/')
def create_event(request):
    if request.method == 'POST':
        event_name = request.POST.get('name', False)
        print(event_name)
        if not Event.objects.filter(name = event_name).exists():
            print('new event')
            E = Event(
                name = event_name,
                created_by = request.user
                )
            E.save()
            EU = EventUser(
                event = E,
                user = request.user
            )
            EU.save()
            return redirect(home)
        else:
            print('event exists')
    return render(request, 'create_event.html', {'form': PassCreationForm()})

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
            code = hashlib.sha1((str(PASS.event.id)+email).encode("UTF-8")).hexdigest()
            C = Customer(
                event = PASS.event,
                email = email,
                name = name,
                code = code
            )
            C.save()
        T = Transaction(
                customer = C,
                event = E,
                PASS = PASS,
                count = count
            )
        T.save()
        message = 'Success'
    T = Transaction.objects.all() 
    ''' add a registeredby field to transactions'''
    return render(request, 'register.html', {'form': RegistrationForm(event = E.id),'event_name': event_name, 'transactions': T,'message': message})

@login_required(login_url='/login/')
def delete_data(request):
    e = request.POST.get('event', False)
    if e:
        T = Transaction.objects.filter(event = e)
        C = Customer.objects.filter(event = e)
        T.delete(); C.delete()
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
                #print(BALANCE)
                file = str(C.event.id) + str(C.email) + ".png"
                if file not in listdir(QR_FOLDER):
                    create_qr_image(QR_FOLDER + file, C.code)
                return render(request, 'customer.html',
                    {'customer': C, 'transactions': T, 'passes': BALANCE})
    return redirect(create_event)

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Transaction, Customer, Pass
from email.mime.image import MIMEImage
from django.db.models import Sum
from django.conf import settings
import main.views as main_views
from os import listdir
from PIL import Image

from_email = 'pythonformkeanesan@gmail.com'


def create_register_message(C, PASS, T):
    if C.name == '': name = 'there'
    else: name = C.name
    message = f'''
Hi {name},<br>
Your ticket(s) for '{C.event.name}' have been registered successfully!
<br><br>
Current Balance:<br>
<table border="1">
<tr><td>Pass Type</td><td> Count </td></tr>
'''
    for P in PASS:
        t = T.filter(PASS = P)
        total = t.aggregate(Sum('count'))
        message += f"<tr><td>{P.name}</td></td>{total['count__sum']}</td></tr>"
    message += '''
</table>
<br>
Your QR-Pass for the event is included along with this email.
Please do not share your code with others.
'''
    #print(message)
    return message

def send_register_mail(to, file):
    C = Customer.objects.get(email = to)
    T = Transaction.objects.filter(customer = C)
    PASS = Pass.objects.filter(event = C.event)
    with open(file, 'rb') as f:
        data = f.read()
    img = MIMEImage(data, name=file)
    msg = EmailMultiAlternatives('Your pass has been registered!', 'Your pass has been registered!', from_email, [to])
    msg.attach_alternative(create_register_message(C, PASS, T), 'text/html')
    msg.attach(img)
    msg.send()

def create_undo_register_message(C, PASS, T, datetime):
    if C.name == '': name = 'there'
    else: name = C.name
    message = f'''
Hi {name},<br>
Your registration for {C.event.name} at {datetime} has been cancelled.
<br><br>
Current Balance:<br>
<table border="1">
<tr><td>Pass Type</td><td> Count </td></tr>
'''
    for P in PASS:
        t = T.filter(PASS = P)
        total = t.aggregate(Sum('count'))
        message += f"<tr><td>{P.name}</td></td>{total['count__sum']}</td></tr>"
    message += '''
</table>
<br>
Your QR-Pass for the event is included along with this email.
Please do not share your code with others.
'''
    #print(message)
    return message

def send_undo_register_mail(C, datetime):
    to = C.email
    T = Transaction.objects.filter(customer = C)
    PASS = Pass.objects.filter(event = C.event)

    message = create_undo_register_message(C, PASS, T, datetime)

    msg = EmailMultiAlternatives('Registration Cancelled!', message, from_email, [to])
    msg.attach_alternative(create_register_message(C, PASS, T), 'text/html')
    msg.send()
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

def send_register_mail(C, file):
    T = Transaction.objects.filter(customer = C)
    PASS = Pass.objects.filter(event = C.event)
    with open(file, 'rb') as f:
        data = f.read()
    img = MIMEImage(data, name=file)
    msg = EmailMultiAlternatives('Your pass has been registered!', 'Your pass has been registered!', from_email, [C.email])

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
    msg.attach_alternative(message, 'text/html')
    msg.attach(img)
    msg.send()


def send_undo_register_mail(C, datetime):
    to = C.email
    T = Transaction.objects.filter(customer = C)
    PASS = Pass.objects.filter(event = C.event)

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

    msg = EmailMultiAlternatives('Registration Cancelled!', message, from_email, [to])
    msg.attach_alternative(message, 'text/html')
    msg.send()
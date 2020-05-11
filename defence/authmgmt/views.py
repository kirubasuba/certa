from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import os
import pyAesCrypt
from os import remove
import uuid
from django.conf import settings
from .models import registration,firmregistrationstatusmodel
from django.core.mail import send_mail
import subprocess
from datetime import datetime
from django.core.mail import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
# from .forms import LoginForm
def login(request):
    print('req => %s',request)
    _message = 'Please Login..'
    _next = 'home'
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        user = authenticate(username=_username, password=_password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                
                print(_next)
                if request.GET.get('next') == '/':
                    _next = 'home'
                print(_next)
                return HttpResponseRedirect(reverse(_next))
            else:
                _message = 'Your account is not activated'
        else:
            _message = 'Invalid login, please try again.'
    context = {'message': _message, 'next': request.GET.get('next')}
    return render(request, 'authmgmt/login.html', context)

def logout(request):
    user = request.user
    if not user.is_active:
        return HttpResponseRedirect(reverse('home'))
    else:
        auth_logout(request)
    return render(request, 'authmgmt/logout.html')

def forgotPassword(request):
    return render(request, 'authmgmt/forgot-password.html')

def register(request):
    return render(request, 'authmgmt/register.html')

def sign_up(request):
    if request.method == 'POST':
        myfile=''
        firmname=request.POST['firmname']
        firmhead=request.POST['firmhead']
        addr=request.POST['address']

        # addr=request.POST['addr']
        username=request.POST['username']
        email=request.POST['email']
        # password=request.POST['password']
            
        myfile = request.FILES['doc']          
        print(myfile.name,'myfile')
        fn=myfile.name
        ext=fn[-4:]
        print(ext,'ext')
        extension=ext

        # curr_path = str(request.user.id) + '/application'
        curr_path = "/"+email+ "/registration/"
        curr_path=curr_path.replace('/','\\')
        new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
        print(new_path,'newpath')

        fs = FileSystemStorage(location=new_path , base_url = new_path )

            # encrypt the file
        # fs = FileSystemStorage()
        unique_filename = str(uuid.uuid4())
        filename = fs.save(unique_filename, myfile)
        uploaded_file_url = fs.path(filename)
        print(uploaded_file_url,'url')

       
        bufferSize = 64 * 1024
        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
        with open(uploaded_file_url, "rb") as fIn:
            with open(uploaded_file_url+".aes", "wb") as fOut:
                pyAesCrypt.encryptStream(fIn, fOut, passw, bufferSize)
        date_joined = datetime.now()
        formatted_datetime = date_joined.strftime("%Y-%m-%d")
        status='inactive'
        reg = registration(firmname=firmname, firmhead=firmhead,addr=addr,username=username,email=email,doc=uploaded_file_url+".aes",status=status,remarks='',extension=extension,request_date=formatted_datetime)
        reg.save()


        # sender = 'kiruba@gennext.com'
        # receivers = ['kiruba@gennext.com']

        # message = """From:<kiruba@gennext.com>
        # Subject: New Firm Registration

        # Hi admin, Kindly register the new user -"""+username

        # try:
        #     smtpObj = smtplib.SMTP('localhost', 25)
        #     smtpObj.sendmail(sender, receivers, message)         
        #     print("Successfully sent email")
        # except smtplib.SMTPException:
        #     print("Error: unable to send email")

# ======================
        # FROMADDR = "kiruba@gennext.com"
        # # GROUP_ADDR = ['suba@gennext.com']
        # PASSWORD = 'sublee@123'


        # TOADDR   = ['suba@gennext.com']
        # # CCADDR   = ['group@server.com']

        # # Create message container - the correct MIME type is multipart/alternative.
        # msg            = MIMEMultipart('alternative')
        # msg['Subject'] = 'Test'
        # msg['From']    = FROMADDR
        # msg['To']      = ', '.join(TOADDR)
        # # msg['Cc']      = ', '.join(CCADDR)

        # # Create the body of the message (an HTML version).
        # text = """Hi  this is the body
        # """

        # # Record the MIME types of both parts - text/plain and text/html.
        # body = MIMEText(text, 'plain')

        # # Attach parts into message container.
        # msg.attach(body)

        # # Send the message via local SMTP server.
        # s = smtplib.SMTP('gennext.com', 25)
        # s.set_debuglevel(1)
        # s.ehlo()
        # s.starttls()
        # s.login(FROMADDR, PASSWORD)
        # s.sendmail(FROMADDR, TOADDR, msg.as_string())
        # s.quit()
# ===============

        # SERVER = "gennext"
        # LOGIN = "kiruba@gennext.com"
        # PASSWORD = "sublee@123"

        # FROM = "kiruba@gennext.com"
        # TO = ["suba@gennext.com",] # must be a list
        # SUBJECT = "Hello!"

        # TEXT = "This message was sent with Python's smtplib."

        # # Prepare actual message
        # message = """\
        # From: %s
        # To: %s
        # Subject: %s

        # %s
        # """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        # server = smtplib.SMTP(SERVER,port=25)
        # server.set_debuglevel(1)
        # server.login(LOGIN, PASSWORD)
        # server.sendmail(FROM, TO, message)
        # server.quit()
# =============================
        # email = EmailMessage(
        #     subject='New Firm Registration',
        #     message='Hi admin, Kindly register the new user '+username,
        #     from_email='kiruba@gennext.com',
        #     recipient_list=['kiruba@gennext.com'],
        #     reply_to='kiruba@gennext.com'
        # )
        # sent = email.send(fail_silently=False)
        # if sent:
        # =================================
        # send_mail('New Firm Registration', 'Hi admin, Kindly register the new user '+username, 'kiruba@gennext.com', ['kiruba@gennext.com',])
        remove(uploaded_file_url)
                        
        messages.success(request, 'Firm Registration UnderProcess!!!')
        return redirect('enroll')

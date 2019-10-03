from django.shortcuts import render,redirect
from .models import app,registration,User
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from sample.services import services
import requests
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

# Create your views here.

from .forms import UserCreationForm
class viewclass:
    def userDetails(request):

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():

                u = form.save()
                send_mail('Registered Successfully!!!', 'Hi '+form.cleaned_data['username']+',You account is Successfully Registered in CEMILAC.Now you can login with the following credentials.Username: '+form.cleaned_data['email']+',Password :'+form.cleaned_data['password1'], 'cemilac.drdo@gmail.com', [form.cleaned_data['email'],])
                messages.success(request, 'User Created successfully!')
                navlist=[]
                form = UserCreationForm
                if apps_list != []:
                    for nav in apps_list:
                        print('nav1',nav['app_name'])
                        navlist.append(nav['app_name'])
                return render(request, 'newuser.html', {'form': form,'navlist':navlist})
                # users = User.objects.all()

                # return render(request, 'index.html', {'users': users})
        else:
            form = UserCreationForm

        return render(request, 'newuser.html', {
            'form': form,
        })

    def index(request):
    # if request.method == 'POST':
    #     check_in=request.POST['checkin-date']
    #     check_out=request.POST['checkout-date']
    #     room=request.POST['room']
    #     adults=request.POST['adults']
    #     children=request.POST['children']

    #     sample=sampleinfo(checkin_date=check_in,checkout_date=check_out,no_of_rooms=room,no_of_adults=adults,no_of_children=children)
    #     sample.save()
    #     print('sample created')
    #     return redirect('index')
    # else:
    #     samples=sampleinfo.objects.filter(no_of_children="3").delete()
        return render(request,'index.html')
    
    def login(request):
        return render(request,'login.html')
    
    def login_new(request):
        return render(request,'login_2.html')

    def login_1(request):
        return render(request,'login_1.html')

    def loggedin(request):
        if request.method == 'POST':
            username=request.POST['username']
            password=request.POST['password']
            role=request.POST['role']
            user = authenticate(request, username=username, password=password)
            if user:
                
                token = services.get_auth_token(username,password)
            # token, _ = Token.objects.get_or_create(user=user)
                request.session['authtoken'] = token
                request.session['username'] = user.username
                if role=="1" and user.is_appadmin:
                    print(token,role,'authtoken')
                    global apps_list
                    apps_list = services.get_auth_app(role,request)
                    navlist=[]
                    form = UserCreationForm
                    if apps_list != []:
                        for nav in apps_list:
                            print('nav',nav['app_name'])
                            navlist.append(nav['app_name'])
                    return render(request, 'newuser.html', {'form': form,'navlist':navlist})
                elif role=="2" and user.is_applicant:
                    apps_list = services.get_auth_app(role,request)
                    navlist=[]
                    form = UserCreationForm
                    if apps_list != []:
                        for nav in apps_list:
                            print('nav',nav['app_name'])
                            navlist.append(nav['app_name'])
                    return render(request, 'applicant.html', {'form': form,'navlist':navlist})
                elif role=="3" and user.is_dealing_officer:
                    apps_list = services.get_auth_app(role,request)
                    navlist=[]
                    form = UserCreationForm
                    if apps_list != []:
                        for nav in apps_list:
                            print('nav',nav['app_name'])
                            navlist.append(nav['app_name'])
                    return render(request, 'processTR.html', {'form': form,'navlist':navlist})
                else:
                    apps_list=[]
                    messages.error(request, 'Invalid Role!!!')
                    return redirect('login_1')
                

            # if user.is_admin:
            #     request.session['role'] = 'Admin'
            #     navlist.append("View Type Record")
            #     navlist.append("Pro A")
            #     navlist.append("Forward Type Record")
            #     print('navlist',navlist)
            #     return render(request,'app_home.html',{'navlist':navlist,'navbar':'true'})
            # elif user.is_applicant:
            #     request.session['role'] = 'Applicant'
            #     navlist=[]
            #     navlist.append("Apply for Type Approval")
                
            #     print('navlist',navlist)
            # elif user.is_applicant:
            #     return render(request,'dealing_officer/do_home.html',{'name':'dealing_officer'})
            # elif user.is_applicant:
            #     return render(request,'RD/rd_home.html',{'name':'RD'})
            # elif user.is_applicant:
            #     return render(request,'TA_coordr/ta_coordr_home.html',{'name':'TA_Coordinator'})
            else:
                messages.error(request, 'Invalid Credentials!!!')
                return redirect('login_1')

    def sign_up(request):
        if request.method == 'POST':
            firmname=request.POST['firmname']
            firmhead=request.POST['firmhead']
            addr=request.POST['addr']
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            status='inactive'
            region=request.POST['region']
            reg = registration(firmname=firmname, firmhead=firmhead,addr=addr,username=username,email=email,password=password,status=status,region=region)
            reg.save()
            send_mail('New Firm Registration', 'Hi admin, Kindly register the new user '+username, 'cemilac.drdo@gmail.com', ['cemilac.drdo@gmail.com',])
            messages.error(request, 'Successfully Registered!!!')
            return redirect('login_1')

    def newuserreg(request):
        if request.method == 'POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            role_id=request.POST['role']
            date_joined= date.today()
            last_login= date.today()
            is_active=True
            if form.getvalue('superuser'):
                is_superuser = True
            else:
                is_superuser = False

    def adminmenulist1(request):
        return render(request,'login.html')

    def NewUser(request):
        form = UserCreationForm
        navlist=[]
        global apps_list
        if apps_list != []:
            for nav in apps_list:
                print('nav',nav['app_name'])
                navlist.append(nav['app_name'])
        return render(request, 'newuser.html',{'form': form,'navlist':navlist})

  
    def logout(request):
        auth.logout(request)
        return redirect('/')
        
    def get(request):
            reg_list = services.get_all_registration(request)
            print('reg_list',reg_list)
            return render(request,'app_home.html')

    def viewfirm(request):
        navlist=[]
        reg_list = services.get_all_registration(request)
        global apps_list
        if apps_list != []:
            for nav in apps_list:
                print('nav',nav['app_name'])
                navlist.append(nav['app_name'])
        return render(request, 'viewuser.html',{'d':reg_list,'navlist':navlist})
        
            

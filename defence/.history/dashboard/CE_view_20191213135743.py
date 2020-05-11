from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User,Group
from .forms import UserCreationForm,TAapplicationForm,cemilacUserForm,proforma_A_form,checklistForm
from django.contrib import messages
from common.decorators import role_required
from authmgmt.models import registration
from .models import TAapplicationmodel,proforma_A_model,checklistmodel,TAapplicationfiles
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse,HttpResponseRedirect
from .views import link_callback
import os
from io import BytesIO
import pyAesCrypt
from os import stat, remove
from datetime import datetime
from django.utils import formats
import urllib
from datetime import datetime

# @login_required(login_url=settings.LOGIN_URL)
# @role_required(allowed_roles=["RD","TCS-GD",])
# def recommends_ta(request):
#     pro=checklistmodel.objects.all()
#     return render(request, 'rd/viewrecords.html',{'details':pro,'status':True})

# @login_required(login_url=settings.LOGIN_URL)
# @role_required(allowed_roles=["RD","TCS-GD"])
# def newchecklist(request,id):
#     form = checklistForm()
#     return render(request, 'ta coordinator/newchecklist.html',{'form': form,})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-CE"])
def ce_received(request):
    print(request.VG,'VGGGGG')
    reg=TAapplicationmodel.objects.filter(file_in_name="CE")
    return render(request, 'tcs ce/receivedtyperecord.html',{'details':reg,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-CE"])
def CE_forward_GD(request,id):
    reg_by_id=TAapplicationmodel.objects.filter(file_in_name="CE").first()
    reg_by_id.file_in_name='GD'
    reg_by_id.save()

    reg=TAapplicationmodel.objects.filter(file_in_name="CE")
    return render(request, 'tcs ce/receivedtyperecord.html',{'details':reg,'status':True})
    
@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-GD"])
def gd_received(request):
    print(request.VG,'VGGGGG')
    reg=TAapplicationmodel.objects.filter(file_in_name="GD")
    return render(request, 'tcs gd/receivedtyperecord.html',{'details':reg,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-GD"])
def gd_forward_tac(request,id):

    idprefix=request.POST['idprefix']
    reg_by_id=TAapplicationmodel.objects.filter(file_in_name="GD").first()
    reg_by_id.file_in_name='TCS-TAC'
    reg_by_id.save()

    print("ready rd",idprefix,id)

    taapp_form=TAapplicationmodel.objects.filter(user_id=id,idprefix=idprefix).first()
    print("tac_form",taapp_form.id)

    get_taap_id=statusmodel.objects.filter(TAA_id=taapp_form.id).first()
    get_taap_id.status='Send_to_TCS_TAC'
    get_taap_id.Send_to_TCS_TAC=datetime.now()
    get_taap_id.save()
    print("status",get_taap_id)

    reg=TAapplicationmodel.objects.filter(file_in_name="GD")
    return render(request, 'tcs gd/receivedtyperecord.html',{'details':reg,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-TA Coordinator"])
def tac_received(request):
    print(request.VG,'VGGGGG')
    reg=TAapplicationmodel.objects.filter(file_in_name="TCS-TAC")
    return render(request, 'tcs tac/receivedtyperecord.html',{'details':reg,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-TA Coordinator"])
def tac_forward_do(request,id):

    idprefix=request.POST['idprefix']
    reg_by_id=TAapplicationmodel.objects.filter(file_in_name="TCS-TAC").first()
    reg_by_id.file_in_name='TCS-DO'
    reg_by_id.save()

    print("ready rd",idprefix,id)

    taapp_form=TAapplicationmodel.objects.filter(user_id=id,idprefix=idprefix).first()
    print("tac_form",taapp_form.id)

    get_taap_id=statusmodel.objects.filter(TAA_id=taapp_form.id).first()
    get_taap_id.status='Send_to_TCS_DO'
    get_taap_id.Send_to_TCS_DO=datetime.now()
    get_taap_id.save()
    print("status",get_taap_id)

    reg=TAapplicationmodel.objects.filter(file_in_name="TCS-TAC")
    return render(request, 'tcs tac/receivedtyperecord.html',{'details':reg,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-Dealing Officer"])
def do_received(request):
    print(request.VG,'VGGGGG')
    reg=TAapplicationmodel.objects.filter(file_in_name="TCS-DO")
    return render(request, 'tcs do/receivedtyperecord.html',{'details':reg,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-Dealing Officer"])
def DO_verified(request,id):
    reg_by_id=TAapplicationmodel.objects.filter(file_in_name="TCS-DO").first()
    reg_by_id.file_in_name='TCS-DO-Verified'
    reg_by_id.save()

    reg=TAapplicationmodel.objects.filter(file_in_name="TCS-DO")
    # print(request.VG,'VGGGGG')
    # reg=TAapplicationmodel.objects.filter(file_in_name="TCS-DO-Verified")
    return render(request, 'tcs do/receivedtyperecord.html',{'details':reg,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-TA Coordinator"])
def TAC_received_verified(request):
    print(request.VG,'VGGGGG')
    reg=TAapplicationmodel.objects.filter(file_in_name="TCS-DO-Verified")
    return render(request, 'tcs tac/viewtyperecord.html',{'details':reg,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-TA Coordinator"])
def TAC_verified(request,id):
    reg_by_id=TAapplicationmodel.objects.filter(file_in_name="TCS-DO-Verified").first()
    reg_by_id.file_in_name='TCS-TAC-Verified'
    reg_by_id.save()

    # reg=TAapplicationmodel.objects.filter(file_in_name="TCS-DO")
    # print(request.VG,'VGGGGG')
    reg=TAapplicationmodel.objects.filter(file_in_name="TCS-DO-Verified")
    return render(request, 'tcs tac/viewtyperecord.html',{'details':reg,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-GD"])
def gd_received_verified(request):
    print(request.VG,'VGGGGG')
    reg=TAapplicationmodel.objects.filter(file_in_name="TCS-TAC-Verified")
    return render(request, 'tcs gd/viewtyperecord.html',{'details':reg,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-GD"])
def gd_verified(request,id):
    reg_by_id=TAapplicationmodel.objects.filter(file_in_name="TCS-TAC-Verified").first()
    reg_by_id.file_in_name='TCS-GD-Verified'
    reg_by_id.save()

    # reg=TAapplicationmodel.objects.filter(file_in_name="TCS-DO")
    # print(request.VG,'VGGGGG')
    reg=TAapplicationmodel.objects.filter(file_in_name="TCS-TAC-Verified")
    return render(request, 'tcs gd/viewtyperecord.html',{'details':reg,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-CE"])
def ce_received_verified(request):
    print(request.VG,'VGGGGG')
    reg=TAapplicationmodel.objects.filter(file_in_name="TCS-GD-Verified")
    return render(request, 'tcs ce/viewtyperecord.html',{'details':reg,'status':True})
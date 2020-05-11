from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import UserCreationForm,TAapplicationForm,cemilacUserForm,IDGenerationForm,fileUploadForm
from django.core.mail import send_mail
from django.contrib import messages
from common.decorators import role_required
from authmgmt.models import registration,firmregistrationstatusmodel
from django.core.files.storage import FileSystemStorage
import os
import uuid
from datetime import datetime
from os import stat, remove
import pyAesCrypt
from django.http import HttpResponse
from pathlib import Path
import comtypes.client
import pythoncom
from django.contrib.auth.models import User,Group
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import TAapplicationmodel,TAapplicationfiles,idgenerationmodel,statusmodel,commentsmodel
from io import BytesIO
from django.db.models import Count



@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    print(request.role,'ooo')
    context={}
    # if request.role=='TCS-GD' or request.role == 'TCS-CE':
    #     regStatus = firmregistrationstatusmodel.objects.all().values('status').annotate(total=Count('status'))
    #     print("if regpart")
    #     for reg_status_obj in regStatus:
    #         context[reg_status_obj['status']] = reg_status_obj['total']
    #         print('regStatus',context)
    #     return render(request, 'dashboard/dashboard.html',context)
   
    if request.VG is None:
        if request.role=='TA Applicant':
            allStatus = statusmodel.objects.filter(user_id=request.user.id).values('status').annotate(total=Count('status'))
            print("if part",allStatus)
            # status=statusmodel.objects.filter(user_id=request.user.id,status=stauts_from_req,RCMA=request.VG).values('TAA_id')
        else :
            status_to_get ={"Recommended"}            
            allStatus = statusmodel.objects.filter(status__in=status_to_get).values('status').annotate(total=Count('status'))
            print("ELSE part",request.VG)
            regStatus = firmregistrationstatusmodel.objects.all().values('status').annotate(total=Count('status'))

    else :
        allStatus = statusmodel.objects.filter(RCMA=request.VG).values('status').annotate(total=Count('status'))
        #status=statusmodel.objects.filter(user_id=request.user.id,status=stauts_from_req).values('TAA_id')
        # count =statusmodel.objects.filter(status="RCMA_RD_Received").count()
        # print("status",count,request.user.id)
    print("all status",allStatus)        
    for status_obj in allStatus:
        context[status_obj['status']] = status_obj['total']

    for reg_status_obj in regStatus:
        context[reg_status_obj['status']] = reg_status_obj['total']
    print('allstatus',context)
    return render(request, 'dashboard/dashboard.html',context)

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-GD"])
def user_edit(request,id):
    print('sai',id)
    # reg=get_object_or_404(registration,id=id)
    reg=registration.objects.get(pk=id)
    if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():

    #         u = form.save()
    #         send_mail('Registered Successfully!!!', 'Hi '+form.cleaned_data['username']+',You account is Successfully Registered in CEMILAC.Now you can login with the following credentials.Username: '+form.cleaned_data['email']+',Password :'+form.cleaned_data['password1'], 'cemilac.drdo@gmail.com', [form.cleaned_data['email'],])
    #         messages.success(request, 'User Created successfully!')
    #         # navlist=[]
    #         form = UserCreationForm
    #         # if apps_list != []:
    #         #     for nav in apps_list:
    #         #         print('nav1',nav['app_name'])
    #         #         navlist.append(nav['app_name'])
        return render(request, 'app admin/newuser.html', {'form': form,})
    else:
        form = UserCreationForm(instance=reg)
        if reg.remarks=='':
            hold=False
        else:
            hold=True
        print(hold,'holdddddddddd')
    return render(request, 'app admin/newuser.html', {'form': form,'id':id,'hold':hold})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-GD"])
def hold_remarks(request):
    idnew=request.POST['idnew']
    remark=request.POST['remark']
    form = UserCreationForm
    print('idddddddddddd',idnew,remark)
    reg=registration.objects.get(pk=idnew)
    reg.status='hold'
    reg.remarks=remark
    reg.save()

    submitted_date = datetime.now()
    formatted_datetime = submitted_date.strftime("%Y-%m-%d")
    print("registered",formatted_datetime)

    get_taap_id=firmregistrationstatusmodel.objects.filter(email=email).first()
    get_taap_id.status='Hold_Registration'
    get_taap_id.Hold_Registration=formatted_datetime
    get_taap_id.save()

    messages.warning(request, 'D&D Firm Registration Hold!')
    return render(request, 'app admin/newuser.html', {'form': form,})


@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-GD"])
def new_user(request):
    print(request.role)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # if form.is_valid():
        first_name=request.POST['firmname']
        last_name=request.POST['firmhead']
        # addr=request.POST['addr']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        # role=form.cleaned_data.pop('role')
        
        reg=registration.objects.get(email=request.POST['email'])
        reg.status='active'
        reg.save()
        grp=Group.objects.filter(name='TA Applicant').first()
        user = User(first_name=first_name, last_name=last_name,username=username,email=email)
        user.save()
        user.groups.set([grp])
        user.set_password(password)
        user.save()

        submitted_date = datetime.now()
        formatted_datetime = submitted_date.strftime("%Y-%m-%d")
        print("registered",user,user.id,formatted_datetime)

        get_taap_id=firmregistrationstatusmodel.objects.filter(email=email).first()
        get_taap_id.status='Registered_Firms'
        get_taap_id.Registered_Firms=formatted_datetime
        get_taap_id.save()


        # send_mail('Registered Successfully!!!', 'Hi '+form.cleaned_data['username']+',You account is Successfully Registered in CEMILAC.Now you can login with the following credentials.Username: '+form.cleaned_data['email']+',Password :'+form.cleaned_data['password'], 'cemilac.drdo@gmail.com', [form.cleaned_data['email'],])
        messages.success(request, 'D&D Firm successfully Registered as TAapplicant!')
        # navlist=[]
        form = UserCreationForm
        # if apps_list != []:
        #     for nav in apps_list:
        #         print('nav1',nav['app_name'])
        #         navlist.append(nav['app_name'])
        return render(request, 'app admin/newuser.html', {'form': form,})
                # users = User.objects.all()

                # return render(request, 'index.html', {'users': users})
    else:
        form = UserCreationForm

    return render(request, 'app admin/newuser.html', {'form': form,})


@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["App Admin"])
def new_cemilac_user(request):
    print(request.role)
    if request.method == 'POST':
        form = cemilacUserForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            maingroups=form.cleaned_data['maingroups']
            vg=form.cleaned_data['vg']
            mainroles=form.cleaned_data['mainroles']
            print(maingroups,vg,mainroles,'groupppppppppppppppppppp')
            if maingroups=="RCMA":
                grp=Group.objects.filter(name=vg+'-'+mainroles).first()
            elif maingroups=="TCS":
                grp=Group.objects.filter(name='TCS-'+mainroles).first()
            u = form.save()
            u.groups.set([grp])
            date_joined = datetime.now()
            formatted_datetime = date_joined.strftime("%Y-%m-%d")
            u.request_date=formatted_datetime
            u.set_password(password)
            u.save()
            send_mail('Registered Successfully!!!', 'Hi '+form.cleaned_data['username']+',You account is Successfully Registered in CEMILAC.Now you can login with the following credentials.Username: '+form.cleaned_data['email']+',Password :'+form.cleaned_data['password'], 'cemilac.drdo@gmail.com', [form.cleaned_data['email'],])
            messages.success(request, 'User Account Created successfully!')
            # navlist=[]
            form = cemilacUserForm
            # if apps_list != []:
            #     for nav in apps_list:
            #         print('nav1',nav['app_name'])
            #         navlist.append(nav['app_name'])
            return render(request, 'app admin/newcemilacuser.html', {'form': form,})
                # users = User.objects.all()

                # return render(request, 'index.html', {'users': users})
    else:
        form = cemilacUserForm
        print('else')
    return render(request, 'app admin/newcemilacuser.html', {'form': form,})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-GD"])
def viewregistration(request):
    reg=registration.objects.filter(status="active")
    return render(request, 'app admin/viewregistration.html',{'details':reg,'view':False,'status':'active'})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-GD"])
def viewunregistration(request):
    reg=registration.objects.filter(status="inactive")
    return render(request, 'app admin/viewregistration.html',{'details':reg,'view':True,'status':'inactive'})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-GD"])
def hold(request):
    reg=registration.objects.filter(status="hold")
    return render(request, 'app admin/viewregistration.html',{'details':reg,'view':True,'status':'hold'})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Applicant"])
def newtypeapproval(request):
    idprefix=request.POST['idpre']
    idnew=request.POST['idnew']
    form = TAapplicationForm(request=request.user,idpre=idprefix)
    date_joined = datetime.now()
    formatted_datetime = date_joined.strftime("%Y-%m-%d")
    idg=idgenerationmodel.objects.filter(user_id=request.user.id,idprefix=idprefix).first()
    idg.submitted_date=formatted_datetime
    idg.save()
    taa=TAapplicationmodel.objects.filter(user_id=request.user.id,idprefix=idprefix)
    if taa:
        messages.success(request, 'Application successfully submitted !')
        return render(request, 'applicant/newtypeapproval.html')
    else:
        return render(request, 'applicant/newtypeapproval.html',{'form': form,'idprefix':idprefix,'idnew':idnew})


@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-GD"])
def fileView(request):
    aesurl=request.POST['url']
    ext=request.POST['ext']
    print('aesview',aesurl)

    pdfurl=''
    docurl=''
    nameonly=''
    if ext=='.pdf':
        pdfurl = aesurl[:-3]+'pdf'
        print('aesview',aesurl)
        print('pdfview',pdfurl)

            # (should store the filename and extension in db for) decrypt the file
        try:
            bufferSize = 64 * 1024
            passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
            encFileSize = stat(aesurl).st_size
            with open(aesurl, "rb") as fIn:
                with open(pdfurl, "wb") as fOut:
                    pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
            with open(pdfurl, 'rb') as pdf:
                response = HttpResponse(pdf.read(),content_type='application/pdf')
                response['Content-Disposition'] = 'filename=some_file.pdf'
            return response
        finally:
            os.remove(pdfurl) 

    elif ext=='docx':
        # word to pdf 
        nameonly=aesurl[:-4]
        docurl = aesurl[:-4]+'.docx'
        print('aesview',aesurl)
        print('nameonly',nameonly)
        print('docurl',docurl)

        try:
            bufferSize = 64 * 1024
            passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
            encFileSize = stat(aesurl).st_size
            with open(aesurl, "rb") as fIn:
                with open(docurl, "wb") as fOut:
                    pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)

            pythoncom.CoInitialize()
            wdFormatPDF = 17
            # print(tempfile.gettempdir(),'temp')

            in_file = os.path.abspath(docurl)
            # out_file = os.path.abspath('D:/cemilac/certa/defence/media/org1.pdf')

            word = comtypes.client.CreateObject('Word.Application')
            doc = word.Documents.Open(in_file)
            doc.SaveAs(nameonly+'.pdf', FileFormat=wdFormatPDF)
            doc.Close()
            word.Quit()
            with open(nameonly+'.pdf', 'rb') as pdf:
                response = HttpResponse(pdf.read(),content_type='application/pdf')
                response['Content-Disposition'] = 'filename=some_file.pdf'
            return response
        finally:
            os.remove(nameonly+'.pdf')
            os.remove(docurl)

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Applicant"])
def generatepdf(request):
    if request.POST:
        # dal_mdi_files = request.FILES.getlist('dal_mdi_file')
        # for f in dal_mdi_files:
        #     print(f.name,'myfile')
        #     fn=f.name
        #     ext=fn[-4:]
        #     print(ext,'ext')
        #     extension=ext

        #     curr_path = "/"+str(request.user.id)+ "/DAL_MDI/"
        #     curr_path=curr_path.replace('/','\\')
        #     new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
        #     print(new_path,'newpath')

        #     fs = FileSystemStorage(location=new_path , base_url = new_path )

        #     unique_filename = str(uuid.uuid4())
        #     filename = fs.save(unique_filename, f)
        #     uploaded_file_url = fs.path(filename)
        #     print(uploaded_file_url,'url')

        
        #     bufferSize = 64 * 1024
        #     passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
        #     with open(uploaded_file_url, "rb") as fIn:
        #         with open(uploaded_file_url+".aes", "wb") as fOut:
        #             pyAesCrypt.encryptStream(fIn, fOut, passw, bufferSize)

        #     remove(uploaded_file_url)
        #     taf = TAapplicationfiles(filecategory='DAL_MDI', filepath=uploaded_file_url+".aes",ext=extension,user_id=request.user.id)
        #     taff=taf.save()

        # bom_files = request.FILES.getlist('bom_file')
        # for f in bom_files:
        #     print(f.name,'myfile')
        #     fn=f.name
        #     ext=fn[-4:]
        #     print(ext,'ext')
        #     extension=ext

        #     curr_path = "/"+str(request.user.id)+ "/BOM/"
        #     curr_path=curr_path.replace('/','\\')
        #     new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
        #     print(new_path,'newpath')

        #     fs = FileSystemStorage(location=new_path , base_url = new_path )

        #     unique_filename = str(uuid.uuid4())
        #     filename = fs.save(unique_filename, f)
        #     uploaded_file_url = fs.path(filename)
        #     print(uploaded_file_url,'url')

        
        #     bufferSize = 64 * 1024
        #     passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
        #     with open(uploaded_file_url, "rb") as fIn:
        #         with open(uploaded_file_url+".aes", "wb") as fOut:
        #             pyAesCrypt.encryptStream(fIn, fOut, passw, bufferSize)

        #     remove(uploaded_file_url)
        #     taf = TAapplicationfiles(filecategory='BOM', filepath=uploaded_file_url+".aes",ext=extension,user_id=request.user.id)
        #     taff=taf.save()

        # sop_acbs_files = request.FILES.getlist('sop_acbs_file')
        # for f in sop_acbs_files:
        #     print(f.name,'myfile')
        #     fn=f.name
        #     ext=fn[-4:]
        #     print(ext,'ext')
        #     extension=ext

        #     curr_path = "/"+str(request.user.id)+ "/SOP_ACBS/"
        #     curr_path=curr_path.replace('/','\\')
        #     new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
        #     print(new_path,'newpath')

        #     fs = FileSystemStorage(location=new_path , base_url = new_path )

        #     unique_filename = str(uuid.uuid4())
        #     filename = fs.save(unique_filename, f)
        #     uploaded_file_url = fs.path(filename)
        #     print(uploaded_file_url,'url')

        
        #     bufferSize = 64 * 1024
        #     passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
        #     with open(uploaded_file_url, "rb") as fIn:
        #         with open(uploaded_file_url+".aes", "wb") as fOut:
        #             pyAesCrypt.encryptStream(fIn, fOut, passw, bufferSize)

        #     remove(uploaded_file_url)
        #     taf = TAapplicationfiles(filecategory='SOP_ACBS', filepath=uploaded_file_url+".aes",ext=extension,user_id=request.user.id)
        #     taff=taf.save()
        
        form = TAapplicationForm(request.POST,request.FILES)
        if form.is_valid():
            idprefix=request.POST['idprefix']
            taf=idgenerationmodel.objects.get(user_id=request.user.id,idprefix=idprefix)
            print(idprefix,'iiiiiiiiiiiid')

             # current Date
            date_joined = datetime.now()
            formatted_datetime = date_joined.strftime("%Y-%m-%d")

            taapp= form.save(commit=False)
            taapp.user = request.user
            taapp.submitted_date = formatted_datetime
            
            taapp.file_in_name="RD"
            taapp.rcma=taf.rcma
            taapp.idprefix=idprefix
            taapp.save()

            submitted_date = datetime.now()
            print("taapp",taapp,taapp.id,taapp.rcma,submitted_date)
            tastatus = statusmodel(TAA_id=taapp.id, RCMA=taapp.rcma,status="RCMA_RD_Received",RCMA_RD_Received=submitted_date,user_id=request.user.id)
            tastatusdb=tastatus.save()

            messages.success(request, 'TA Application Submitted Successfully!')
            
            myfile = request.FILES['sign']  
            curr_path = "/"+str(request.user.id)
            curr_path=curr_path.replace('/','\\')
            new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
            print(new_path,'newpath')

            fs = FileSystemStorage(location=new_path , base_url = new_path )

            # unique_filename = str(uuid.uuid4())
            filename = fs.save(str(request.user.id)+".jpg", myfile)
            uploaded_file_url = fs.path(filename)
            print(uploaded_file_url,'url')

            

            template = get_template('applicant/newtypeapprovalpdf.html')
            context= {
                'firmname':request.POST['firmname'],
                'addr1':request.POST['addr1'],
                'addr2':request.POST['addr2'],
                'tot':request.POST['tot'],
                'item_name':request.POST['item_name'],
                'part_no':request.POST['part_no'],
                'desc':request.POST['desc'],
                'spec': request.POST['spec'],
                'dal_mdi':request.POST['dal_mdi'],
                'bom':request.POST['bom'],
                'sop_acbs':request.POST['sop_acbs'],
                'pc': request.POST['pc'],
                'tre':request.POST['tre'],
                'otheritems':request.POST['otheritems'],
                'sign':uploaded_file_url,
                'designation':request.POST['designation'],
                'date':formatted_datetime,
                'addr':request.POST['addr']

            }
            html = template.render(context)


            curr_path = "/"+str(request.user.id)+"/"+idprefix+"Annexure 1/TAapplication/"
            curr_path=curr_path.replace('/','\\')
            new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
            os.makedirs(new_path)
            result = open(new_path+"TAapplication.pdf", 'wb')
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result,link_callback=link_callback)
            result.close()
            taf = TAapplicationfiles(filecategory='TAapplication', filepath=new_path+"TAapplication.pdf",ext=".pdf",user_id=request.user.id,refid=idprefix,refpath='Annexure 1')
            taff=taf.save()
            remove(uploaded_file_url) 
            return render(request, 'applicant/newtypeapproval.html')
        else:
            print('ddddddd')
            return render(request, 'applicant/newtypeapproval.html')

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Applicant"])
def id_gen(request):
    form = IDGenerationForm(request=request.user)
    return render(request, 'applicant/idgeneration.html',{'form': form,})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Applicant"])
def new_id_generate(request):
    # form = IDGenerationForm(request=request.user)
    # if form.is_valid():
    form = IDGenerationForm(request.POST)

    sfirmname=request.POST['sfirmname']
    sprodname=request.POST['sprodname']
    rcma=request.POST['rcma']
    i=form.save(commit=False)
    i.idprefix=sfirmname+'/'+sprodname+'/'+rcma+'/'
    i.user_id = request.user.id
    date_joined = datetime.now()
    formatted_datetime = date_joined.strftime("%Y-%m-%d")
    i.registered_date=formatted_datetime
    i.save()
    messages.success(request, 'New Product Added successfully')
    return render(request, 'applicant/idgeneration.html')

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Applicant"])
def upload_refdoc(request):
    idg=idgenerationmodel.objects.filter(user_id=request.user.id)
    return render(request, 'applicant/view_all_id.html',{'details': idg,'taapp':False})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Applicant"])
def upload_taapplication(request):
    idg=idgenerationmodel.objects.filter(user_id=request.user.id)
    return render(request, 'applicant/view_all_id.html',{'details': idg,'taapp':True})


@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Applicant"])
def doc_upload_views(request):
    form=fileUploadForm
    idprefix=request.POST['idpre']  
    print('idprefixxxxxxxxxxxxxx')
    print(idprefix,'idprefix')
    taf=TAapplicationfiles.objects.filter(user_id=request.user.id,refid=idprefix).order_by('refpath')
    idg=idgenerationmodel.objects.filter(user_id=request.user.id,idprefix=idprefix).first()
    return render(request, 'applicant/view_all_doc.html',{'form':form,'details': taf,'idg':idg,'idprefix':idprefix})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Applicant"])
def doc_add(request):
    idprefix=request.POST['idprefix']
    print(idprefix,'xxxxxxxxxxxxx')

    if request.POST:
        filecategory=request.POST['filecategory']
        refdate=request.POST['refdate']
        file_refno=request.POST['file_refno']
        print(filecategory,refdate,'fc')
        files = request.FILES['files']

        if filecategory=='TOT':
            newpath='Annexure 1.1/'+filecategory
            refpath='Annexure 1.1'
        elif filecategory=='Brief_Desc':
            newpath='Annexure 2/'+filecategory
            refpath='Annexure 2'
        elif filecategory=='Cont_TR':
            newpath='Annexure 4/'+filecategory
            refpath='Annexure 4'
        elif filecategory=='PH':
            newpath='Annexure 4.1/'+filecategory
            refpath='Annexure 4.1'
        elif filecategory=='Tech_Spec':
            newpath='Annexure 4.2/'+filecategory
            refpath='Annexure 4.2'
        elif filecategory=='DAL_MDI':
            newpath='Annexure 4.3/'+filecategory
            refpath='Annexure 4.3'
        elif filecategory=='BOM':
            newpath='Annexure 4.4/'+filecategory
            refpath='Annexure 4.4'
        elif filecategory=='SOP_ACBS':
            newpath='Annexure 4.5/'+filecategory
            refpath='Annexure 4.5'
        elif filecategory=='Pro_Doc':
            newpath='Annexure 4.6/'+filecategory
            refpath='Annexure 4.6'
        elif filecategory=='QTS':
            newpath='Annexure 4.7/'+filecategory
            refpath='Annexure 4.7'
        elif filecategory=='QTR':
            newpath='Annexure 4.8/'+filecategory
            refpath='Annexure 4.8'
        elif filecategory=='Comp_TR':
            newpath='Annexure 4.9/'+filecategory
            refpath='Annexure 4.9'
        elif filecategory=='COD':
            newpath='Annexure 4.10/'+filecategory
            refpath='Annexure 4.10'
        elif filecategory=='FER':
            newpath='Annexure 4.11/'+filecategory
            refpath='Annexure 4.11'
        elif filecategory=='Per_Fb':
            newpath='Annexure 4.12/'+filecategory
            refpath='Annexure 4.12'
        elif filecategory=='PC':
            newpath='Annexure 4.13/'+filecategory
            refpath='Annexure 4.13'
        elif filecategory=='Drawings':
            newpath='Annexure 5/'+filecategory
            refpath='Annexure 5'
        elif filecategory=='TA_Data_Sheet':
            newpath='Annexure 6/'+filecategory
            refpath='Annexure 6'


        i = 1
        # for f in files:
        print(files.name,'myfile')
        fn=files.name
        ext=fn[-4:]
        print(ext,'ext')
        extension=ext

        curr_path = "/"+str(request.user.id)+ "/"+idprefix+newpath+"/"
        curr_path=curr_path.replace('/','\\')
        new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
        print(new_path,'newpath')

        fs = FileSystemStorage(location=new_path , base_url = new_path )

        # unique_filename = str(uuid.uuid4())
        # filename = fs.save(unique_filename, files)
        filename = fs.save(files.name, files)
        uploaded_file_url = fs.path(filename)
        print(uploaded_file_url,'url')

    
        bufferSize = 64 * 1024
        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
        with open(uploaded_file_url, "rb") as fIn:
            with open(uploaded_file_url+".aes", "wb") as fOut:
                pyAesCrypt.encryptStream(fIn, fOut, passw, bufferSize)

        # refpath=idprefix+newpath+ "/"+files.name
        i+=1
        remove(uploaded_file_url)
        taf = TAapplicationfiles(filecategory=filecategory, filepath=uploaded_file_url+".aes",ext=extension,user_id=request.user.id,refid=idprefix,refpath=refpath,refdate=refdate,file_refno=file_refno,relation='parent')
        taff=taf.save()

        print('idprefixxx')
        print(idprefix,'idprefix')
        form=fileUploadForm
        taf=TAapplicationfiles.objects.filter(user_id=request.user.id,refid=idprefix).order_by('refpath')
        idg=idgenerationmodel.objects.filter(user_id=request.user.id,idprefix=idprefix).first()
        # get_refpath=TAapplicationfiles.objects.filter(user_id=request.user.id,refid=idprefix).values('refpath').order_by('refpath')

        # print(get_refpath,'get_refpath')

        # for anex_name in get_refpath:
        #     anexture_name = anex_name['refpath']
        #     print(anexture_name,'taff')
        #     comments = commentsmodel(name=anexture_name,idprefix=idprefix,user_id=request.user.id)
        #     commentsdb=comments.save()

        return render(request, 'applicant/view_all_doc.html',{'form':form,'details': taf,'idg':idg,'idprefix':idprefix})
    else:
        print('idprefixxx')
        print(idprefix,'idprefix')
        form=fileUploadForm
        taf=TAapplicationfiles.objects.filter(user_id=request.user.id).order_by('refpath')
        return render(request, 'applicant/view_all_doc.html',{'form':form,'details': taf,'idprefix':idprefix})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Applicant"])
def addanotherdoc(request):

    idnew=request.POST['idnew']

    refpath=request.POST['refp']
    idprefix=request.POST['idprefix']
    fcat=request.POST['fcat']
    refdate=request.POST['refd']
    file_refno=request.POST['refn']
    files = request.FILES['updoc']
    tafcount=TAapplicationfiles.objects.filter(user_id=request.user.id,filecategory=fcat,refid=idprefix).count()
    refpathcount = str(refpath[9:])+'.'+str(tafcount)
    newrefpath='Annexure '+str(refpathcount)
    ann_ex=TAapplicationfiles.objects.filter(refpath=newrefpath,user_id=request.user.id).exists()
    if ann_ex:
        form=fileUploadForm
        taf=TAapplicationfiles.objects.filter(user_id=request.user.id).order_by('refpath')
        idg=idgenerationmodel.objects.filter(user_id=request.user.id,idprefix=idprefix).first()
        print(idnew,refpath,fcat,refpathcount,'nnnnnnnnnnnnnnnnnn')
        return render(request, 'applicant/view_all_doc.html',{'form':form,'details': taf,'idg':idg,'idprefix':idprefix})
    else:
        newpath=refpath+'/'+fcat+'/'+newrefpath

        print(files.name,'myfile')
        fn=files.name
        ext=fn[-4:]
        print(ext,'ext')
        extension=ext

        curr_path = "/"+str(request.user.id)+ "/"+idprefix+newpath+"/"
        curr_path=curr_path.replace('/','\\')
        new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
        print(new_path,'newpath')

        fs = FileSystemStorage(location=new_path , base_url = new_path )

        # unique_filename = str(uuid.uuid4())
        # filename = fs.save(unique_filename, files)
        filename = fs.save(files.name, files)
        uploaded_file_url = fs.path(filename)
        print(uploaded_file_url,'url')


        bufferSize = 64 * 1024
        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
        with open(uploaded_file_url, "rb") as fIn:
            with open(uploaded_file_url+".aes", "wb") as fOut:
                pyAesCrypt.encryptStream(fIn, fOut, passw, bufferSize)

        # refpath=idprefix+newpath+ "/"+files.name
        remove(uploaded_file_url)

        taf = TAapplicationfiles(filecategory=fcat, filepath=uploaded_file_url+".aes",ext=extension,user_id=request.user.id,refid=idprefix,refpath=newrefpath,refdate=refdate,file_refno=file_refno,relation='child')
        taff=taf.save()
        form=fileUploadForm
        taf=TAapplicationfiles.objects.filter(user_id=request.user.id).order_by('refpath')
        idg=idgenerationmodel.objects.filter(user_id=request.user.id,idprefix=idprefix).first()
        print(idnew,refpath,fcat,refpathcount,'nnnnnnnnnnnnnnnnnn')
        return render(request, 'applicant/view_all_doc.html',{'form':form,'details': taf,'idg':idg,'idprefix':idprefix})
    
@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Applicant"])
def doc_change(request):
    idnew=request.POST['idnew']

    refpath=request.POST['refp']
    idprefix=request.POST['idprefix']
    fcat=request.POST['fcat']
    refdate=request.POST['refd']
    file_refno=request.POST['refn']
    files = request.FILES['updoc']
    ann_ex=TAapplicationfiles.objects.filter(refpath=refpath,user_id=request.user.id,refid=idprefix).first()
    remove(ann_ex.filepath)
    if ann_ex.relation=='parent':
        newpath=refpath+'/'+fcat
    else:
        newpath=refpath[-2:]+'/'+fcat+'/'+refpath
    print(newpath,'pathhhhhhhhhhhh')
    print(files.name,'myfile')
    fn=files.name
    ext=fn[-4:]
    print(ext,'ext')
    extension=ext

    curr_path = "/"+str(request.user.id)+ "/"+idprefix+newpath+"/"
    curr_path=curr_path.replace('/','\\')
    new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
    print(new_path,'newpath')

    fs = FileSystemStorage(location=new_path , base_url = new_path )

    # unique_filename = str(uuid.uuid4())
    # filename = fs.save(unique_filename, files)
    filename = fs.save(files.name, files)
    uploaded_file_url = fs.path(filename)
    print(uploaded_file_url,'url')


    bufferSize = 64 * 1024
    passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
    with open(uploaded_file_url, "rb") as fIn:
        with open(uploaded_file_url+".aes", "wb") as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, passw, bufferSize)

    # refpath=idprefix+newpath+ "/"+files.name
    remove(uploaded_file_url)
    ann_ex.filepath=uploaded_file_url+".aes"
    ann_ex.refdate=refdate
    ann_ex.file_refno=file_refno
    # taf = TAapplicationfiles(filecategory=fcat, filepath=uploaded_file_url+".aes",ext=extension,user_id=request.user.id,refid=idprefix,refpath=refpath,refdate=refdate,file_refno=file_refno,relation='child')
    taff=ann_ex.save()
    form=fileUploadForm
    taf=TAapplicationfiles.objects.filter(user_id=request.user.id).order_by('refpath')
    idg=idgenerationmodel.objects.filter(user_id=request.user.id,idprefix=idprefix).first()
    print(idnew,refpath,fcat,'nnnnnnnnnnnnnnnnnn')
    return render(request, 'applicant/view_all_doc.html',{'form':form,'details': taf,'idg':idg,'idprefix':idprefix})
    # else:
    #     newpath=refpath+'/'+fcat+'/'+newrefpath

    #     print(files.name,'myfile')
    #     fn=files.name
    #     ext=fn[-4:]
    #     print(ext,'ext')
    #     extension=ext

    #     curr_path = "/"+str(request.user.id)+ "/"+idprefix+newpath+"/"
    #     curr_path=curr_path.replace('/','\\')
    #     new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
    #     print(new_path,'newpath')

    #     fs = FileSystemStorage(location=new_path , base_url = new_path )

    #     # unique_filename = str(uuid.uuid4())
    #     # filename = fs.save(unique_filename, files)
    #     filename = fs.save(files.name, files)
    #     uploaded_file_url = fs.path(filename)
    #     print(uploaded_file_url,'url')


    #     bufferSize = 64 * 1024
    #     passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
    #     with open(uploaded_file_url, "rb") as fIn:
    #         with open(uploaded_file_url+".aes", "wb") as fOut:
    #             pyAesCrypt.encryptStream(fIn, fOut, passw, bufferSize)

    #     # refpath=idprefix+newpath+ "/"+files.name
    #     remove(uploaded_file_url)

    #     taf = TAapplicationfiles(filecategory=fcat, filepath=uploaded_file_url+".aes",ext=extension,user_id=request.user.id,refid=idprefix,refpath=newrefpath,refdate=refdate,file_refno=file_refno,relation='child')
    #     taff=taf.save()
    #     form=fileUploadForm
    #     taf=TAapplicationfiles.objects.filter(user_id=request.user.id)
    #     idg=idgenerationmodel.objects.filter(user_id=request.user.id,idprefix=idprefix).first()
    #     print(idnew,refpath,fcat,refpathcount,'nnnnnnnnnnnnnnnnnn')
    #     return render(request, 'applicant/view_all_doc.html',{'form':form,'details': taf,'idg':idg,'idprefix':idprefix})
    

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Applicant","RD","TA Coordinator","Dealing Officer","TCS-CE","TCS-GD",
"TCS-TA Coordinator","TCS-Dealing Officer"])
def dashboard_status(request):
    stauts_from_req=request.GET['st']
    if request.VG is None:
        if request.role=='TA Applicant':
            get_firm_id=statusmodel.objects.filter(user_id=request.user.id,status=stauts_from_req).values('TAA_id')
            print("inside iF",request.user.id,get_firm_id)
        else :
            get_firm_id = statusmodel.objects.filter(status=stauts_from_req,RCMA=request.VG).values('TAA_id')
            print(" inside ELSE ")

    else :
        get_firm_id=statusmodel.objects.filter(status=stauts_from_req,RCMA=request.VG).values('TAA_id')

    formid=TAapplicationmodel.objects.filter(id__in=[get_firm_id]) 
    print("formid",formid) 
    context={
        'formid':formid
    }
    return render(request, 'dashboard/dashboard_count.html',{'firmdetails': formid})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-CE","TCS-GD"])
def reg_dashboard_status(request):
    print('inside method')
    stauts_from_req=request.GET['st']
    regStatus = firmregistrationstatusmodel.objects.filter(status=stauts_from_req).values('email')
    print("if regpart",regStatus)
    user_details=registration.objects.filter(email__in=[regStatus]) 
    print("user_details",user_details) 
    context={'user_details': user_details}
    return render(request, 'dashboard/register_dashboard.html',context)
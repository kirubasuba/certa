from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User,Group
from .forms import UserCreationForm,TAapplicationForm,cemilacUserForm,proforma_A_form,checklistForm
from django.contrib import messages
from common.decorators import role_required
from authmgmt.models import registration
from .models import TAapplicationmodel,proforma_A_model,checklistmodel,TAapplicationfiles,statusmodel
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

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["RD","TCS-GD",])
def recommends_ta(request):
    pro=checklistmodel.objects.all()
    return render(request, 'rd/viewrecords.html',{'details':pro,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["RD","TCS-GD"])
def newchecklist(request,id):
    form = checklistForm()
    return render(request, 'ta coordinator/newchecklist.html',{'form': form,})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["RD"])
def RD_received(request):
    print(request.VG,'VGGGGG')
    reg=TAapplicationmodel.objects.filter(rcma=request.VG,file_in_name="RD")
    return render(request, 'rd/viewtyperecord.html',{'details':reg,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["RD"])
def RD_forward_tac(request,id):
    reg_by_id=TAapplicationmodel.objects.filter(rcma=request.VG,file_in_name="RD",user_id=id).first()
    reg_by_id.file_in_name='TAC'
    reg_by_id.save()

    get_taap_id=statusmodel.objects.filter(TAA_id=reg_by_id.id).first()
    get_taap_id.status='Send_to_RCMA_TAC'
    get_taap_id.Send_to_RCMA_TAC=datetime.now()
    get_taap_id.save()
    
    print("status",get_taap_id)
    reg=TAapplicationmodel.objects.filter(rcma=request.VG,file_in_name="RD")
    return render(request, 'rd/viewtyperecord.html',{'details':reg,'status':True})
    
@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["RD","TCS-GD"])
def sign_pass(request):
    if request.role=="RD":
        password=request.POST['pass']
        if password=="kiruba":
            idnew=request.POST['idnew']
            idprefix=request.POST['idprefix']
            print('password',password,idnew,idprefix)

            curr_path = "/sign/rd_signature.aes"
            curr_path=curr_path.replace('/','\\')
            new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
            print(new_path,'newpath')


            #encryption
            
            # bufferSize = 64 * 1024
            # passw = "kiruba"
            # with open(new_path, "rb") as fIn:
            #     with open(new_path[:-4]+".aes", "wb") as fOut:
            #         pyAesCrypt.encryptStream(fIn, fOut, passw, bufferSize)

            imgurl = new_path[:-4]+".png"
            print('docurl',imgurl)

            bufferSize = 64 * 1024
            passw = "kiruba"
            encFileSize = stat(new_path).st_size
            with open(new_path, "rb") as fIn:
                with open(imgurl, "wb") as fOut:
                    pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)

            form = proforma_A_form(request=idnew,idpre=idprefix)
            print('sai',idnew)
            pro=proforma_A_model.objects.filter(user_id=idnew,idprefix=idprefix).first()
            taa=TAapplicationmodel.objects.filter(user_id=idnew,idprefix=idprefix).first()
            if pro:
                template = get_template('dealing officer/proformapdf.html')
                date_joined = datetime.now()
                formatted_datetime = date_joined.strftime("%Y-%m-%d")
                print(formatted_datetime,'dte')
                context= {
                    'firmname':taa.firmname,
                    'addr1':taa.addr1,
                    'addr2':taa.addr2,
                    'item_name':taa.item_name,
                    'part_no':taa.part_no,
                    'desc':taa.desc,
                    'dal_mdi':taa.dal_mdi,
                    'bom':taa.bom,
                    'sop_acbs':taa.sop_acbs,
                    'pc': taa.pc,
                    'tre':taa.tre,
                    'otheritems':taa.otheritems,
                    
                    'ta': pro.ta,
                    'techspec': pro.techspec,
                    'qts': pro.qts,
                    'qtr': pro.qtr,
                    'cd': pro.cd,
                    'photo': pro.photo,
                    'feedback': pro.feedback,
                    'req': pro.req,
                    'cost': pro.cost,
                    'quantity': pro.quantity,
                    'pc': pro.pc,
                    'tacomments':pro.tacomments,
                    'sign':imgurl,
                    'datenow':formatted_datetime
                }
                html = template.render(context)
                curr_path = "/"+str(idnew)+"/"+idprefix+"/Annexure 3/Proforma_A"
                curr_path=curr_path.replace('/','\\')
                new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
                os.makedirs(new_path)
                result = open(new_path+"/Proforma_A.pdf", 'wb')
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result,link_callback=link_callback)
                result.close()

                taa.file_in_name='GD'
                taa.save()
                form = checklistForm()
                print('sai',idnew)
                ck=checklistmodel.objects.filter(user_id=idnew,idprefix=idprefix).first()
                if ck:
                    template = get_template('ta coordinator/checklistpdf.html')
                    # date_joined = datetime.now()
                    # formatted_datetime = date_joined.strftime("%Y-%m-%d")
                    # print(formatted_datetime,'dte')
                    context= {
                        'application':ck.application,
                        'proforma':ck.proforma,
                        'desc':ck.desc,
                        'typerecord':ck.typerecord,
                        'drawings':ck.drawings,
                        'css_qts':ck.css_qts,
                        'dtac':ck.dtac,
                        'sign':imgurl,
                        'datenow':formatted_datetime
                    }
                    html = template.render(context)
                    curr_path = "/"+str(idnew)+"/"+idprefix+"Annexure 1/Checklist"
                    curr_path=curr_path.replace('/','\\')
                    new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
                    os.makedirs(new_path)
                    result = open(new_path+"/Checklist.pdf", 'wb')
                    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result,link_callback=link_callback)
                    result.close()
                    ck.status="Recommended by RCMA RD"
                    ck.save()

                    print("ready rd",ck.idprefix,idnew)

                    taapp_form=TAapplicationmodel.objects.filter(user_id=idnew,idprefix=idprefix).first()
                    print("tac_form",taapp_form.id)

                    get_taap_id=statusmodel.objects.filter(TAA_id=taapp_form.id).first()
                    get_taap_id.status='Recommended'
                    get_taap_id.Recommended=datetime.now()
                    get_taap_id.save()
                    print("status",get_taap_id)

                    remove(imgurl)
                    messages.success(request, 'Type Record Successfully Forwarded to TCS-GD !!')
                    # reg_by_id=TAapplicationmodel.objects.filter(rcma=request.VG,file_in_name='AIR-DO1',user_id=id).first()
                    # reg_by_id.file_in_name='CE'
                    # reg_by_id.save()
        else:
            messages.warning(request, 'Wrong Password')

        pro=checklistmodel.objects.all()
        return render(request, 'rd/viewrecords.html',{'details':pro,'status':True})
    else:
        password=request.POST['pass']
        if password=="loga":
            idnew=request.POST['idnew']
            print('password',password,idnew)

            curr_path = "/sign/GD_sign.aes"
            curr_path=curr_path.replace('/','\\')
            new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
            print(new_path,'newpath')


            #encryption
            
            # bufferSize = 64 * 1024
            # passw = "loga"
            # with open(new_path, "rb") as fIn:
            #     with open(new_path[:-4]+".aes", "wb") as fOut:
            #         pyAesCrypt.encryptStream(fIn, fOut, passw, bufferSize)

            imgurl = new_path[:-4]+".png"
            print('docurl',imgurl)

            bufferSize = 64 * 1024
            passw = "loga"
            encFileSize = stat(new_path).st_size
            with open(new_path, "rb") as fIn:
                with open(imgurl, "wb") as fOut:
                    pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
            ck=checklistmodel.objects.filter(user_id=idnew).first()
            taa=TAapplicationmodel.objects.filter(user_id=idnew).first()
            template = get_template('dealing officer/Draft TA pdf.html')
            
            context= {
                'firmname':taa.firmname,
                'addr1':taa.addr1,
                'item_name':taa.item_name,
                'part_no':taa.part_no,
                'sign':imgurl,
            }
            html = template.render(context)

            curr_path = "/"+str(idnew)+ "/Draft_TA"
            curr_path=curr_path.replace('/','\\')
            new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
            os.makedirs(new_path)
            result = open(new_path+"/Draft_TA.pdf", 'wb')
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result,link_callback=link_callback)
            result.close()
            messages.success(request, 'Type Record with related documents are Approved !!')
            ck.status="Approved by TCS-GD"
            ck.save()
            remove(imgurl)
            print('elseeeeee')
            pro=checklistmodel.objects.all()
            return render(request, 'rd/viewrecords.html',{'details':pro,'status':True})
        else:
            messages.warning(request, 'Wrong Password')

        pro=checklistmodel.objects.all()
        return render(request, 'rd/viewrecords.html',{'details':pro,'status':True})


@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TCS-GD"])
def sign_pass_TCSGD(request):
    password=request.POST['pass']
    if password=="loga":
        idnew=request.POST['idnew']
        print('password',password,idnew)

        curr_path = "/sign/GD_sign.aes"
        curr_path=curr_path.replace('/','\\')
        new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
        print(new_path,'newpath')


        #encryption
        
        # bufferSize = 64 * 1024
        # passw = "kiruba"
        # with open(new_path, "rb") as fIn:
        #     with open(new_path[:-4]+".aes", "wb") as fOut:
        #         pyAesCrypt.encryptStream(fIn, fOut, passw, bufferSize)

        # imgurl = new_path[:-4]+".png"
        # print('docurl',imgurl)

        # bufferSize = 64 * 1024
        # passw = "kiruba"
        # encFileSize = stat(new_path).st_size
        # with open(new_path, "rb") as fIn:
        #     with open(imgurl, "wb") as fOut:
        #         pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)

        # form = proforma_A_form(request=idnew)
        # print('sai',idnew)
        # pro=proforma_A_model.objects.filter(user_id=idnew).first()
        # taa=TAapplicationmodel.objects.filter(user_id=idnew).first()
        # if pro:
        #     template = get_template('dealing officer/proformapdf.html')
        #     date_joined = datetime.now()
        #     formatted_datetime = date_joined.strftime("%Y-%m-%d")
        #     print(formatted_datetime,'dte')
        #     context= {
        #         'firmname':taa.firmname,
        #         'addr1':taa.addr1,
        #         'addr2':taa.addr2,
        #         'item_name':taa.item_name,
        #         'part_no':taa.part_no,
        #         'desc':taa.desc,
        #         'dal_mdi':taa.dal_mdi,
        #         'bom':taa.bom,
        #         'sop_acbs':taa.sop_acbs,
        #         'pc': taa.pc,
        #         'tre':taa.tre,
        #         'otheritems':taa.otheritems,
                
        #         'ta': pro.ta,
        #         'techspec': pro.techspec,
        #         'qts': pro.qts,
        #         'qtr': pro.qtr,
        #         'cd': pro.cd,
        #         'photo': pro.photo,
        #         'feedback': pro.feedback,
        #         'req': pro.req,
        #         'cost': pro.cost,
        #         'quantity': pro.quantity,
        #         'pc': pro.pc,
        #         'tacomments':pro.tacomments,
        #         'sign':imgurl,
        #         'datenow':formatted_datetime
        #     }
        #     html = template.render(context)
        #     curr_path = "/"+str(idnew)+ "/Proforma_A"
        #     curr_path=curr_path.replace('/','\\')
        #     new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
        #     os.makedirs(new_path)
        #     result = open(new_path+"/Proforma_A.pdf", 'wb')
        #     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result,link_callback=link_callback)
        #     result.close()


        #     form = checklistForm()
        #     print('sai',idnew)
        #     ck=checklistmodel.objects.filter(user_id=idnew).first()
        #     if ck:
        #         template = get_template('ta coordinator/checklistpdf.html')
        #         # date_joined = datetime.now()
        #         # formatted_datetime = date_joined.strftime("%Y-%m-%d")
        #         # print(formatted_datetime,'dte')
        #         context= {
        #             'application':ck.application,
        #             'proforma':ck.proforma,
        #             'desc_ann':ck.desc_ann,
        #             'typerecord_ann':ck.typerecord_ann,
        #             'drawings_ann':ck.drawings_ann,
        #             'css_qts_ann':ck.css_qts_ann,
        #             'dtac_ann':ck.dtac_ann,
        #             'sign':imgurl,
        #             'datenow':formatted_datetime
        #         }
        #         html = template.render(context)
        #         curr_path = "/"+str(idnew)+ "/Checklist"
        #         curr_path=curr_path.replace('/','\\')
        #         new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
        #         os.makedirs(new_path)
        #         result = open(new_path+"/Checklist.pdf", 'wb')
        #         pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result,link_callback=link_callback)
        #         result.close()
        #         ck.status="Approved by RCMA RD"
        #         ck.save()
        #         remove(imgurl)

        #     messages.success(request, 'Type Record with related documents are Approved !!')

    else:
        messages.warning(request, 'Wrong Password')

    pro=checklistmodel.objects.all()
    return render(request, 'rd/viewrecords.html',{'details':pro,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["RD"])
def rejected(request,id):
    pro=proforma_A_model.objects.all()
    return render(request, 'rd/viewrecords.html',{'details':pro,'status':True})


@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["Dealing Officer","TA Coordinator","RD","TCS-GD","TCS-CE","TCS-Dealing Officer","TCS-TA Coordinator"])
def comments(request):
    id=request.POST['id']
    comment=request.POST['comment']
    filename=request.POST['filename']
    print(id,filename,comment,'if')
    if filename=="TAapplication.pdf":
        tf=TAapplicationfiles.objects.filter(user_id=id,filecategory="TAapplication").first()
        tf.comments=comment
        tf.save()
    pro=proforma_A_model.objects.all()
    messages.success(request, 'Comments Successfully Submitted !')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["Dealing Officer","TA Coordinator","RD","TCS-GD","TCS-CE","TCS-Dealing Officer","TCS-TA Coordinator"])
def allcomments(request):
    id=request.POST['id']
    comment=request.POST['comment']
    filepath=request.POST['path']
    print(id,filepath,comment,'ifffffffff')
    tf=TAapplicationfiles.objects.filter(user_id=id,filepath=filepath).first()
    tf.comments=comment
    tf.save()
    # pro=proforma_A_model.objects.all()
    messages.success(request, 'Comments Successfully Submitted !')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["Dealing Officer","TA Coordinator","RD","TCS-GD"])
def viewtyperecordbyrd(request,id):
    print('saiiiiiiiiiiiiiii',id)
    # reg=get_object_or_404(registration,id=id)
    # taa=TAapplicationmodel.objects.filter(user_id=id).first()
    # if request.method == 'POST':
    #     return render(request, 'dealing officer/newtypeapproval.html', {'form': form,})
    # else:
    #     form = TAapplicationForm(instance=taa)
    #     template = get_template('applicant/newtypeapprovalpdf.html')
    #     context= {
    #         'firmname':taa.firmname,
    #         'addr1':taa.addr1,
    #         'addr2':taa.addr2,
    #         'tot':taa.tot,
    #         'item_name':taa.item_name,
    #         'part_no':taa.part_no,
    #         'desc':taa.desc,
    #         'spec': taa.spec,
    #         'dal_mdi':taa.dal_mdi,
    #         'bom':taa.bom,
    #         'sop_acbs':taa.sop_acbs,
    #         'pc': taa.pc,
    #         'tre':taa.tre,
    #         'otheritems':taa.otheritems
    #     }
    #     response = HttpResponse(content_type='application/pdf')
    #     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #     html = template.render(context)

    #     pisaStatus = pisa.CreatePDF(
    #     html, dest=response, link_callback=link_callback)
    #     if pisaStatus:
    #         return HttpResponse(response, content_type='application/pdf')
    # # if error then show some funy view
    #     if pisaStatus.err:
    #         return HttpResponse('We had some errors <pre>' + html + '</pre>')
    #     return response
    # return render(request, 'applicant/newtypeapprovalpdf.html', {'form': form,})

    # curr_path=curr_path.replace('/','\\')
    # new_path = os.path.join(settings.MEDIA_ROOT + curr_path)


    # with open(new_path+'TAapplication.pdf', 'rb') as pdf:
    #     response = HttpResponse(pdf.read(),content_type='application/pdf')
    #     response['Content-Disposition'] = 'filename=some_file.pdf'
    # return response
    print(id,'kkk')
    idprefix=request.POST['idprefix']
    filename=request.POST['filename']
    if filename!='':
        comment=request.POST['comment']
        if filename=="TAapplication.pdf":
            tf=TAapplicationfiles.objects.filter(user_id=id,filecategory="TAapplication").first()
            tf.comments=comment
            tf.save()
        pro=proforma_A_model.objects.all()
        messages.success(request, 'Comments Successfully Submitted !')  
    print(id,idprefix,'kkk')
    fc=TAapplicationmodel.objects.filter(user_id=id,idprefix=idprefix).first()
    print(fc.idprefix,'kkk')
    tafil=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory="TAapplication",refid=fc.idprefix).first()
    curr_path = "/"+str(fc.user_id)+"/"+fc.idprefix+"Annexure 1/TAapplication/"
    print(tafil,'tafile')
    filename='TAapplication.pdf'
    url='http://127.0.0.1:8000/media'+urllib.parse.quote(curr_path)+'TAapplication.pdf'
    print(tafil.comments,'new')
    return render(request, 'dealing officer/pdf viewer.html',{'url':url,'id':id,'filename':filename,'fc':tafil.comments,'idprefix':fc.idprefix})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["Dealing Officer","TA Coordinator","RD","TCS-GD","TCS-CE","TCS-Dealing Officer","TCS-TA Coordinator"])
def proformaviewbyrd(request,id):
    idprefix=request.POST['idprefix']
    fc=TAapplicationmodel.objects.filter(user_id=id,idprefix=idprefix).first()
    print(fc.idprefix,'kkk')
    # tafil=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory="TAapplication",refid=fc.idprefix).first()

    curr_path = "/"+str(fc.user_id)+ "/"+ fc.idprefix+"Annexure 3/Proforma_A/"
    curr_path=curr_path.replace('/','\\')
    new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
    if os.path.isdir(new_path):
        print('hhhhhhhh',new_path)
        with open(new_path+'Proforma_A.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = 'filename=some_file.pdf'
        return response
    else:
        print('sai',fc.user_id,fc.idprefix)
        form = proforma_A_form(request=fc.user_id,idpre=fc.idprefix)
        pro=proforma_A_model.objects.filter(user_id=fc.user_id,idprefix=idprefix).first()
        taa=TAapplicationmodel.objects.filter(user_id=fc.user_id,idprefix=idprefix).first()
        if pro:
            template = get_template('dealing officer/proformapdf.html')
            date_joined = datetime.now()
            formatted_datetime = date_joined.strftime("%Y-%m-%d")
            print(formatted_datetime,'dte')
            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='DAL_MDI',refid=fc.idprefix).first()
            dalurl=''
            if taf:
                aesurl=taf.filepath
                if taf.ext=='.pdf':
                    pdfurl = aesurl[:-4]
                    print('aesview',aesurl)
                    print('pdfview',pdfurl)
                    bufferSize = 64 * 1024
                    passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                    encFileSize = stat(aesurl).st_size
                    with open(aesurl, "rb") as fIn:
                        with open(pdfurl, "wb") as fOut:
                            pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                    pdfpath = pdfurl[25:]
                    print(pdfpath,'pppppppppp')
                    curr_path=pdfpath
                    dalurl='http://127.0.0.1:8000/media'+curr_path
                    print(dalurl,'pppp11111pppppp')
            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='BOM',refid=fc.idprefix).first()
            bomurl=''
            if taf:
                aesurl=taf.filepath
                if taf.ext=='.pdf':
                    pdfurl = aesurl[:-4]
                    print('aesview',aesurl)
                    print('pdfview',pdfurl)
                    bufferSize = 64 * 1024
                    passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                    encFileSize = stat(aesurl).st_size
                    with open(aesurl, "rb") as fIn:
                        with open(pdfurl, "wb") as fOut:
                            pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                    pdfpath = pdfurl[25:]
                    print(pdfpath,'pppppppppp')
                    curr_path=pdfpath
                    bomurl='http://127.0.0.1:8000/media'+curr_path
                    print(bomurl,'pppp11111pppppp')
            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='Tech_Spec',refid=fc.idprefix).first()
            techspecurl=''
            if taf:
                aesurl=taf.filepath
                if taf.ext=='.pdf':
                    pdfurl = aesurl[:-4]
                    print('aesview',aesurl)
                    print('pdfview',pdfurl)
                    bufferSize = 64 * 1024
                    passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                    encFileSize = stat(aesurl).st_size
                    with open(aesurl, "rb") as fIn:
                        with open(pdfurl, "wb") as fOut:
                            pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                    pdfpath = pdfurl[25:]
                    print(pdfpath,'pppppppppp')
                    curr_path=pdfpath
                    techspecurl='http://127.0.0.1:8000/media'+curr_path
                    print(techspecurl,'pppp11111pppppp')
                    
            context= {
                'firmname':taa.firmname,
                'addr1':taa.addr1,
                'addr2':taa.addr2,
                'item_name':taa.item_name,
                'part_no':taa.part_no,
                'desc':taa.desc,
                'dal_mdi':taa.dal_mdi,
                'bom':taa.bom,
                'sop_acbs':taa.sop_acbs,
                'pc': taa.pc,
                'tre':taa.tre,
                'otheritems':taa.otheritems,
                'dalurl':dalurl,
                'bomurl':bomurl,
                'techspecurl':techspecurl,

                
                'ta': pro.ta,
                'techspec': pro.techspec,
                'qts': pro.qts,
                'qtr': pro.qtr,
                'cd': pro.cd,
                'photo': pro.photo,
                'feedback': pro.feedback,
                'req': pro.req,
                'cost': pro.cost,
                'quantity': pro.quantity,
                'pc': pro.pc,
                'tacomments':pro.tacomments,
                'datenow':formatted_datetime
                
            }

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            html = template.render(context)

            pisaStatus = pisa.CreatePDF(
            html,dest=response,link_callback=link_callback)
            if pisaStatus:
                return HttpResponse(response,content_type='application/pdf')
        # if error then show some funy view
            if pisaStatus.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        else:
            print(form.errors)
            return render(request, 'dealing officer/proforma.html', {'form': form,'id':id})


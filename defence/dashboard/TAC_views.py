from django.shortcuts import render
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
from django.http import HttpResponse
from .views import link_callback
import os
import ast
import urllib
from datetime import datetime
from os import stat, remove
import pyAesCrypt
from io import BytesIO,StringIO
import comtypes.client
import pythoncom





@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Coordinator"])
def checklist(request):
    pro=proforma_A_model.objects.all()
    return render(request, 'ta coordinator/viewallchecklist.html',{'details':pro,'status':True})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Coordinator","RD","TCS-GD","TCS-CE","TCS-Dealing Officer","TCS-TA Coordinator"])
def newchecklist(request,id):
    idprefix=request.POST['idprefix']
    curr_path = "/"+str(id)+ "/"+ idprefix+ "/Annexure 1/Checklist/"
    curr_path=curr_path.replace('/','\\')
    new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
    print('sssssssssssssss',new_path)
    if os.path.isdir(new_path):
        print('ssssssssssssss11s',new_path)
        with open(new_path+'Checklist.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = 'filename=some_file.pdf'
        return response
    else:
        form = checklistForm()
        print('sai',id)
        ck=checklistmodel.objects.filter(user_id=str(id),idprefix=idprefix).first()
        if ck:
            template = get_template('ta coordinator/checklistpdf.html')
            # date_joined = datetime.now()
            # formatted_datetime = date_joined.strftime("%Y-%m-%d")
            # print(formatted_datetime,'dte')
            taf=TAapplicationfiles.objects.filter(user_id=str(id),filecategory='TAapplication',refid=idprefix).first()
            taappli = {}
            if taf:
                pdfurl=taf.filepath
                pdfpath = pdfurl[58:]
                tot='Enclosed at-'+taf.refpath+' '
                val='http://127.0.0.1:8000/media'+pdfpath
                # bomurl.append(val)
                taappli[tot] = val
                print(taappli,'pppp11111pppppp')
            else:
                taappli['No File Reference'] = ''

            taf=TAapplicationfiles.objects.filter(user_id=str(id),filecategory='Brief_Desc',refid=idprefix)
            dict_bd_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot_new='Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_bd_obj[tot_new] = val
                        print(dict_bd_obj,'pppp11111pppppp')
                    elif ta.ext=='docx':
                        nameonly=aesurl[:-8]
                        docurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('nameonly',nameonly)
                        print('docurl',docurl)
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
                        print(nameonly+'.pdf')
                        pdfurl=nameonly+'.pdf'
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot_new='Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_bd_obj[tot_new] = val
                        print(dict_bd_obj,'pppp11111pppppp')

            else:
                dict_bd_obj['No File Reference'] = ''

            taf=TAapplicationfiles.objects.filter(user_id=str(id),filecategory='Cont_TR',refid=idprefix)
            dict_tr_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot_new='Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_tr_obj[tot_new] = val
                        print(dict_tr_obj,'pppp11111pppppp')
            else:
                dict_tr_obj['No File Reference'] = ''
            
            taf=TAapplicationfiles.objects.filter(user_id=str(id),filecategory='Drawings',refid=idprefix)
            dict_dr_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot_new='Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_dr_obj[tot_new] = val
                        print(dict_dr_obj,'pppp11111pppppp')
            else:
                dict_dr_obj['No File Reference'] = ''

            taf=TAapplicationfiles.objects.filter(user_id=str(id),filecategory='TA_Data_Sheet',refid=idprefix)
            dict_ds_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot_new='Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_ds_obj[tot_new] = val
                        print(dict_ds_obj,'pppp11111pppppp')
            else:
                dict_ds_obj['No File Reference'] = ''
            context= {
                'dict_appli_obj':taappli,
                'proforma':ck.proforma,
                'dict_bd_obj':dict_bd_obj,
                'dict_tr_obj':dict_tr_obj,
                'dict_dr_obj':dict_dr_obj,
                'dict_ds_obj':dict_ds_obj,
                'dtac':ck.dtac,
            }

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            html = template.render(context)

            pisaStatus = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)
            if pisaStatus:
                return HttpResponse(response, content_type='application/pdf')
        # if error then show some funy view
            if pisaStatus.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        else:
            print(form.errors)
            return render(request, 'ta coordinator/newchecklist.html', {'form': form,'id':id,'idprefix':idprefix})

    # form = checklistForm()
    # return render(request, 'ta coordinator/newchecklist.html',{'form': form,})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Coordinator","RD","TCS-GD"])
def addchecklist(request):
    if request.POST:
        id=request.POST['id']
        idprefix=request.POST['idprefix']
        user=User.objects.get(pk=id)
        print(id,idprefix,'ddddddddddddd')
        form = checklistForm(request.POST)
        if form.is_valid():
            print(id,idprefix,'ddddddddddddd')
            ck= form.save(commit=False)
            ck.user = user
            ck.status="waiting for approval"
            ck.idprefix=idprefix
            ck.save()

            print("ready",ck.idprefix,id)

            taapp_form=TAapplicationmodel.objects.filter(user_id=id,idprefix=ck.idprefix).first()
            print("tac_form",taapp_form.id)

            get_taap_id=statusmodel.objects.filter(TAA_id=taapp_form.id).first()
            get_taap_id.status='Ready_for_Reco'
            get_taap_id.Ready_for_Reco=datetime.now()
            get_taap_id.save()
            print("status",get_taap_id)

            messages.success(request, 'Checklist Successfully Prepared !')
    return render(request, 'ta coordinator/newchecklist.html')

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Coordinator"])
def TAC_received(request):
    print(request.VG,'VGGGGG')
    do_usr=User.objects.filter(groups__name=request.VG+'-Dealing Officer').values('id','first_name').order_by('groups__name')
    print(do_usr,'dddddddddddddd')
    reg=TAapplicationmodel.objects.filter(rcma=request.VG,file_in_name__endswith="TAC")
    return render(request, 'ta coordinator/viewtyperecord.html',{'details':reg,'status':True,'do_usr':do_usr})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["TA Coordinator"])
def TAC_forward_do(request):
    id=request.POST['id']
    do_id=request.POST['user_detail']
    do_id1=ast.literal_eval(do_id)
    print(do_id1['id'],do_id1['first_name'],'taccccccccccc')
    reg_by_id=TAapplicationmodel.objects.filter(rcma=request.VG,file_in_name__endswith="TAC",user_id=id).first()
    reg_by_id.file_in_name=do_id1['first_name']
    reg_by_id.file_in_id=do_id1['id']
    reg_by_id.save()

    get_taap_id=statusmodel.objects.filter(TAA_id=reg_by_id.id).first()
    get_taap_id.status='Send_to_RCMA_DO'
    get_taap_id.Send_to_RCMA_DO=datetime.now()
    get_taap_id.save()


    do_usr=User.objects.filter(groups__name=request.VG+'-Dealing Officer').values('id','first_name')
    print(do_usr,'dddddddddddddd')
    reg=TAapplicationmodel.objects.filter(rcma=request.VG,file_in_name="TAC")
    return render(request, 'ta coordinator/viewtyperecord.html',{'details':reg,'status':True,'do_usr':do_usr})

@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["Dealing Officer","TA Coordinator","RD","TCS-GD"])
def viewtyperecordbytac(request,id):
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
@role_required(allowed_roles=["Dealing Officer","TA Coordinator","RD","TCS-GD"])
def proformaviewbytac(request,id):
    idprefix=request.POST['idprefix']
    fc=TAapplicationmodel.objects.filter(user_id=id,idprefix=idprefix).first()
    print(fc.idprefix,'kkk')
    # tafil=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory="TAapplication",refid=fc.idprefix).first()

    curr_path = "/"+str(fc.user_id)+ fc.idprefix+"Annexure 3/Proforma_A/"
    curr_path=curr_path.replace('/','\\')
    new_path = os.path.join(settings.MEDIA_ROOT + curr_path)
    if os.path.isdir(new_path):
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
            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='DAL_MDI',refid=fc.idprefix)
            dict_dal_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot='Ref.no:-'+ta.file_refno+', dt.-'+ta.refdate+', Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_dal_obj[tot] = val
                        print(dict_dal_obj,'pppp11111pppppp')
            else:
                dict_dal_obj['No File Reference'] = ''
            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='BOM',refid=fc.idprefix)
            dict_bom_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot='Ref.no:-'+ta.file_refno+', dt.-'+ta.refdate+', Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        # bomurl.append(val)
                        dict_bom_obj[tot] = val
                        print(dict_bom_obj,'pppp11111pppppp')
            else:
                dict_bom_obj['No File Reference'] = ''

            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='SOP_ACBS',refid=fc.idprefix)
            dict_sop_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot='Ref.no:-'+ta.file_refno+', dt.-'+ta.refdate+', Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        # bomurl.append(val)
                        dict_sop_obj[tot] = val
                        print(dict_sop_obj,'pppp11111pppppp')
            else:
                dict_sop_obj['No File Reference'] = ''

            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='TAapplication',refid=fc.idprefix).first()
            taappli = {}
            if taf:
                pdfurl=taf.filepath
                pdfpath = pdfurl[58:]
                tot='Enclosed at-'+taf.refpath+' '
                val='http://127.0.0.1:8000/media'+pdfpath
                # bomurl.append(val)
                taappli[tot] = val
                print(taappli,'pppp11111pppppp')
            else:
                taappli['No File Reference'] = ''
            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='Tech_Spec',refid=fc.idprefix)
            dict_tech_spec_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot='Ref.no:-'+ta.file_refno+', dt.-'+ta.refdate+', Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_tech_spec_obj[tot] = val
                        print(dict_tech_spec_obj,'pppp11111pppppp')
            else:
                dict_tech_spec_obj['No File Reference'] = ''

            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='QTS',refid=fc.idprefix)
            dict_qts_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot='Ref.no:-'+ta.file_refno+', dt.-'+ta.refdate+', Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_qts_obj[tot] = val
                        print(dict_qts_obj,'pppp11111pppppp')
            else:
                dict_qts_obj['No File Reference'] = ''

            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='QTR',refid=fc.idprefix)
            dict_qtr_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot='Ref.no:-'+ta.file_refno+', dt.-'+ta.refdate+', Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_qtr_obj[tot] = val
                        print(dict_qtr_obj,'pppp11111pppppp')
            else:
                dict_qtr_obj['No File Reference'] = ''

            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='COD',refid=fc.idprefix)
            dict_cod_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot='Ref.no:-'+ta.file_refno+', dt.-'+ta.refdate+', Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_cod_obj[tot] = val
                        print(dict_cod_obj,'pppp11111pppppp')
            else:
                dict_cod_obj['No File Reference'] = ''

            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='Cont_TR',refid=fc.idprefix)
            dict_cont_tr_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot='Ref.no:-'+ta.file_refno+', dt.-'+ta.refdate+', Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_cont_tr_obj[tot] = val
                        print(dict_cont_tr_obj,'pppp11111pppppp')
            else:
                dict_cont_tr_obj['No File Reference'] = ''

            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='PH',refid=fc.idprefix)
            dict_ph_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot='Ref.no:-'+ta.file_refno+', dt.-'+ta.refdate+', Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_ph_obj[tot] = val
                        print(dict_ph_obj,'pppp11111pppppp')
            else:
                dict_ph_obj['No File Reference'] = ''

            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='Per_Fb',refid=fc.idprefix)
            dict_per_fb_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot='Ref.no:-'+ta.file_refno+', dt.-'+ta.refdate+', Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_per_fb_obj[tot] = val
                        print(dict_per_fb_obj,'pppp11111pppppp')
            else:
                dict_per_fb_obj['No File Reference'] = ''

            taf=TAapplicationfiles.objects.filter(user_id=fc.user_id,filecategory='PC',refid=fc.idprefix)
            dict_pc_obj = {} 
            if taf:
                for ta in taf:
                    aesurl=ta.filepath
                    if ta.ext=='.pdf':
                        pdfurl = aesurl[:-4]
                        print('aesview',aesurl)
                        print('pdfview',pdfurl)
                        bufferSize = 64 * 1024
                        passw = "#EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
                        encFileSize = stat(aesurl).st_size
                        with open(aesurl, "rb") as fIn:
                            with open(pdfurl, "wb") as fOut:
                                pyAesCrypt.decryptStream(fIn, fOut, passw, bufferSize, encFileSize)
                        pdfpath = pdfurl[58:]
                        print(pdfpath,'pppppppppp')
                        tot='Ref.no:-'+ta.file_refno+', dt.-'+ta.refdate+', Enclosed at-'+ta.refpath+' '
                        curr_path=pdfpath
                        val='http://127.0.0.1:8000/media'+curr_path
                        dict_pc_obj[tot] = val
                        print(dict_pc_obj,'pppp11111pppppp')
            else:
                dict_pc_obj['No File Reference'] = ''
                    
            context= {
                'firmname':taa.firmname,
                'addr1':taa.addr1,
                'addr2':taa.addr2,
                'item_name':taa.item_name,
                'part_no':taa.part_no,
                'desc':taa.desc,
                'dal_mdi':taa.dal_mdi,
                'bom':taa.bom,
                'dict_sop_obj':dict_sop_obj,
                'pc': taa.pc,
                'dict_cont_tr_obj':dict_cont_tr_obj,
                'otheritems':taa.otheritems,
                'dict_dal_obj':dict_dal_obj,
                'dict_bom_obj':dict_bom_obj,
                'dict_tech_spec_obj':dict_tech_spec_obj,

                
                'ta': taappli,
                'techspec': pro.techspec,
                'dict_qts_obj': dict_qts_obj,
                'dict_qtr_obj': dict_qtr_obj,
                'dict_cod_obj': dict_cod_obj,
                'dict_ph_obj': dict_ph_obj,
                'dict_per_fb_obj':dict_per_fb_obj,
                'req': pro.req,
                'cost': pro.cost,
                'quantity': pro.quantity,
                'dict_pc_obj': dict_pc_obj,
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


@login_required(login_url=settings.LOGIN_URL)
@role_required(allowed_roles=["RD","TCS-GD"])
def re_assign_to(request):
    id=request.POST['id']
    do_id=request.POST['user_detail']
    do_id1=ast.literal_eval(do_id)
    print(do_id1['id'],do_id1['first_name'],'taccccccccccc')
    reg_by_id=TAapplicationmodel.objects.filter(rcma=request.VG,pk=id).first()
    reg_by_id.file_in_name=do_id1['first_name']
    reg_by_id.file_in_id=do_id1['id']
    reg_by_id.save()

    get_taap_id=statusmodel.objects.filter(TAA_id=reg_by_id.id).first()
    if do_id1['first_name'].endswith('TAC'):
        get_taap_id.status='Send_to_RCMA_TAC'
        get_taap_id.Send_to_TAC=datetime.now()
    else:
        get_taap_id.status='Send_to_RCMA_DO'
        get_taap_id.Send_to_RCMA_DO=datetime.now()

    get_taap_id.save()


    do_usr=User.objects.filter(groups__name=request.VG+'-Dealing Officer').values('id','first_name')
    print(do_usr,'dddddddddddddd')
    reg=TAapplicationmodel.objects.filter(rcma=request.VG,file_in_name="TAC")
    return render(request, 'ta coordinator/viewtyperecord.html',{'details':reg,'status':True,'do_usr':do_usr})

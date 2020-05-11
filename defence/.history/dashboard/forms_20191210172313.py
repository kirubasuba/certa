from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from authmgmt.models import registration
from .models import TAapplicationmodel,proforma_A_model,checklistmodel,idgenerationmodel,TAapplicationfiles
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

# class UserCreationForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#     role=forms.ModelChoiceField(queryset=Group.objects.all())

#     class Meta:
#         model = User
#         fields = ('first_name','last_name','email', 'username',)
#         # fields = ('email', 'username','is_appadmin','is_applicant','is_dealing_officer','is_TA_coordr','is_RD')

#     def __init__(self, *args, **kwargs):
        
#             if kwargs.get('instance'):
#                 super(UserCreationForm, self).__init__(*args, **kwargs)
#                 for visible in self.visible_fields():
#                     visible.field.widget.attrs['class'] = 'form-control form-control-user'
#                 initial = kwargs.setdefault('initial',{})
#                 if kwargs['instance'].Group.all():
#                     initial['role']=kwargs['instance'].Group.all()[0]
#                 else:
#                     initial['role']=None
#             forms.ModelForm.__init__(self, *args, **kwargs)
#             super(UserCreationForm, self).__init__(*args, **kwargs)
#             for visible in self.visible_fields():
#                 visible.field.widget.attrs['class'] = 'form-control form-control-user'



#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         role=self.cleaned_data.pop('role')
#         # user = super().save(commit=False)
#         user = super().save()
#         user.groups.set([role])
#         user.set_password(self.cleaned_data["password1"])
#         # if commit:
#         user.save()
#         return user

class UserCreationForm(forms.ModelForm):
    
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    # role=forms.ModelChoiceField(queryset=Group.objects.all())
    # role=forms.ModelChoiceField(queryset=Group.objects.all())
    # role=forms.ModelChoiceField(queryset=Group.objects.all())
    # password = forms.CharField(label='Password',widget=forms.PasswordInput)
    firmname = forms.CharField(label='Name of the Firm', widget=forms.TextInput(attrs={'cols': 80, 'rows': 2}))
    firmhead = forms.CharField(label='Head of the organisation', widget=forms.TextInput(attrs={'cols': 80, 'rows': 2}))
    email = forms.CharField(label='Email for future communication', widget=forms.TextInput(attrs={'cols': 80, 'rows': 2}))
    # addr = forms.CharField(label='D&D Firm Address', widget=forms.TextInput(attrs={'cols': 80, 'rows': 2}))
    remarks = forms.CharField(label='Remarks', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))

    class Meta:
        model = registration
        fields = ('firmname','firmhead','email', 'username','password','remarks')
        # fields = ('email', 'username','is_appadmin','is_applicant','is_dealing_officer','is_TA_coordr','is_RD')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            self.fields['firmname'].widget.attrs['readonly'] = True
            self.fields['firmhead'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['username'].widget.attrs['readonly'] = True
            # self.fields['password'].widget.attrs['readonly'] = True
            self.fields['password'].widget = forms.HiddenInput()
            # self.fields['addr'].widget.attrs['readonly'] = True
            self.fields['remarks'].widget.attrs['readonly'] = True

            # if kwargs.get('instance'):
            #     super(UserCreationForm, self).__init__(*args, **kwargs)
            #     for visible in self.visible_fields():
            #         visible.field.widget.attrs['class'] = 'form-control form-control-user'
            #     initial = kwargs.setdefault('initial',{})
            #     if kwargs['instance'].Group.all():
            #         initial['role']=kwargs['instance'].Group.all()[0]
            #     else:
            #         initial['role']=None
            # forms.ModelForm.__init__(self, *args, **kwargs)
            # super(UserCreationForm, self).__init__(*args, **kwargs)
            # for visible in self.visible_fields():
            #     visible.field.widget.attrs['class'] = 'form-control form-control-user'



    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     # role=self.cleaned_data.pop('role')
    #     # user = super().save(commit=False)
    #     user = user.save()
    #     # user.groups.set([role])
    #     user.set_password(self.cleaned_data["password"])
    #     # if commit:
    #     user.save()
    #     return user
class TAapplicationForm(forms.ModelForm):
    
    firmname = forms.CharField(label='Name of the Firm',widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    addr1 = forms.CharField(label='Address of Design and Development', widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    addr2 = forms.CharField(label='Address of Manufacturer / Production', widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    tot = forms.CharField(label='Details of ToT', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    item_name = forms.CharField(label='Nomenclature', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    part_no = forms.CharField(label='Part Number', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    desc = forms.CharField(label='Brief Description with intended use of the product(Not more than 50 words)', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    spec = forms.CharField(label='Governing specification of the item', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    dal_mdi= forms.CharField(label='DAL/MDI', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    # dal_mdi_file= forms.FileField(label='Attach files for DAL/MDI',widget=forms.FileInput(attrs={'multiple': True}))
    bom = forms.CharField(label='BOM', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    # bom_file = forms.FileField(label='Attach files for BOM',widget=forms.FileInput(attrs={'multiple': True}))
    sop_acbs = forms.CharField(label='SOP/ACBS', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    # sop_acbs_file = forms.FileField(label='Attach files for SOP/ACBS',widget=forms.FileInput(attrs={'multiple': True}))
    pc = forms.CharField(label='Details of the PCs issued', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    tre = forms.CharField(label='Type Record', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    otheritems = forms.CharField(label='Any other relevant information', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    sign = forms.FileField(label='Attach Authorized Signature',widget=forms.FileInput(attrs={'multiple': False}))
    designation = forms.CharField(label='Designation of Signing Authority', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    # date =  forms.CharField(widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
    addr = forms.CharField(label='Address', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))

    
    
    class Meta:
        model = TAapplicationmodel
        fields = ('firmname','addr1','addr2','tot','item_name', 'part_no','desc','spec','dal_mdi','bom','sop_acbs','pc','tre','otheritems')
        # fields = ('email', 'username','is_appadmin','is_applicant','is_dealing_officer','is_TA_coordr','is_RD')

    def __init__(self, *args, **kwargs):

        if kwargs.get('request'):
            self.user = kwargs.pop('request',User)
            self.idprefix = kwargs.pop('idpre')
            print(self.user.id,self.idprefix,'id')
            super(TAapplicationForm,self).__init__(*args,**kwargs)
            idg=idgenerationmodel.objects.filter(user_id=self.user.id,idprefix=self.idprefix).first()

            self.fields['firmname'].widget = forms.TextInput(attrs={'value':idg.firmname})
            self.fields['addr1'].widget = forms.TextInput(attrs={'value':idg.addr1})
            self.fields['addr2'].widget = forms.TextInput(attrs={'value':idg.addr2})
            self.fields['item_name'].widget = forms.TextInput(attrs={'value':idg.item_name})
            self.fields['part_no'].widget = forms.TextInput(attrs={'value':idg.part_no})
            self.fields['desc'].widget = forms.TextInput(attrs={'value':idg.desc})
            self.fields['otheritems'].widget = forms.TextInput(attrs={'value':idg.otheritems})

            taa=TAapplicationfiles.objects.filter(user_id=self.user.id,filecategory='TOT',refid=self.idprefix).order_by('refpath')
            if taa:
                tot1=''
                for t in taa:
                    print(t.file_refno)
                    tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                    tot1=tot1+tot
                    print(tot,'update')
                self.fields['tot'].initial  = tot
            else:
                self.fields['tot'].widget = forms.TextInput(attrs={'value':'No File Reference'})

            taa=TAapplicationfiles.objects.filter(user_id=self.user.id,filecategory='Tech_Spec',refid=self.idprefix).order_by('refpath')
            if taa:
                tot1=''
                for t in taa:
                    print(t.file_refno)
                    tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                    tot1=tot1+tot
                    print(tot,'update')
                self.fields['spec'].initial  = tot
            else:
                self.fields['spec'].widget = forms.TextInput(attrs={'value':'No File Reference'})

            taa=TAapplicationfiles.objects.filter(user_id=self.user.id,filecategory='DAL_MDI',refid=self.idprefix).order_by('refpath')
            if taa:
                tot1=''
                for t in taa:
                    print(t.file_refno)
                    tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                    tot1=tot1+tot
                    print(tot,'update')
                self.fields['dal_mdi'].initial  = tot
            else:
                self.fields['dal_mdi'].widget = forms.TextInput(attrs={'value':'No File Reference'})

            taa=TAapplicationfiles.objects.filter(user_id=self.user.id,filecategory='BOM',refid=self.idprefix).order_by('refpath')
            if taa:
                tot1=''
                for t in taa:
                    print(t.file_refno)
                    tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                    tot1=tot1+tot
                    print(tot,'update')
                self.fields['bom'].initial  = tot1
            else:
                self.fields['bom'].widget = forms.TextInput(attrs={'value':'No File Reference'})

            taa=TAapplicationfiles.objects.filter(user_id=self.user.id,filecategory='SOP_ACBS',refid=self.idprefix).order_by('refpath')
            if taa:
                tot1=''
                for t in taa:
                    print(t.file_refno)
                    tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                    tot1=tot1+tot
                    print(tot,'update')
                self.fields['sop_acbs'].initial  = tot
            else:
                self.fields['sop_acbs'].widget = forms.TextInput(attrs={'value':'No File Reference'})

            taa=TAapplicationfiles.objects.filter(user_id=self.user.id,filecategory='PC',refid=self.idprefix).order_by('refpath')
            if taa:
                tot1=''
                for t in taa:
                    print(t.file_refno)
                    tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                    tot1=tot1+tot
                    print(tot,'update')
                self.fields['pc'].initial  = tot
            else:
                self.fields['pc'].widget = forms.TextInput(attrs={'value':'No File Reference'})

            taa=TAapplicationfiles.objects.filter(user_id=self.user.id,filecategory='Cont_TR',refid=self.idprefix).order_by('refpath')
            if taa:
                tot1=''
                for t in taa:
                    print(t.file_refno)
                    tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                    tot1=tot1+tot
                    print(tot,'update')
                self.fields['tre'].initial  = tot
            else:
                self.fields['tre'].widget = forms.TextInput(attrs={'value':'No File Reference'})

            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control form-control-user'
                self.fields['firmname'].widget.attrs['readonly'] = True
                self.fields['addr1'].widget.attrs['readonly'] = True
                self.fields['addr2'].widget.attrs['readonly'] = True
                self.fields['item_name'].widget.attrs['readonly'] = True
                self.fields['part_no'].widget.attrs['readonly'] = True
                self.fields['desc'].widget.attrs['readonly'] = True
                self.fields['otheritems'].widget.attrs['readonly'] = True
                self.fields['tot'].widget.attrs['readonly'] = True
                self.fields['spec'].widget.attrs['readonly'] = True
                self.fields['dal_mdi'].widget.attrs['readonly'] = True
                self.fields['bom'].widget.attrs['readonly'] = True
                self.fields['sop_acbs'].widget.attrs['readonly'] = True
                self.fields['pc'].widget.attrs['readonly'] = True
                self.fields['tre'].widget.attrs['readonly'] = True

        else:
            super(TAapplicationForm,self).__init__(*args,**kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control form-control-user'
                self.fields['firmname'].widget.attrs['readonly'] = True

      
class cemilacUserForm(forms.ModelForm):
    

    maingroup= [
    ('RCMA', 'RCMA'),
    ('TCS', 'TCS')
    ]

    vg= [
    ('---', '---'),
    ('AIR', 'Aircraft'),
    ('HEL', 'Helicopter'),
    ('MAT', 'Materials'),
    ('MSL', 'Missiles'),
    ('AAP', 'Air Armament'),
    ('LKN', 'Lucknow'),
    ('KPT', 'Koraput'),
    ('ENG', 'Engines'),
    ('FFF', 'F&F-FOL'),
    ('HYD', 'Hyderabad'),
    ('NSK', 'Nasik'),
    ('KNP', 'Kanpur'),
    ('KOR', 'Korwa'),
    ('CHD', 'Chandigarh'),
    ]

    mainrole= [
    ('CE', 'CE'),
    ('GD', 'GD'),
    ('RD', 'RD'),
    ('TA Coordinator', 'TA Coordinator'),
    ('Dealing Officer', 'Dealing Officer'),
    ]



    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    # role=forms.ModelChoiceField(queryset=Group.objects.all())
    maingroups= forms.CharField(label='Group', widget=forms.Select(choices=maingroup))
    vg= forms.CharField(label='VG', widget=forms.Select(choices=vg))
    mainroles= forms.CharField(label='Role', widget=forms.Select(choices=mainrole))


    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password','maingroups','vg','mainroles')
        # fields = ('email', 'username','is_appadmin','is_applicant','is_dealing_officer','is_TA_coordr','is_RD')

    def __init__(self, *args, **kwargs):
        super(cemilacUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'

    # def save(self, commit=True):
    #     role=self.cleaned_data.pop('role')
    #     user = super().save()
    #     user.groups.set([role])
    #     user.set_password(self.cleaned_data["password"])
    #     user.save()
    #     return user


class proforma_A_form(forms.ModelForm):

    desc = forms.CharField(label='Brief Description of the product with end use of the application(Not more than 50 words)', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    item_name = forms.CharField(label='Nomenclature', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    part_no = forms.CharField(label='Part Number', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    dal_mdi = forms.CharField(label='DAL/MDI', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    bom = forms.CharField(label='BOM', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    sop_acbs = forms.CharField(label='SOP/ACBS', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    otheritems = forms.CharField(label='Any other relevant information', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    firmname = forms.CharField(label='Name of the Firm')
    addr1 = forms.CharField(label='Design and Development', widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    addr2 = forms.CharField(label='Manufacturer / Production', widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    ta = forms.CharField(label='Application of TA by Design and Developing agency(IPR holder for the product)', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    techspec = forms.CharField(label='Technical specification of the document reference with date', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    qts = forms.CharField(label='Qualification Test schedule document reference with date ', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    qtr = forms.CharField(label='Qualification Test Result document reference with date', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    cd = forms.CharField(label='Certificate of Design', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    tre = forms.CharField(label='Type Record', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    photo = forms.CharField(label='Color photograph 3 different views', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    feedback = forms.CharField(label='User Performance feedback,if available(from DGAQA/DPSU/User Services)', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    req = forms.CharField(label='Annual requirement of the product', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    cost = forms.CharField(label='Cost of the product per unit in rupees', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    quantity = forms.CharField(label='Quantity produced till date', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    pc = forms.CharField(label='Details of the PCs issued and subsequent renewals', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    tacomments = forms.CharField(label='Recommendations for Type Approval with comments and observation,if any', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    
    class Meta:
        model = proforma_A_model
        fields = ('desc','item_name', 'part_no','dal_mdi','bom','sop_acbs','otheritems','firmname','addr1','addr2','ta','techspec','qts','qtr','cd','tre','photo','feedback','req','cost','quantity','pc','tacomments')
        # fields = ('email', 'username','is_appadmin','is_applicant','is_dealing_officer','is_TA_coordr','is_RD')

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('request')
        self.idprefix = kwargs.pop('idpre')
        print(self.id,self.idprefix,'lllllllllllllllllll')
        super(proforma_A_form,self).__init__(*args,**kwargs)
        taa=TAapplicationmodel.objects.filter(user_id=self.id,idprefix=self.idprefix).first()
        self.fields['firmname'].widget = forms.TextInput(attrs={'value':taa.firmname})
        self.fields['addr1'].widget = forms.TextInput(attrs={'value':taa.addr1})
        self.fields['addr2'].widget = forms.TextInput(attrs={'value':taa.addr2})
        self.fields['item_name'].widget = forms.TextInput(attrs={'value':taa.item_name})
        self.fields['part_no'].widget = forms.TextInput(attrs={'value':taa.part_no})
        self.fields['desc'].widget = forms.TextInput(attrs={'value':taa.desc})
        self.fields['otheritems'].widget = forms.TextInput(attrs={'value':taa.otheritems})

        taa=TAapplicationfiles.objects.filter(user_id=self.id,filecategory='Tech_Spec',refid=self.idprefix).order_by('refpath')
        if taa:
            tot1=''
            for t in taa:
                print(t.file_refno)
                tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                tot1=tot1+tot
                print(tot,'update')
            self.fields['techspec'].initial  = tot
        else:
            self.fields['techspec'].widget = forms.TextInput(attrs={'value':'No File Reference'})

        taa=TAapplicationfiles.objects.filter(user_id=self.id,filecategory='DAL_MDI',refid=self.idprefix).order_by('refpath')
        if taa:
            tot1=''
            for t in taa:
                print(t.file_refno)
                tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                tot1=tot1+tot
                print(tot,'update')
            self.fields['dal_mdi'].initial  = tot
        else:
            self.fields['dal_mdi'].widget = forms.TextInput(attrs={'value':'No File Reference'})

        taa=TAapplicationfiles.objects.filter(user_id=self.id,filecategory='BOM',refid=self.idprefix).order_by('refpath')
        if taa:
            tot1=''
            for t in taa:
                print(t.file_refno)
                tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                tot1=tot1+tot
                print(tot,'update')
            self.fields['bom'].initial  = tot1
        else:
            self.fields['bom'].widget = forms.TextInput(attrs={'value':'No File Reference'})

        taa=TAapplicationfiles.objects.filter(user_id=self.id,filecategory='SOP_ACBS',refid=self.idprefix).order_by('refpath')
        if taa:
            tot1=''
            for t in taa:
                print(t.file_refno)
                tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                tot1=tot1+tot
                print(tot,'update')
            self.fields['sop_acbs'].initial  = tot
        else:
            self.fields['sop_acbs'].widget = forms.TextInput(attrs={'value':'No File Reference'})

        taa=TAapplicationfiles.objects.filter(user_id=self.id,filecategory='PC',refid=self.idprefix).order_by('refpath')
        if taa:
            tot1=''
            for t in taa:
                print(t.file_refno)
                tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                tot1=tot1+tot
                print(tot,'update')
            self.fields['pc'].initial  = tot
        else:
            self.fields['pc'].widget = forms.TextInput(attrs={'value':'No File Reference'})

        taa=TAapplicationfiles.objects.filter(user_id=self.id,filecategory='Cont_TR',refid=self.idprefix).order_by('refpath')
        if taa:
            tot1=''
            for t in taa:
                print(t.file_refno)
                tot='Ref.no:-'+t.file_refno+', dt.-'+t.refdate+', Enclosed at-'+t.refpath+' '
                tot1=tot1+tot
                print(tot,'update')
            self.fields['tre'].initial  = tot
        else:
            self.fields['tre'].widget = forms.TextInput(attrs={'value':'No File Reference'})
        
        taa=TAapplicationfiles.objects.filter(user_id=self.id,filecategory='TAapplication',refid=self.idprefix).order_by('refpath')
        if taa:
            tot1=''
            for t in taa:
                # print(t.file_refno)
                tot= 'Enclosed at-'+t.refpath
                tot1=tot1+tot
                print(tot,'update')
            self.fields['ta'].initial  = tot
        else:
            self.fields['ta'].widget = forms.TextInput(attrs={'value':'No File Reference'})

        taa=TAapplicationfiles.objects.filter(user_id=self.id,filecategory='QTS',refid=self.idprefix).order_by('refpath')
        if taa:
            tot1=''
            for t in taa:
                # print(t.file_refno)
                tot= 'Enclosed at-'+t.refpath
                tot1=tot1+tot
                print(tot,'update')
            self.fields['qts'].initial  = tot
        else:
            self.fields['qts'].widget = forms.TextInput(attrs={'value':'No File Reference'})

        taa=TAapplicationfiles.objects.filter(user_id=self.id,filecategory='QTR',refid=self.idprefix).order_by('refpath')
        if taa:
            tot1=''
            for t in taa:
                # print(t.file_refno)
                tot= 'Enclosed at-'+t.refpath
                tot1=tot1+tot
                print(tot,'update')
            self.fields['qtr'].initial  = tot
        else:
            self.fields['qtr'].widget = forms.TextInput(attrs={'value':'No File Reference'})

        taa=TAapplicationfiles.objects.filter(user_id=self.id,filecategory='COD',refid=self.idprefix).order_by('refpath')
        if taa:
            tot1=''
            for t in taa:
                # print(t.file_refno)
                tot= 'Enclosed at-'+t.refpath
                tot1=tot1+tot
                print(tot,'update')
            self.fields['cd'].initial  = tot
        else:
            self.fields['cd'].widget = forms.TextInput(attrs={'value':'No File Reference'})
            
        taa=TAapplicationfiles.objects.filter(user_id=self.id,filecategory='Per_Fb',refid=self.idprefix).order_by('refpath')
        if taa:
            tot1=''
            for t in taa:
                # print(t.file_refno)
                tot= 'Enclosed at-'+t.refpath
                tot1=tot1+tot
                print(tot,'update')
            self.fields['feedback'].initial  = tot
        else:
            self.fields['feedback'].widget = forms.TextInput(attrs={'value':'No File Reference'})
        
        taa=TAapplicationfiles.objects.filter(user_id=self.id,filecategory='PH',refid=self.idprefix).order_by('refpath')
        if taa:
            tot1=''
            for t in taa:
                # print(t.file_refno)
                tot= 'Enclosed at-'+t.refpath
                tot1=tot1+tot
                print(tot,'update')
            self.fields['photo'].initial  = tot
        else:
            self.fields['photo'].widget = forms.TextInput(attrs={'value':'No File Reference'})
        


        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            self.fields['firmname'].widget.attrs['readonly'] = True
            self.fields['addr1'].widget.attrs['readonly'] = True
            self.fields['addr2'].widget.attrs['readonly'] = True
            self.fields['item_name'].widget.attrs['readonly'] = True
            self.fields['part_no'].widget.attrs['readonly'] = True
            self.fields['desc'].widget.attrs['readonly'] = True
            self.fields['otheritems'].widget.attrs['readonly'] = True
            self.fields['techspec'].widget.attrs['readonly'] = True
            self.fields['dal_mdi'].widget.attrs['readonly'] = True
            self.fields['bom'].widget.attrs['readonly'] = True
            self.fields['sop_acbs'].widget.attrs['readonly'] = True
            self.fields['pc'].widget.attrs['readonly'] = True
            self.fields['tre'].widget.attrs['readonly'] = True
            self.fields['ta'].widget.attrs['readonly'] = True
            self.fields['qts'].widget.attrs['readonly'] = True
            self.fields['qtr'].widget.attrs['readonly'] = True
            self.fields['cd'].widget.attrs['readonly'] = True
            self.fields['feedback'].widget.attrs['readonly'] = True
            self.fields['photo'].widget.attrs['readonly'] = True

class checklistForm(forms.ModelForm):
    
    application = forms.CharField(label='Application for the type approval by D&D agency,duly recommemded by RD,RCMA',widget=forms.Textarea(attrs={'cols': 80, 'rows': 1}))
    desc = forms.CharField(label='Brief Description of the item and end use/application of the item',widget=forms.FileInput(attrs={'multiple': True}))
    proforma = forms.CharField(label='Proforma A for fresh type approval', widget=forms.Textarea(attrs={'cols': 80, 'rows': 1}))
    # desc_ann = forms.CharField(label='Annexure Number', widget=forms.Textarea(attrs={'cols': 80, 'rows': 1}))
    typerecord = forms.CharField(label='Type record duly vetted by D&D and RCMA',widget=forms.FileInput(attrs={'multiple': True}))
    # typerecord_ann = forms.CharField(label='Annexure Number', widget=forms.Textarea(attrs={'cols': 80, 'rows': 1}))
    drawings = forms.CharField(label='Drawings(including one in type record) provisionally approved by RCMA',widget=forms.FileInput(attrs={'multiple': True}))
    # drawings_ann = forms.CharField(label='Annexure Number', widget=forms.Textarea(attrs={'cols': 80, 'rows': 1}))
    css_qts = forms.CharField(label='Compliance statement to the specification and Qualification Test Schedule and hard copy authenticated by RD,RCMA',widget=forms.FileInput(attrs={'multiple': True}))
    # css_qts_ann = forms.CharField(label='Annexure Number', widget=forms.Textarea(attrs={'cols': 80, 'rows': 1}))
    dtac = forms.CharField(label='Draft type approval certificate and hard copy authenticated by RD,RCMA',widget=forms.FileInput(attrs={'multiple': True}))
    # dtac_ann = forms.CharField(label='Annexure Number', widget=forms.Textarea(attrs={'cols': 80, 'rows': 1}))
    

    class Meta:
        model = checklistmodel
        fields = ('application','desc','proforma','typerecord','drawings','css_qts','dtac')

    def __init__(self, *args, **kwargs):

        super(checklistForm,self).__init__(*args,**kwargs)
        self.fields['application'].widget = forms.TextInput(attrs={'value':'Enclosed at Annexure-1'})
        self.fields['desc'].widget = forms.TextInput(attrs={'value':'Enclosed at Annexure-2'})
        self.fields['proforma'].widget = forms.TextInput(attrs={'value':'Enclosed at Annexure-3'})
        self.fields['typerecord'].widget = forms.TextInput(attrs={'value':'Enclosed at Annexure-4'})
        self.fields['drawings'].widget = forms.TextInput(attrs={'value':'Enclosed at Annexure-5'})
        self.fields['css_qts'].widget = forms.TextInput(attrs={'value':'Enclosed at Annexure-6'})
        self.fields['dtac'].widget = forms.TextInput(attrs={'value':'Enclosed at Annexure-7'})
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            self.fields['application'].widget.attrs['readonly'] = True
            self.fields['desc'].widget.attrs['readonly'] = True
            self.fields['proforma'].widget.attrs['readonly'] = True
            self.fields['typerecord'].widget.attrs['readonly'] = True
            self.fields['drawings'].widget.attrs['readonly'] = True
            self.fields['css_qts'].widget.attrs['readonly'] = True
            self.fields['dtac'].widget.attrs['readonly'] = True


class IDGenerationForm(forms.ModelForm):
    
    vg= [
    ('---', '---'),
    ('AIR', 'Aircraft'),
    ('HEL', 'Helicopter'),
    ('MAT', 'Materials'),
    ('MSL', 'Missiles'),
    ('AAP', 'Air Armament'),
    ('LKN', 'Lucknow'),
    ('KPT', 'Koraput'),
    ('ENG', 'Engines'),
    ('FFF', 'F&F-FOL'),
    ('HYD', 'Hyderabad'),
    ('NSK', 'Nasik'),
    ('KNP', 'Kanpur'),
    ('KOR', 'Korwa'),
    ('CHD', 'Chandigarh'),
    ]
    sfirmname = forms.CharField(label='Short form of D&D Firm Name', widget=forms.TextInput(attrs={'cols': 80, 'rows': 2,'placeholder':'D&D Firm Name(4 Characters Only)'}))
    sprodname = forms.CharField(label='Short form of the Product Name', widget=forms.TextInput(attrs={'cols': 80, 'rows': 2,'placeholder':'Product Name(4 Characters Only)'}))
    rcma= forms.CharField(label='Choose RCMA', widget=forms.Select(choices=vg))
    firmname = forms.CharField(label='Name of the Firm',widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    addr1 = forms.CharField(label='Address of Design and Development', widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    addr2 = forms.CharField(label='Address of Manufacturer / Production', widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    item_name = forms.CharField(label='Nomenclature', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    part_no = forms.CharField(label='Part Number', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    desc = forms.CharField(label='Brief Description with intended use of the product(Not more than 50 words)', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    otheritems = forms.CharField(label='Any other relevant information', widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    class Meta:
        model = idgenerationmodel
        fields = ('sfirmname','sprodname','rcma','firmname','addr1','addr2','item_name','part_no','desc','otheritems')

    def __init__(self, *args, **kwargs):

        if kwargs.get('request'):
            self.user = kwargs.pop('request',User)
            print(self.user.id,'id')
            super(IDGenerationForm,self).__init__(*args,**kwargs)
            self.fields['firmname'].widget = forms.TextInput(attrs={'value':self.user.first_name})
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control form-control-user'
                self.fields['firmname'].widget.attrs['readonly'] = True

        else:
            super(IDGenerationForm,self).__init__(*args,**kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control form-control-user'
                self.fields['firmname'].widget.attrs['readonly'] = True

class fileUploadForm(forms.ModelForm):
    
    ft= [
    ('', 'Choose TR Annexure Type'),
    ('TOT', 'Annexure 1.1 - TOT'),
    ('Brief_Desc', 'Annexure 2 - Brief Description'),
    ('Cont_TR', 'Annexure 4 - Contents of Type Record'),
    ('PH', 'Annexure 4.1 - Photographs'),
    ('Tech_Spec', 'Annexure 4.2 - Technical Specification'),
    ('DAL_MDI', 'Annexure 4.3 - DAL_MDI'),
    ('BOM', 'Annexure 4.4 - BOM'),
    ('SOP_ACBS', 'Annexure 4.5 - SOP_ACBS'),
    ('Pro_Doc', 'Annexure 4.6 - Process Document'),
    ('QTS', 'Annexure 4.7 - QTS and Test Procedure'),
    ('QTR', 'Annexure 4.8 - QTR'),
    ('Comp_TR', 'Annexure 4.9 - Complience of Test Result'),
    ('COD', 'Annexure 4.10 - COD'),
    ('FER', 'Annexure 4.11 - Flight Evaluation Report'),
    ('Per_Fb', 'Annexure 4.12 - Performance Feedback'),
    ('PC', 'Annexure 4.13 - PC'),
    ('Drawings', 'Annexure 5 - Drawings'),
    ('TA_Data_Sheet', 'Annexure 6 - Type Approval Data Sheet'),
    ]

    filecategory= forms.CharField(label='Choose TR Annexure Type', widget=forms.Select(choices=ft))
    files = forms.FileField(label='Choose File',widget=forms.FileInput(attrs={'multiple': False}))
    file_refno = forms.CharField(label='Ref No.', widget=forms.TextInput(attrs={'cols': 80, 'rows': 2,'placeholder':'Ref.No.'}))
    refdate =  forms.CharField(label='Ref Date', widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))

    
    class Meta:
        model = TAapplicationfiles
        fields = ('filecategory','files','file_refno','refdate')

    def __init__(self, *args, **kwargs):

        super(fileUploadForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'

class commentsUploadForm(forms.ModelForm):

    ft= [
    ('', 'Choose responsible for this anexture'),
    ('HEL-DO', 'HEL-Dealing Officer'),
    ('HEL-TAC','HEL-TA Coordinator'),
    ('HEL-RD', 'HEL-RD'),
    ('AIR-DO', 'AIR-Dealing Officer'),
    ('AIR-TAC','AIR-TA Coordinator'),
    ('AIR-RD', 'AIR-RD'),
    ]

    status= [
    ('', 'Underprocess'),
    ('Closed', 'Closed'),
    ('Rework','Rework'),
    ('Underprocess', 'Underprocess'),
   
    ]


    name = forms.CharField(label='Anexture name', widget=forms.TextInput(attrs={'cols': 80, 'rows': 2,'placeholder':'Anexture name'}))
    comments = forms.CharField(label='comments',widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    responsible= forms.CharField(label='Choose responsible for this anexture', widget=forms.Select(choices=ft))
    action_taken = forms.CharField(label='action_taken', widget=forms.TextInput(attrs={'cols': 80, 'rows': 2,'placeholder':'action_taken'}))
    status= forms.CharField(label='status for this anexture', widget=forms.Select(choices=status))

    class Meta:
        model = commentsmodel
        fields = ('name','comments','responsible','action_taken','status')

    def __init__(self, *args, **kwargs):

        super(fileUploadForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
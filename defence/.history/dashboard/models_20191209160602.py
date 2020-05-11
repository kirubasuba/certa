from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import User,Group

# Create your models here.
# class MyUserManager(BaseUserManager):
#     def create_user(self, email,username,password=None):
#         """
#         Creates and saves a User with the given email, roleid ,username and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email,username,password):
#         """
#         Creates and saves a superuser with the given email, roleid,username and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             username=username,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

#     objects = MyUserManager()

#     # USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin

Group.add_to_class('VG', models.CharField(max_length=180,null=True, blank=True))
Group.add_to_class('rol', models.CharField(max_length=180,null=True, blank=True))

class TAapplicationmodel(models.Model):

    firmname=models.TextField()
    addr1=models.TextField()
    addr2=models.TextField()
    tot=models.TextField()
    item_name=models.TextField()
    part_no=models.TextField()
    desc=models.TextField()
    spec=models.TextField()
    dal_mdi=models.TextField()
    bom=models.TextField()
    sop_acbs = models.TextField()
    pc=models.TextField()
    tre=models.TextField()
    otheritems=models.TextField()
    file_in_id=models.TextField()
    file_in_name=models.TextField()
    rcma=models.TextField()
    idprefix=models.TextField()
    submitted_date=models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class TAapplicationfiles(models.Model):
    filecategory=models.TextField()
    filepath=models.TextField()
    ext=models.TextField()
    comments=models.TextField()
    refid=models.TextField()
    refpath=models.TextField()
    file_refno=models.TextField()
    refdate=models.TextField()
    relation=models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class proforma_A_model(models.Model):

    ta=models.TextField()
    techspec=models.TextField()
    qts=models.TextField()
    qtr=models.TextField()
    photo=models.TextField()
    feedback=models.TextField()
    cd=models.TextField()
    req=models.TextField()
    cost=models.TextField()
    quantity=models.TextField()
    pc=models.TextField()
    tacomments=models.TextField()
    idprefix=models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class checklistmodel(models.Model):

    application=models.TextField()
    proforma=models.TextField()
    desc=models.TextField()
    typerecord=models.TextField()
    drawings=models.TextField()
    css_qts=models.TextField()
    dtac=models.TextField()
    status=models.TextField()
    idprefix=models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class idgenerationmodel(models.Model):

    sfirmname=models.TextField()
    sprodname=models.TextField()
    rcma=models.TextField()
    idprefix=models.TextField(unique=True)

    firmname=models.TextField()
    addr1=models.TextField()
    addr2=models.TextField()
    item_name=models.TextField()
    part_no=models.TextField()
    desc=models.TextField()
    otheritems=models.TextField()
    registered_date=models.TextField()
    submitted_date=models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class statusmodel(models.Model):

    TAA_id=models.IntegerField()
    RCMA=models.TextField()
    status=models.TextField()
    RCMA_RD_Received=models.TextField()
    Send_to_RCMA_TAC=models.TextField()
    Send_to_RCMA_DO=models.TextField()
    Ready_for_CL=models.TextField()   
    Ready_for_Reco=models.TextField()
    Recommended=models.TextField()
    Send_to_TCS_GD=models.TextField()
    Send_to_TCS_TAC=models.TextField()
    Send_to_TCS_DO=models.TextField()
    Draft_TA=models.TextField()
    Forward_to_GD=models.TextField()
    Forward_to_CE=models.TextField()
    Issued_TA=models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class commentsmodel(models.Model):

    name=models.TextField()
    comments=models.TextField()
    commented_date=models.TextField()
    commented_by=models.TextField()
    responsible=models.TextField()
    action_taken=models.TextField()
    action_taken_by=models.TextField()
    idprefix=models.TextField()
    status=models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
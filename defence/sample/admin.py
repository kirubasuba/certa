from django.contrib import admin
from .models import app,registration,User
from django.contrib.auth.admin import UserAdmin
from django.db import models


# class UserClass(UserAdmin):
#     email = models.EmailField(verbose_name="email", max_length=60, unique=True)
#     username = models.CharField(max_length=30, unique=True)
#     # date_joined = models.DateTimeField(verbose_name='date joined')
#     # last_login = models.DateTimeField(verbose_name='last login')
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     role_id=models.IntegerField(default=1)

#     # is_admin = models.BooleanField(default=False)
#     # is_applicant = models.BooleanField(default=False)
#     # is_dealing_officer = models.BooleanField(default=False)
#     # is_TA_coordr = models.BooleanField(default=False)
#     # is_RD = models.BooleanField(default=False)
#     # is_group_dealing_officer = models.BooleanField(default=False)
#     # is_GD = models.BooleanField(default=False)
#     # is_TCS_dealing_officer = models.BooleanField(default=False)
#     # is_TCS_over_sight_officer = models.BooleanField(default=False)
#     # is_TCS_GD = models.BooleanField(default=False)
#     # is_Hindi_cell = models.BooleanField(default=False)
#     # is_CE = models.BooleanField(default=False)
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
    
#     def __str__(self):
#         return self.email
#         # For checking permissions. to keep it simple all admin have ALL permissons
#     def has_perm(self, perm, obj=None):
#         return self.is_active
        
#         # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
#     def has_module_perms(self, app_label):
#         return True

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username','is_appadmin','is_applicant','is_dealing_officer','is_TA_coordr','is_RD')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password','username','is_appadmin','is_applicant','is_dealing_officer','is_TA_coordr','is_RD','is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username','is_applicant','password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

# admin.site.register(User, UserClass)
admin.site.register(registration)
admin.site.register(app)
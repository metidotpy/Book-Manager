from typing import Set
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from crispy_forms.helper import FormHelper

# registration user form
class UserForm(UserCreationForm):
    # change first_name Field
    first_name = forms.CharField(max_length = 60, required=True, help_text = 'First Name')
    # change last_name field
    last_name = forms.CharField(max_length = 60, required=True, help_text='Last Name')
    # change username field
    username = forms.CharField(max_length = 150, required=True, help_text="Username")
    # change email field
    email = forms.EmailField(max_length = 254,required=True , help_text = 'Email')

    # turnoff auto compelete from username
    username.widget.attrs.update(
        autocomplete="off"
    )

    # meta class
    class Meta:
        # our model
        model = User
        # our fields
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'avatar','password1', 'password2']
    avatar = forms.ImageField(label=None ,widget=forms.FileInput(attrs={'disabled':True}))
# update user form
class UserFormEdit(forms.ModelForm):
    # meta class
    class Meta:
        # our model
        model = User
        # our fields
        fields = ['username', 'first_name', 'last_name', 'avatar']
    
    # make disabled some fields
    username = forms.CharField(widget=forms.TextInput(attrs={'disabled':True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'disabled':True}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'disabled':True}))
    avatar = forms.ImageField(label=None ,widget=forms.FileInput(attrs={'disabled':True}))

# update user form
class UserFormEditAccess(forms.ModelForm):
    # meta class
    class Meta:
        # our model
        model = User
        # our fields
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'avatar','is_superuser', 'is_access', 'is_active', 'is_staff']
    # make disabled some fields
    username = forms.CharField(widget=forms.TextInput(attrs={'disabled':True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'disabled':True}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'disabled':True}))
    email = forms.CharField(widget=forms.TextInput(attrs={'disabled':True}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'disabled':True}))
    avatar = forms.ImageField(label=None ,widget=forms.FileInput(attrs={'disabled':True}))

# registration user in admin panel for superusers
class UserFormAccess(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserFormAccess, self).__init__(*args, **kwargs)
    # meta class
    class Meta:
        # our model
        model = User
        # our fields
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'avatar','password1', 'password2', 'is_superuser', 'is_access', 'is_active', 'is_staff']

# registration user in admin panel for access
class UserFormNotAccess(UserCreationForm):
    # meta class
    class Meta:
        # our model
        model = User
        # our fields
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'avatar','password1', 'password2']
    avatar = forms.ImageField(label=None)
# update form for superuser
class UserFormAccessOnlyYouSuper(forms.ModelForm):
    # meta class
    class Meta:
        # our model
        model = User
        # our fields
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'avatar','is_superuser', 'is_access', 'is_active', 'is_staff']
    avatar = forms.ImageField(label=None)

# update forms for only user
class UserFormAccessOnlyYou(forms.ModelForm):
    # meta class
    class Meta:
        # our model
        model = User
        # our fields
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'avatar']
    

# change set password class
class SetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None

# change PasswordChangeView form
class PasswordChangeForm(PasswordChangeForm, SetPasswordForm):
    field_order = ['old_password', 'new_password1', 'new_password2']
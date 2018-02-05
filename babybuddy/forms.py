# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import get_user_model

from .models import Settings


class UserAddForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active']

    def save(self, commit=True):
        user = super(UserAddForm, self).save(commit=False)
        user.is_superuser = True
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserPasswordForm(PasswordChangeForm):
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['dashboard_refresh_rate']

class UserSignupForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password']


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = (
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2'
            )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name'] 
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']  

        if commit:
            user.save()
        return user    

        

from django import forms
from django.contrib.auth.models import User
from .models import Profile
import os

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    set_default_picture = forms.BooleanField(required=False)
    
    class Meta:
        model = Profile
        fields = ['profile_picture']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email 

    def save(self, user):
        """Save profile changes and handle setting default image."""
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        profile = user.profile
        profile.phone_number = self.cleaned_data['phone_number']

        if self.cleaned_data.get("set_default_picture"):
            # If the hidden field is True, set default image
            profile.profile_picture = "images/profile_pics/default.png"
        elif self.cleaned_data.get("profile_picture"):
            # If a new image is provided, update it
            profile.profile_picture = self.cleaned_data["profile_picture"]
        
        profile.save()
        return profile
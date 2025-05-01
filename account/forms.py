from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        cc_username = cleaned_data.get("username")
        cc_email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if User.objects.filter(username=cc_username).exists():
            raise forms.ValidationError('Username already taken')

        if User.objects.filter(email=cc_email).exists():
            raise forms.ValidationError('Email already taken')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Email'}))
    change_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'Change Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Confirm Password'}))


class UserProfileDetailsForm(forms.ModelForm):
    GENDER_CHOICES = [
        (1, 'Male'),
        (0, 'Female'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ('bio', 'age', 'gender',)
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control w-50', 'placeholder': 'Bio',
                                         'name': "bio",
                                         'rows': "3",
                                         'required id': "id_bio"}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),

        }

from django import forms
from app.models import User, Profile
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=3)


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(help_text=False)
    password_check = forms.CharField(widget=forms.PasswordInput, min_length=3)

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {'password': forms.PasswordInput}

    field_order = ['username', 'email', 'password', 'password_check']

    def clean(self):
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_check']

        if password_1 != password_2:
            raise ValidationError("Passwords do not match!")

        return self.cleaned_data

    def save(self):
        data = self.cleaned_data
        data.pop('password_check')
        user = User.objects.create_user(**data)
        return Profile.objects.create(user=user)

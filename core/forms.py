from django import forms
from core.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    # avatar = forms.ImageField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This user already exist')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError('First name must be only letters')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError('Last name must be only letters')
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        if password != repeat_password:
            raise forms.ValidationError("Passwords are not the same")
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        return self.cleaned_data


class EditForm(forms.Form):
    username = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    # avatar = forms.ImageField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This user already exist')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError('First name must be only letters')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError('Last name must be only letters')
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email
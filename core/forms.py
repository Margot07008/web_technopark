from django import forms


class RegistrationForm(forms.Form):
    class RegistrationForm(forms.Form):
        username = forms.CharField()
        first_name = forms.CharField()
        last_name = forms.CharField()
        email = forms.EmailField()
        password = forms.CharField(widget=forms.PasswordInput)
        repeat_password = forms.CharField(widget=forms.PasswordInput)
        # avatar = forms.ImageField()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class EditForm(forms.Form):
    username = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    # avatar = forms.ImageField()
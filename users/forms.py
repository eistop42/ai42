from django import forms

from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())



    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        # вызов родительского метода инит
        super().__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data

        username = data['username']
        password = data['password']

        # проверка пароля пользователя
        self.user = authenticate(self.request, username=username, password=password)

        if not self.user:
            raise forms.ValidationError('Неверный логин или пароль')

        return data

    def get_user(self):
        return self.user


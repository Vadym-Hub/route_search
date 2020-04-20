from django import forms
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    """Регістрація"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def cleam(self, *args, **kwargs):  # перевірка на регістрацію
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Такий користувач відсутній')
            if not user.check_password(password):
                raise forms.ValidationError('Невірний пароль')
        return super(UserLoginForm, self).clean(*args, **kwargs)

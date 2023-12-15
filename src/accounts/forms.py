from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scrap.models import City, Language

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password')

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('User does not exists')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('False password')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('User is blocked')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords is not eval')
        return cd['password2']


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    send_mail = forms.BooleanField(required=False, widget=forms.CheckboxInput)

    class Meta:
        model = User
        field = ('city', 'language', 'send_mail')


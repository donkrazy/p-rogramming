from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class QuizAuthenticationForm(AuthenticationForm):
    answer = forms.CharField(label='0.9999999999..=?', help_text='힌트: 1')

    def clean_answer(self):
        answer = self.cleaned_data.get('answer', '')
        if answer != '1':
            raise forms.ValidationError('땡 !!!')


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username",)

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('이미 등록된 이메일입니다')
        return email

    def save(self, commit=True):
        user = super(EmailUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class MySignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('이미 등록된 username')
            else:
                return username

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data.get('password2', '')
        if password and password2:
            if password != password2:
                raise forms.ValidationError('확인 비밀번호가 다릅니다')
        if len(password) < 6:
            raise forms.ValidationError('6글자 이상 입력하세요')
        return password

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User()
        user.username = username
        user.set_password(password)

        if commit:
            user.save()
        return user


class EmailLoginForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super(EmailLoginForm, self).clean()
        return cleaned_data

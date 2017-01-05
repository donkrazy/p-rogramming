from django import forms
from megazine.models import Post, Comment
import re
from project.widgets import PointWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'tags', 'lnglat')
        widgets = {
            'lnglat': PointWidget,
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            if len(title) < 3:
                raise forms.ValidationError("3글자 이상 입력해라")
        return title

    def clean_lnglat(self):
        lnglat = self.cleaned_data.get('lnglat', '')
        if lnglat:
            if not re.match(r'\d+\.?\d*,\d+\.?\d*', lnglat):
                raise forms.ValidationError('invalid lnglat')
        return lnglat


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )


class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    age = forms.IntegerField(min_value=1)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username:
            if username.startswith('kim'):
                raise forms.ValidationError('김정은이')
            elif 'fuck' in username:
                raise forms.ValidationError('욕하지마세요')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            if email.endswith('@naver.com'):
                raise forms.ValidationError('야레야레')
        return email

    def clean_age(self):
        age = self.cleaned_data['age']
        if age:
            if age < 19:
                raise forms.ValidationError('애들은 가라 !!!')
        return age

    def clean(self):
        username = self.cleaned_data.get('username', '')
        email = self.cleaned_data.get('email', '')
        age = self.cleaned_data.get('age', 1)
        return self.cleaned_data

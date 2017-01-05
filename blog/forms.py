from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image')

    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            if len(title) < 10:
                raise forms.ValidationError("10글자 입력해라")
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class JokeSignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    age = forms.IntegerField(min_value=1)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username:
            if username.startswith('이'):
                raise forms.ValidationError('저희 정책상, 이씨는 가입할 수 없어요. 죄송.')
            elif 'fuck' in username:
                raise forms.ValidationError('욕하지마세요!')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            if email.endswith('@nis.go.kr'):
                raise forms.ValidationError('국정원 이메일은 가입하실 수 없습니다.')
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

        print(repr(email))
        print(repr(age))

        if email.endswith('@seoul.go.kr') and age < 30:
            raise forms.ValidationError('20대 서울시청 공무원이 있을 수 있습니까?')
        return self.cleaned_data

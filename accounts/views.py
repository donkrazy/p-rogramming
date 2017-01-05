from django.shortcuts import render, redirect
from accounts.forms import (QuizAuthenticationForm, EmailUserCreationForm,
                            MySignupForm, EmailLoginForm)
from django.contrib.auth.views import login as auth_login
from django.contrib.auth import login as user_login
from accounts.models import EmailToken
from .naverMail import send_email
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login(request):
    return auth_login(request,
                      template_name='accounts/form.html',
                      redirect_field_name='next',
                      authentication_form=QuizAuthenticationForm,
                      extra_context={'title': 'Login by ID/PW', })


def login_email(request):
    form = EmailLoginForm()

    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            # Remove previous tokens
            email = form.cleaned_data['email']
            EmailToken.objects.filter(email=email).delete()

            # Create new
            token = EmailToken(email=email)
            token.save()
            send_email(token.token)
            return redirect('refresh')
    return render(request, 'accounts/form.html', {
        'form': form,
        'title': 'Login by email',
        'message': '입력하신 이메일로 1회용 로그인 토큰을 발급합니다'
    })


def login_email_req(request, token):
    time_threshold = datetime.now() - timedelta(hours=1)

    try:
        token = EmailToken.objects.get(token=token,
                                       created_at__gte=time_threshold)
    except ObjectDoesNotExist:
        return render(request, 'accounts/login_notvalidtoken.html', {})
    email = token.email
    # Create user automatically by email as id, token as password
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        user = User.objects.create_user(email, email, token)
        user.save()
    token.delete()
    # Set backend manually
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    user_login(request, user)
    return redirect('megazine:index')


def signup(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user_login(request, user)
            messages.success(request, '{} 님. 가입을 환영합니다.'.format(user))
            return redirect('refresh')
    else:
        form = EmailUserCreationForm()
    return render(request, 'accounts/form.html', {
        'form': form,
        'title': 'Signup',
        'message': 'MEGAZINE 가입을 환영합니다.'
        })


def mySignup(request):
    if request.method == 'POST':
        form = MySignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user_login(request, user)
            messages.success(request, '{} 님. 가입을 환영합니다.'.format(user))
            return redirect('megazine:index')
    else:
        form = MySignupForm()
    return render(request, 'accounts/form.html', {
        'form': form,
        'title': 'mySignup',
        'message': 'MEGAZINE 가입을 환영합니다.'
        })


@login_required
def info(request):
    return render(request, 'accounts/info.html', {
        'title': 'accounts info',
        })

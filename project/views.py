from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})


def refresh(request):
    return render(request, "refresh.html", {})

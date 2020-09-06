from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import SignUpForm


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=username, password=raw_password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('home')
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }
    template = 'signup.html'
    return render(request, template, context)

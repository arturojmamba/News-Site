from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def main_spa(request):
    return render(request, 'api/spa/index.html', {})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to a success page or home
            return redirect('main_spa')
    else:
        form = SignUpForm()
    
    return render(request, 'registration/sign_up.html', {"form": form})

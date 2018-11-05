from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import EmailForm


from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Un compte a été créé pour {username}')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {"form": form})


@login_required
def account(request):

    user = request.user

    if request.method == "POST":
        form = EmailForm(request.POST, instance=user)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            email = email.lower()
            form.save()
            messages.success(
                request, f'Merci d\'enresigtrer votre adress e-mail, {email}')
            return redirect('users:account')
    else:
        form = EmailForm()
    return render(request, 'users/account.html', {"form": form})

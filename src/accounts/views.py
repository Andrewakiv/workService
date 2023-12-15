from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email']
            password = cd['password']
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return redirect('scrap:home_view')
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'accounts/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('scrap:home_view')


def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.success(request, "Profile has been created.")
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context=context)


def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user.city = cd['city']
                user.language = cd['language']
                user.send_mail = cd['send_mail']
                user.save()
                messages.success(request, "Profile details updated.")
                return redirect('accounts:update_view')
        else:
            form = UserUpdateForm(initial={'city': user.city, 'language': user.language, 'send_mail': user.send_mail})
            return render(request, 'accounts/update.html', {'form': form})
    else:
        return redirect("accounts:login")


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, "An account has been deleted.")
    return redirect('scrap:home_view')

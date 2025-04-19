
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from urllib import request
from django.shortcuts import redirect, render,get_object_or_404
from .forms import SignupForm,UserForm,ProfileForm
from django.contrib.auth import authenticate,login
from .models import Profile
from django.urls import reverse


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/accounts/profile')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required  # Ensures only authenticated users can access this view
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=request.user)
        profileform = ProfileForm(request.POST, request.FILES, instance=profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            return redirect(reverse('accounts:profile'))
    else:
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=profile)
    
    return render(request, 'accounts/profile_edit.html', {'userform': userform, 'profileform': profileform})




def logout_view(request):
    logout(request)
    return redirect('login')  # تأكد أن 'login' هو اسم الـ URL لصفحة تسجيل الدخول
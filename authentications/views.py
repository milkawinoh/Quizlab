from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm()
        if form.is_valid:
            form.save
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(password=password, password=password)
            login(request, user)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form':form})
# Create your views here.

# 
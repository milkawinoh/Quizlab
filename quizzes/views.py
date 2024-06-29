# quizzes/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
           # return redirect('quiz_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #return redirect('quiz_list')
        else:
            return render(request, 'templates/registration/login.html', {'error': 'Invalid username or password'})
    return render(request, 'templates/registration/login.html')

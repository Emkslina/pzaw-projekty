from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Score

def home(request):
    return redirect('game')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('game')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('game')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def game_view(request):
    return render(request, 'game.html')

@login_required
def save_score(request):
    if request.method == 'POST':
        points = int(request.POST.get('points', 0))
        Score.objects.create(user=request.user, points=points)
        return redirect('leaderboard')
    return redirect('game')

@login_required
def leaderboard(request):
    top_scores = Score.objects.order_by('-points')[:10]
    return render(request, 'leaderboard.html', {'top_scores': top_scores})
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu')  # Redirige a 'menu' se l'autenticazione ha successo
        else:
            # Gestisci errore di login (opzionale)
            return render(request, 'login.html', {'error': 'Credenziali errate'})
    return render(request, 'login.html')

def menu_view(request):
    return render(request, 'menu.html')

def index_view(request):
    return redirect('login')  # Reindirizza alla pagina di login dalla radice


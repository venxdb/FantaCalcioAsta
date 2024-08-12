# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user     = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu')  # Redirige a 'menu' se l'autenticazione ha successo
        else:
            # Gestisci errore di login (opzionale)
            return render(request, 'login.html', {'error': 'Credenziali errate'})
    return render(request, 'login.html')

@login_required
def menu_view(request):

    user    = request.user
    context = {
        'user_name': user.first_name
    }
    return render(request, 'menu.html', context)

def index_view(request):
    return redirect('login')  # Reindirizza alla pagina di login dalla radice


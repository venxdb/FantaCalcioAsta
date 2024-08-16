# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User, Player_Quotes, Acquisti
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

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


@login_required
def acquisti_view(request):
    if request.method == 'POST':
        allenatore_id = request.POST.get('allenatore')
        giocatore_id = request.POST.get('giocatore')
        crediti = request.POST.get('crediti')

        try:
            allenatore = User.objects.get(id=allenatore_id)
            giocatore = Player_Quotes.objects.get(id=giocatore_id)
            acquisto = Acquisti(allenatore=allenatore, giocatore=giocatore, crediti=crediti)
            acquisto.save()
            return JsonResponse({'success': True, 'message': 'Acquisto salvato con successo!'}) # Redirige a una pagina di successo
        except ObjectDoesNotExist:
            return render(request, 'acquisti.html', {'error': 'Allenatore o giocatore non trovato'})
    
    # Gestione delle richieste GET
    if request.is_ajax() and request.GET.get('action') == 'autocomplete':
        query = request.GET.get('q', '')
        giocatori = Player_Quotes.objects.filter(nome__icontains=query)
        results = [{'id': giocatore.id, 'text': giocatore.nome} for giocatore in giocatori]
        return JsonResponse({'results': results})

    allenatori = User.objects.all()
    return render(request, 'acquisti.html', {'allenatori': allenatori})

@login_required
def budget_view(request):

    allenatori = User.objects.all()
    # raggruppo acquisti per allenatore
    acquisti   = Acquisti.objects.values('allenatore').annotate(spesa_totale = Sum('crediti'))


    budget_per_allenatore = {}
    for a in acquisti:
        allenatore_id      = a["allenatore"]
        spesa_totale       = a['spesa_totale']
        allenatore_nome    = User.objects.get(id = allenatore_id).first_name
        allenatore_cognome = User.objects.get(id = allenatore_id).last_name
        allenatore         = User.objects.get(id = allenatore_id)

        budget_per_allenatore[allenatore] = 350 - spesa_totale
    
    budget_per_allenatore = sorted(budget_per_allenatore.items(), key = lambda x: x[1], reverse = True)

    return render(request, 'budget.html', 
                  {
                      'budget_per_allenatore': budget_per_allenatore,
                      'utente_loggato': request.user})
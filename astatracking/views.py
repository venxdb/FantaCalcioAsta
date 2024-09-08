# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User, Player_Quotes, Acquisti, AstaOfferte, AstaCorrente
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Case, When, IntegerField

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
            return JsonResponse({'success': True, 'message': 'Acquisto salvato con successo!'})
        except ObjectDoesNotExist:
            return render(request, 'acquisti.html', {'error': 'Allenatore o giocatore non trovato'})

    # Gestione delle richieste GET
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.GET.get('action') == 'autocomplete':
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

@login_required
def rose_view(request):
    allenatori = User.objects.all()
    
    rose_dict = []
    for a in allenatori:
        acquisti = Acquisti.objects.filter(allenatore=a)
        
        portieri       = [] 
        difensori      = []
        centrocampisti = []
        attaccanti     = []

        for acq in acquisti:
            giocatore = acq.giocatore
            if giocatore.ruolo == "P":
                portieri.append(giocatore.nome)
            elif giocatore.ruolo == "D":
                difensori.append(giocatore.nome)
            elif giocatore.ruolo == "C":
                centrocampisti.append(giocatore.nome)
            elif giocatore.ruolo == "A": 
                attaccanti.append(giocatore.nome)

        allenatore_dict = {
            "nome": a.username,
            "Portieri": portieri,
            "Difensori": difensori,
            "Centrocampisti": centrocampisti,
            "Attaccanti": attaccanti
        }

        rose_dict.append(allenatore_dict)

    # Dividi gli allenatori in gruppi di 4 per riga
    divisi_in_righe = [rose_dict[i:i + 4] for i in range(0, len(rose_dict), 4)]

    return render(request, 'rose.html',
                  {
                      'divisi_in_righe': divisi_in_righe,
                      'rose': rose_dict,
                      'utente_loggato': request.user
                  })


def asta_view(request):
    asta_corrente = AstaCorrente.objects.filter(in_corso=True).first()

    if request.method == 'POST' and asta_corrente:
        # Verifica se l'utente ha già fatto un'offerta per questa asta
        offerta_esistente = AstaOfferte.objects.filter(
            allenatore=request.user,
            giocatore=asta_corrente.giocatore
        ).exists()

        if offerta_esistente:
            return JsonResponse({'success': False, 'message': 'Hai già fatto un\'offerta per questo giocatore'})

        crediti = request.POST.get('crediti')
        if crediti:
            try:
                crediti = int(crediti)
                AstaOfferte.objects.create(
                    allenatore=request.user,
                    giocatore=asta_corrente.giocatore,
                    crediti=crediti
                )
                return JsonResponse({'success': True, 'message': 'Offerta inviata con successo'})
            except ValueError:
                return JsonResponse({'success': False, 'message': 'Offerta non valida'})
        else:
            return JsonResponse({'success': False, 'message': 'Offerta mancante'})

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if asta_corrente:
            # Verifica se l'utente ha già fatto un'offerta
            offerta_esistente = AstaOfferte.objects.filter(
                allenatore=request.user,
                giocatore=asta_corrente.giocatore
            ).exists()

            return JsonResponse({
                'giocatore_scelto': asta_corrente.giocatore.nome,
                'asta_in_corso': True,
                'offerta_fatta': offerta_esistente
            })
        else:
            return JsonResponse({
                'giocatore_scelto': None,
                'asta_in_corso': False,
                'offerta_fatta': False
            })

    context = {
        'giocatore_scelto': asta_corrente.giocatore.nome if asta_corrente else None
    }
    return render(request, 'asta.html', context)


def admin_asta_view(request):
    if request.method == 'POST':
        if 'giocatore' in request.POST:
            giocatore_id = request.POST['giocatore']
            giocatore_scelto = Player_Quotes.objects.get(id=giocatore_id)

            # Aggiorna o crea la nuova asta corrente
            AstaCorrente.objects.all().delete
            AstaCorrente.objects.update_or_create(
                in_corso=True,
                defaults={'giocatore': giocatore_scelto}
            )
            return JsonResponse({'success': True, 'message': 'Asta avviata con successo'})
        elif 'mostra_offerte' in request.POST:
            offerte = AstaOfferte.objects.all()
            return render(request, 'admin-asta.html', {'offerte': offerte})
    return render(request, 'admin-asta.html')


def admin_offerte(request):

    offerte = AstaOfferte.objects.all()

    giocatore_id = AstaOfferte.objects.values('giocatore').distinct().first()['giocatore']
    giocatore    = Player_Quotes.objects.get(id = giocatore_id).nome

    offerte_list = []
    
    for o in offerte:
        # Ottieni l'offerta (crediti)
        offerta = o.crediti
        
        # Ottieni l'allenatore (utente)
        allenatore = User.objects.get(id=o.allenatore.id)
        
        # Aggiungi tuple (allenatore, offerta) alla lista
        offerte_list.append((allenatore, offerta))
    
    # Ordina la lista delle offerte in base ai crediti (offerta) in ordine decrescente
    offerte_list.sort(key=lambda x: x[1], reverse=True)
    
    # Crea un dizionario che mappa ogni allenatore con la sua offerta e il suo ordine
    offerte_dict = {}
    current_rank = 1
    previous_offerta = None
    count_primo_rank = 0 
    
    for idx, (allenatore, offerta) in enumerate(offerte_list):
        # Se l'offerta è diversa dalla precedente, aggiorna il rank
        if offerta != previous_offerta:
            current_rank = idx + 1
        
        # Memorizza l'offerta e l'ordine (rank)
        offerte_dict[allenatore] = {
            'offerta': offerta,
            'ordine': current_rank
        }

        if current_rank == 1:
            count_primo_rank += 1
        # Aggiorna l'offerta precedente per il prossimo confronto
        previous_offerta = offerta
    
    # Passa il dizionario ordinato al template
    
    if count_primo_rank == 1:
        return render(request, 'admin-offerte-singolo.html', {'giocatore_chiamato': giocatore,'offerte': offerte_dict})
    else:
        return render(request, 'admin-offerte-multiplo.html', {'giocatore_chiamato': giocatore,'offerte': offerte_dict})



@login_required
def lista_view(request):

    order_ruolo = Case(
        When(ruolo_desc = "Portiere",       then = 1),
        When(ruolo_desc = "Difensore",      then = 2),
        When(ruolo_desc = "Centrocampista", then = 3),
        When(ruolo_desc = "Attaccante",     then = 4),
        default      = 5,
        output_field = IntegerField
    )

    giocatori = Player_Quotes.objects.all().order_by(order_ruolo, 'nome')

    squadre = Player_Quotes.objects.values_list('squadra', flat=True).distinct().order_by('squadra')

    # Filtra per ruolo e squadra se richiesto
    ruolo_filtro = request.GET.get('ruolo')
    squadra_filtro = request.GET.get('squadra')

    if ruolo_filtro:
        giocatori = giocatori.filter(ruolo_desc=ruolo_filtro)
    if squadra_filtro:
        giocatori = giocatori.filter(squadra=squadra_filtro)

    context = {
        'giocatori': giocatori,
        'squadre': squadre,
        'ruoli': ['Portiere', 'Difensore', 'Centrocampista', 'Attaccante'],
    }
    return render(request, 'lista_giocatori.html', context)
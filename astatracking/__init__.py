import os
import django

def setup():
    module = os.path.split(os.path.dirname(__file__))[-1]
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fantaasta.settings")
    
    try:
        django.setup()
        print("Django setup completato con successo!")
    except Exception as e:
        print(f"Errore durante il setup di Django: {e}")

    
# django_setup.py
import os
import sys
import django

def setup_django():
    # Trova la directory radice del progetto
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    
    # Aggiungi la directory del progetto al sys.path
    sys.path.append(project_root)
    
    # Configura l'ambiente Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fantaasta.settings')
    
    # Setup Django
    django.setup()

if __name__ == "__main__":
    setup_django()
    print("Django setup completato con successo!")
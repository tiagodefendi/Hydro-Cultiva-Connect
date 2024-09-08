import os
import sys
import django

# Adicionar o diretório do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django_q.tasks import schedule
from myapp.tasks import run_all_device_tasks

def setup_schedules():
    # Agendar a execução da função run_all_device_tasks a cada 30 minutos
    schedule(
        'myapp.tasks.run_all_device_tasks',
        schedule_type='I',  # Intervalo
        minutes=1,  # Tempo entre execuções
        repeats=-1  # Repetir indefinidamente
    )

if __name__ == "__main__":
    setup_schedules()

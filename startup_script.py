import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codepluto.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

def run():
    try:
        print("⚙️ Running migrations...")
        call_command('migrate')

        print("📦 Collecting static files...")
        call_command('collectstatic', '--noinput')

        print("🔐 Creating superuser if not exists...")
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpass123'
            )
            print("✅ Superuser created.")
        else:
            print("ℹ️ Superuser already exists.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    run()

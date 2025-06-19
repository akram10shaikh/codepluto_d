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
        if not User.objects.filter(username='codepluto').exists():
            User.objects.create_superuser(
                username='codepluto@gmail.com',
                email='codepluto@gmail.com',
                password='admin'
            )
            print("✅ Superuser created.")
        else:
            print("ℹ️ Superuser already exists.")

        print("⚙️ migrations again...")
        call_command('migrate')

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    run()

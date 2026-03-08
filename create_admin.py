import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.contrib.auth.models import User

email = "shaxzodturayev123@gmail.com"
password = "admin"
username = "admin" # Superuser requires username usually

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Muvaffaqiyatli yaratildi!")
else:
    u = User.objects.get(username=username)
    u.set_password(password)
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print("Parol o'zgartirildi!")

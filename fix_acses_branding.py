
import paramiko
import sys

host = '62.72.32.37'
user = 'root'
password = 'Aa7161062.123'

def fix_acses_branding():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password)
        
        path = '/var/www/acses_backend/project/settings.py'
        stdin, stdout, stderr = client.exec_command(f"cat {path}")
        content = stdout.read().decode('utf-8', errors='ignore')
        
        # Replacement
        old_jazzmin = """JAZZMIN_SETTINGS = {
    "site_title": "Quantum UZ Admin",
    "site_header": "Quantum UZ",
    "site_brand": "Quantum Dashboard",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Quantum UZ boshqaruv paneliga xush kelibsiz!",
    "copyright": "Quantum UZ Team  2026","""
        
        new_jazzmin = """JAZZMIN_SETTINGS = {
    "site_title": "ACSES Scholar Admin",
    "site_header": "ACSES Scholar",
    "site_brand": "ACSES Dashboard",
    "site_logo_classes": "img-circle",
    "welcome_sign": "ACSES Scholar boshqaruv paneliga xush kelibsiz!",
    "copyright": "ACSES Scholar Team © 2026","""
        
        if old_jazzmin in content:
            new_content = content.replace(old_jazzmin, new_jazzmin)
            print("Fixing ACSES branding...")
            with client.open_sftp() as sftp:
                with sftp.file(path, 'w') as f:
                    f.write(new_content)
            
            print("Restarting ACSES backend (port 8000)...")
            # Find the PID of Gunicorn on 8000 and kill it, then restart
            client.exec_command("fuser -k 8000/tcp")
            client.exec_command("cd /var/www/acses_backend && venv/bin/python3 -m gunicorn project.wsgi:application --bind 127.0.0.1:8000 --daemon")
            print("ACSES branding fixed and restarted.")
        else:
            # Fallback to more flexible replacement if formatting differs
            print("Exact match not found, trying flexible replacement...")
            new_content = content
            new_content = new_content.replace('"site_title": "Quantum UZ Admin"', '"site_title": "ACSES Scholar Admin"')
            new_content = new_content.replace('"site_header": "Quantum UZ"', '"site_header": "ACSES Scholar"')
            new_content = new_content.replace('"site_brand": "Quantum Dashboard"', '"site_brand": "ACSES Dashboard"')
            new_content = new_content.replace('"welcome_sign": "Quantum UZ boshqaruv paneliga xush kelibsiz!"', '"welcome_sign": "ACSES Scholar boshqaruv paneliga xush kelibsiz!"')
            new_content = new_content.replace('"copyright": "Quantum UZ Team', '"copyright": "ACSES Scholar Team')
            
            with client.open_sftp() as sftp:
                with sftp.file(path, 'w') as f:
                    f.write(new_content)
            
            client.exec_command("fuser -k 8000/tcp")
            client.exec_command("cd /var/www/acses_backend && venv/bin/python3 -m gunicorn project.wsgi:application --bind 127.0.0.1:8000 --daemon")
            print("ACSES branding fixed (flexible) and restarted.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    fix_acses_branding()

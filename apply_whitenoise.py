
import paramiko
import sys

host = '62.72.32.37'
user = 'root'
password = 'Aa7161062.123'

def apply_whitenoise(path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password)
        
        stdin, stdout, stderr = client.exec_command(f"cat {path}")
        content = stdout.read().decode('utf-8', errors='ignore')
        
        if 'whitenoise.middleware.WhiteNoiseMiddleware' not in content:
            print(f"Adding Whitenoise to {path}...")
            target = "'django.middleware.security.SecurityMiddleware',"
            replacement = target + "\n    'whitenoise.middleware.WhiteNoiseMiddleware',"
            new_content = content.replace(target, replacement)
            
            with client.open_sftp() as sftp:
                with sftp.file(path, 'w') as f:
                    f.write(new_content)
            return True
        return False
    finally:
        client.close()

if __name__ == "__main__":
    q_path = '/root/var/www/Quantum-Uz-Backend/project/settings.py'
    a_path = '/var/www/acses_backend/project/settings.py'
    
    if apply_whitenoise(q_path):
        print("Quantum Uz: Restarting...")
        # PM2 restart
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password)
        client.exec_command("/root/.nvm/versions/node/v24.14.0/bin/pm2 restart quantum-backend")
        client.close()
        
    if apply_whitenoise(a_path):
        print("ACSES: Restarting on 0.0.0.0:8000...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password)
        client.exec_command("fuser -k 8000/tcp")
        client.exec_command("cd /var/www/acses_backend && venv/bin/python3 -m gunicorn project.wsgi:application --bind 0.0.0.0:8000 --daemon")
        client.close()

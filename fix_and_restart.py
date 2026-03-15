
import paramiko
import sys
import os

host = '62.72.32.37'
user = 'root'
password = 'Aa7161062.123'
backend_path = '/root/var/www/Quantum-Uz-Backend'

def run():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {host}...")
        client.connect(host, username=user, password=password)
        
        local_settings = r'd:\Complete\Quantum uz\Quantum uz backend\project\settings.py'
        remote_settings = f"{backend_path}/project/settings.py"
        
        print(f"Uploading {local_settings} to {remote_settings}...")
        with client.open_sftp() as sftp:
            sftp.put(local_settings, remote_settings)
            
        print("Restarting Gunicorn on 8001...")
        cmd = f"fuser -k 8001/tcp; cd {backend_path} && venv/bin/python3 -m gunicorn project.wsgi:application --bind 0.0.0.0:8001 --daemon"
        stdin, stdout, stderr = client.exec_command(cmd)
        stdout.read()
        err = stderr.read().decode()
        if err: print(f"Stderr: {err}")
        
        print("Verification: Running manage.py check...")
        stdin, stdout, stderr = client.exec_command(f"cd {backend_path} && venv/bin/python3 manage.py check")
        print(stdout.read().decode())
        print(stderr.read().decode(), file=sys.stderr)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run()

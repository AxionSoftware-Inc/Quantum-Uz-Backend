
import paramiko
import sys

host = '62.72.32.37'
user = 'root'
password = 'Aa7161062.123'

def run_commands(commands):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password)
        for cmd in commands:
            print(f"\n--- Running: {cmd} ---")
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read().decode()
            err = stderr.read().decode()
            if out: print(out)
            if err: print(f"ERROR: {err}")
    except Exception as e:
        print(f"Connection Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    commands = [
        "netstat -tulnp | grep :8001",
        "netstat -tulnp | grep :3001",
        "netstat -tulnp | grep :3000",
        "ps aux | grep -E 'python|manage.py|gunicorn|node|next'",
        "/root/.nvm/versions/node/v24.14.0/bin/pm2 list",
        "ls -R /root/Quantum-Uz",
        "ls -R /var/www/Quantum-Uz",
        "ls -la /root",
        "df -h",
        "free -m"
    ]
    run_commands(commands)

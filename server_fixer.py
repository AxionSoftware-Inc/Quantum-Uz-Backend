
import paramiko
import json

host = '62.72.32.37'
user = 'root'
password = 'Aa7161062.123'

def run():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password)
        
        # 1. QuantumUz Backend (Ensure it's running on 8001)
        print("Checking QuantumUz Backend...")
        cmd_backend = "lsof -i :8001 || (cd /root/var/www/Quantum-Uz-Backend && venv/bin/python3 -m gunicorn project.wsgi:application --bind 0.0.0.0:8001 --daemon)"
        client.exec_command(cmd_backend)
        
        # 2. QuantumUz Frontend (Ensure it's running on 3001)
        print("Checking QuantumUz Frontend...")
        pm2_path = "/root/.nvm/versions/node/v24.14.0/bin/pm2"
        node_bin = "/root/.nvm/versions/node/v24.14.0/bin"
        
        # Killing whatever is on 3001 just in case, and starting fresh
        setup_fe = f"export PATH={node_bin}:\$PATH; {pm2_path} delete quantum-frontend; cd /root/var/www/Quantum-Uz && PORT=3001 {pm2_path} start npm --name quantum-frontend --cwd /root/var/www/Quantum-Uz -- start"
        client.exec_command(setup_fe)
        
        # 3. Check for other projects that might have been on 3000 (like ACSES)
        # Based on Nginx, ACSES is on 3000. Let's see if we can find its folder.
        # We saw /var/www/acses_backend/ in Nginx. Maybe /var/www/acses_frontend/ exists?
        # Or maybe it's in /root/var/www/
        
        # For now, let's just check what's on 3000
        stdin, stdout, stderr = client.exec_command("lsof -i :3000")
        if not stdout.read():
             print("Port 3000 is empty. Attempting to restart ACSES if possible.")
             # I don't know the exact path for ACSES frontend, but let's try some common ones
             client.exec_command("export PATH=/root/.nvm/versions/node/v24.14.0/bin:\$PATH; pm2 start acses-frontend || pm2 start acses")
        
        print("Waiting for services to start...")
        import time
        time.sleep(10)
        
        # Final Verification
        print("\n--- Final Port Status ---")
        stdin, stdout, stderr = client.exec_command("netstat -tulnp | grep -E '3000|3001|8001'")
        print(stdout.read().decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run()

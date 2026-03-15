
import paramiko
import sys

def update_nginx(host, user, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password, timeout=10)
        
        nginx_config = """
server {
    listen 80;
    server_name 62.72.32.37;

    location / {
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /django-admin/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/quantum_uz/static/;
    }

    location /media/ {
        alias /var/www/quantum_uz/media/;
    }
}
"""
        sftp = client.open_sftp()
        with sftp.file('/etc/nginx/sites-available/quantum_uz', 'w') as f:
            f.write(nginx_config)
        sftp.close()

        # Update symlinks
        client.exec_command('rm -f /etc/nginx/sites-enabled/default')
        client.exec_command('rm -f /etc/nginx/sites-enabled/acses_scholar')
        client.exec_command('ln -sf /etc/nginx/sites-available/quantum_uz /etc/nginx/sites-enabled/quantum_uz')
        
        # Test and reload Nginx
        stdin, stdout, stderr = client.exec_command('nginx -t && systemctl reload nginx')
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        client.close()
        print("Nginx updated successfully.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_nginx("62.72.32.37", "root", "Aa7161062.123")


import paramiko
import os

def deploy_fix(host, user, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password, timeout=10)
        
        sftp = client.open_sftp()
        
        # Paths on server
        base_path = "/root/var/www/Quantum-Uz"
        
        # Local files to upload
        files_to_upload = [
            ("lib/api.ts", base_path + "/lib/api.ts"),
            ("app/(main)/journal/page.tsx", base_path + "/app/(main)/journal/page.tsx"),
            ("app/(main)/library/page.tsx", base_path + "/app/(main)/library/page.tsx"),
        ]
        
        for local_rel, server_abs in files_to_upload:
            local_abs = os.path.abspath(os.path.join("d:/Complete/Quantum uz", local_rel))
            print(f"Uploading {local_abs} to {server_abs}...")
            # Ensure directory exists
            server_dir = os.path.dirname(server_abs)
            client.exec_command(f"mkdir -p {server_dir}")
            sftp.put(local_abs, server_abs)
            
        sftp.close()
        
        # Restore other projects Nginx
        print("Restoring acses_scholar Nginx symlink...")
        client.exec_command("ln -sf /etc/nginx/sites-available/acses_scholar /etc/nginx/sites-enabled/acses_scholar")
        
        # Restart frontend (Quantum Uz)
        # We need to rebuild since it's Next.js
        print("Rebuilding and restarting frontend...")
        commands = [
            f"cd {base_path}",
            "export PATH=/root/.nvm/versions/node/v24.14.0/bin:$PATH",
            "npm run build",
            "fuser -k 3001/tcp",
            "nohup npm start -- -p 3001 > /root/nt.log 2>&1 &"
        ]
        full_command = " && ".join(commands)
        stdin, stdout, stderr = client.exec_command(full_command)
        
        # We don't wait for build to finish here if it takes long, 
        # but let's at least see if it started.
        print("Deployment triggered. Check /root/nt.log for progress.")
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    deploy_fix("62.72.32.37", "root", "Aa7161062.123")

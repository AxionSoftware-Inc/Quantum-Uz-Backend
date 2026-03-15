
import paramiko
import sys

def ssh_exec(host, user, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password, timeout=20)
        
        stdin, stdout, stderr = client.exec_command(command)
        
        while True:
            line = stdout.readline()
            if not line:
                break
            print(line, end='')
            sys.stdout.flush()
            
        err = stderr.read().decode()
        if err:
            print(f"Stderr: {err}", file=sys.stderr)
            
        client.close()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python ssh_robust.py host user password command")
        sys.exit(1)
    
    host = sys.argv[2] # Adjusting because of how I call it
    user = sys.argv[3]
    password = sys.argv[4]
    command = " ".join(sys.argv[5:])
    
    # Wait, the way I call it in run_command is 'python script.py arg1 arg2 ...'
    # argv[0] = script.py
    # argv[1] = 62.72.32.37
    # argv[2] = root
    # argv[3] = Aa7161062.123
    # argv[4:] = command
    
    host = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]
    command = " ".join(sys.argv[4:])
    
    ssh_exec(host, user, password, command)

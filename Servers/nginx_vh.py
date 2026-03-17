import paramiko
#from pathlib import Path
import os
import shutil

def create_ssh_client(hostname, port, username, password):
    """Create and return an SSH client connected to the specified host."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=username, password=password)
    return client

def execute_command(ssh_client, command):
    """Execute a command on the remote server via SSH and return the output."""
    stdin, stdout, stderr = ssh_client.exec_command(command)
    return stdout.read().decode(), stderr.read().decode()

# def upload_file(ssh_client, local_path, remote_path):
#     """Upload a file to the remote server via SFTP."""
  
#     sftp = ssh_client.open_sftp()
#     sftp.put(local_path, remote_path)
#     sftp.close()
    
def dup_file(ssh_client, src, dest):
    """Duplicate a file from src to dest on a remote server via SSH."""
    # shutil.copyfile(src, dest)  # Original implementation commented out

    sftp = ssh_client.open_sftp()
    try:
        # Copy the file on the remote server
        sftp.put(src, dest)
        print(f"File {src} successfully copied to {dest} on the remote server.")
    except Exception as e:
        print(f"Error copying file: {e}")
    finally:
        sftp.close()

def set_new_vh(ssh_client, file_path, url, forwardip):
    """Modify a virtual host configuration file on a remote server via SSH."""
    sftp = ssh_client.open_sftp()
    try:
        # Read the remote file
        with sftp.open(file_path, 'r') as remote_file:
            config_template = remote_file.readlines()
        
        # Modify the file content
        updated_config = []
        for line in config_template:
            if 'api.garrahan.gov.ar' in line:
                line = line.replace('api.garrahan.gov.ar', url)
            if '172.32.20.83' in line:
                line = line.replace('172.32.20.83', forwardip)
            updated_config.append(line)
        
        # Write the updated content back to the remote file
        with sftp.open(file_path, 'w') as remote_file:
            remote_file.writelines(updated_config)
        
        print(f"File {file_path} successfully updated on the remote server.")
    except Exception as e:
        print(f"Error updating file: {e}")
    finally:
        sftp.close()
            

dominio = '.garrahan.gov.ar'
registro = (input("Ingrese el nombre del nuevo sitio : "))
url = registro + dominio
forwardip = input("Ingrese la IP del mismo : ")
#script_dir = Path(__file__).parent.resolve()
new_file = registro + '.conf'
#src = os.path.join(script_dir, 'template.conf')
#dst = os.path.join(script_dir, new_file)
src = '$HOME/nginx/template.conf'
dst = f'$HOME/nginx/{new_file}'
dup_file(src, dst)
set_new_vh(dst, url, forwardip)

hostname = 'reverseproxy.garrahan.gov.ar'
port = 22
username = 'lperalta'
password = input("Ingrese la contraseña del usuario: ")

remote_path = f'/etc/nginx/sites-available/{new_file}'
ssh_client = create_ssh_client(hostname, port, username, password)
upload_file(ssh_client, dst, remote_path)
import json
import paramiko

def migrate_vlan_interfaces(source_vlan, target_vlan, host, username, password):
   
    # Create an SSH client
    client = paramiko.SSHClient()
    client.load_system_host_keys
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, 22, username=username, password=password, allow_agent=False,look_for_keys=False)

    # Get list of interfaces in the source VLAN
    _, stdout, _ = client.exec_command("show interfaces | json")
    interfaces = json.load(stdout)
    source_vlan_interfaces = [iface for iface in interfaces if iface['vlan'] == source_vlan]

    # Migrate interfaces to target VLAN
    for iface in source_vlan_interfaces:
        command = f"configure terminal\ninterface {iface['name']}\nswitchport access vlan {target_vlan}\nexit\nexit"
        _, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if error:
            print(f"Failed to migrate interface {iface['name']}: {error}")
        else:
            print(f"Migrated interface {iface['name']} to VLAN {target_vlan}")

    # Close the SSH connection
    client.close()

if __name__ == "__main__":
    host = "dns name/ip device"
    username = "user_here"
    password = "password_here"
    source_vlan = x
    target_vlan = y

    migrate_vlan_interfaces(source_vlan, target_vlan, host, username, password)

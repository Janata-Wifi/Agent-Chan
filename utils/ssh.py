
from netmiko import ConnectHandler







def execute_command(hostname,command,device_type,username,password,port=22):

    """
    Execute a command on the device using Netmiko.
    Args:
        command (str or list): Command or list of commands to execute on the device.
        hostname (str): Hostname or IP address. 
        device_type (str): Device type. 
        port (int): SSH port. 
        username (str): SSH username. 
        password (str): SSH password. 
    Returns:
        str or list: Output(s) of the command(s).

    """
    port = port 
    username=username
    password=password
    hostname = hostname # Get hostname from kwargs
    command = command   # Get command from kwargs
    device_type = device_type # Get device_type from kwargs
    
    device = {
        "device_type": device_type, # Use kwargs
        "host": hostname,           # Use kwargs
        "port": port,                 # Use instance attribute
        "username": username,         # Use instance attribute
        "password": password,         # Use instance attribute
    }
    try:
        # Establish the connection
        with ConnectHandler(**device) as net_connect:
            if isinstance(command, list):
                outputs = []
                for cmd in command:
                    output = net_connect.send_command(cmd)
                    outputs.append(output)
                return outputs
            else:
                return net_connect.send_command(command)
    except Exception as e:
        return f"Error executing command: {e}"
# Example usage
if __name__ == "__main__":
    # Initialize the NetmikoExecutor with connection parameters (or rely on env vars)
     # Relying on environment variables for connection details

    # Execute a command, passing connection details and command in kwargs
    command_details = {
        "hostname": "192.168.1.1", # Replace with your device's hostname or IP
        "device_type": "mikrotik_routeros", # Replace with your device type
        "command": ["ip add print", "ip route print"],  # Replace with your desired command
        "username": "admin", # Replace with your SSH username if not in env
        "password": "password",  # Replace with your SSH password if not in env
        "port": 22 # Replace with your SSH port if not default
    }
    output = execute_command(**command_details) # Pass command_details as kwargs
    print(output)
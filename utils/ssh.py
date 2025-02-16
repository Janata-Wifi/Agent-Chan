import os
from dotenv import load_dotenv
from netmiko import ConnectHandler

load_dotenv()

class ssh_handler:
    def __init__(self, hostname=None, device_type=None, port=None, username=None, password=None):
        """
        Initialize the Netmiko SSH handler.
        """
        self.hostname = hostname if hostname else os.environ.get("SSH_HOSTNAME")
        self.device_type = device_type if device_type else os.environ.get("SSH_DEVICE_TYPE")
        self.port = port if port else os.environ.get("SSH_PORT") or 22  # Default to 22 if not in env
        self.username = username if username else os.environ.get("SSH_USERNAME")
        self.password = password if password else os.environ.get("SSH_PASSWORD")


    def execute_command(self, hostname,command,device_type):
        """
        Execute a command on the device using Netmiko.

        Args:
            command (str or list): Command or list of commands to execute on the device.
            hostname (str, optional): Hostname or IP address. Overrides instance hostname if provided.
            device_type (str, optional): Device type. Overrides instance device_type if provided.
            port (int, optional): SSH port. Overrides instance port if provided.
            username (str, optional): SSH username. Overrides instance username if provided.
            password (str, optional): SSH password. Overrides instance password if provided.

        Returns:
            str or list: Output(s) of the command(s).
        """
        hostname = hostname # Get hostname from kwargs
        command = command   # Get command from kwargs
        device_type = device_type # Get device_type from kwargs
        print(hostname,command,device_type)

        device = {
            "device_type": device_type, # Use kwargs
            "host": hostname,           # Use kwargs
            "port": self.port,                 # Use instance attribute
            "username": self.username,         # Use instance attribute
            "password": self.password,         # Use instance attribute
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
    executor = ssh_handler() # Relying on environment variables for connection details

    # Execute a command, passing connection details and command in kwargs
    command_details = {
        "hostname": "192.168.1.1", # Replace with your device's hostname or IP
        "device_type": "mikrotik_routeros", # Replace with your device type
        "command": ["ip add print", "ip route print"],  # Replace with your desired command
        "username": "your_username", # Replace with your SSH username if not in env
        "password": "your_password",  # Replace with your SSH password if not in env
        "port": 22 # Replace with your SSH port if not default
    }
    output = executor.execute_command(**command_details) # Pass command_details as kwargs
    print(output)
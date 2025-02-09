from netmiko import ConnectHandler

class ssh_handler:
    def __init__(self, hostname, port=22, username="admin", password="admin",device_type="mikrotik_routeros"):
        """
        Initialize the ssh_handler with connection parameters.

        Args:
            hostname (str): The hostname or IP address of the device.
            port (int, optional): The port to connect to. Defaults to 22.
            username (str, optional): The username for authentication. Defaults to "admin".
            password (str, optional): The password for authentication. Defaults to "admin".
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.device_type = device_type
    def execute_command(self, command):
        """
        Execute a command on the device using Netmiko.

        Args:
            command (str or list): Command or list of commands to execute on the device.

        Returns:
            str or list: Output(s) of the command(s).
        """
        device = {
            "device_type": self.device_type,
            "host": self.hostname,
            "port": self.port,
            "username": self.username,
            "password": self.password,
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
    # Initialize the NetmikoExecutor with connection parameters
    input_hostname = input("Enter the hostname: ")
    input_port = input("Enter the port: ")
    input_username = input("Enter the username: ")
    input_password = input("Enter the password: ")
            
    executor = ssh_handler(
        hostname=input_hostname,  # Replace with your device's hostname or IP
        port=input_port,
        username=input_username,
        password=input_password,
        
    )

    # Execute a command
    command = ["ip add print","ip route print"]  # Replace with your desired command
    output = executor.execute_command(command)
    print(output)
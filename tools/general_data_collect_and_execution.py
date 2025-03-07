import utils.traceroute as traceroute_module
from utils.ssh import execute_command  
from langchain.tools import tool    
traceroute_instance = traceroute_module.traceroute() # Instantiate Traceroute class

import json

@tool
def traceroute(target_ip: str) -> str:
    """Perform a traceroute.
    you can use this tool to get the traceroute result of the target ip.
    it's useful to get the hop count and the ip address of the last hop.

    Args:
        target_ip: The target IP address. it must be a string.
        

    Returns:
        A string containing the traceroute results.

    """
    target_ip = json.loads(target_ip)
    
    try:
        
        traceroute_result = traceroute_instance.perform_traceroute(target_ip["target_ip"])  # Your actual tool function
        

        traceroute_str = "\n".join([
            f"Hop {hop.get('hop', 'UNKNOWN')}: {hop.get('ip', 'UNKNOWN')} (RTT: {hop.get('rtt', 'UNKNOWN')} ms)"
            for hop in traceroute_result
        ])

        return traceroute_str
    except Exception as e:
        return f"Error performing traceroute: {e}"


@tool
def ssh_into_devices(input:str):
    """Can be used to ssh into any device and execute any command and get the output of that command.

    Args:
        a json object with the following keys:
        hostname: The hostname or IP address of the device.
        command: The command to execute (str or list of str).
        device_type: The device type for Netmiko connection.
        username: SSH username
        password: SSH password
    Returns:
        The output of the command(s).
    """
    input = json.loads(input)   
    try:
        connect = execute_command(input["hostname"],input["command"],input["device_type"],input["username"],input["password"])
        return connect
    except Exception as e:
        return f"Error reading data from device: {e}"




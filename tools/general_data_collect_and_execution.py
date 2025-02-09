import utils.traceroute as traceroute
import utils.ssh as ssh 


def traceroute(target_ip: str) -> str:
    """Perform a traceroute.

    Args:
        target_ip: The target IP address.

    Returns:
        A string containing the traceroute results.
    """
    try:
        
        traceroute_result = traceroute.perform_traceroute(target_ip)  # Your actual tool function
        

        traceroute_str = "\n".join([
            f"Hop {hop.get('hop', 'UNKNOWN')}: {hop.get('ip', 'UNKNOWN')} (RTT: {hop.get('rtt', 'UNKNOWN')} ms)"
            for hop in traceroute_result
        ])

        return traceroute_str
    except Exception as e:
        return f"Error performing traceroute: {e}"




def read_data_from_last_hop(last_hop_ip: str, command: str | list[str], device_type: str) -> str:
    """Reads data from the last hop device.

    Args:
        last_hop_ip: The IP address of the last hop, not the hostname. It has to be ip.
        command: The command to execute on the last hop, can be a single command (str) or a list of commands (list[str]).
        device_type: The device type for netmiko connection.

    Returns:
        str: The output of the command(s).
    """
    connect=ssh.netmiko_executor(hostname=last_hop_ip, device_type=device_type, command=command) # Pass command to executor
    try:
        output = connect.execute() # Execute command via executor - no need to pass command again here
        return output
    except Exception as e:
        return f"Error reading data from last hop: {e}"

    
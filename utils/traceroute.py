import subprocess

def parse_traceroute_output(output):
    """
    Parse the raw traceroute output into a list of hops.

    Args:
    
        output (str): The raw traceroute output.

    Returns:
        list: A list of dictionaries, where each dictionary represents a hop.
    """
    hops = []
    for line in output.splitlines():
        # Skip header lines and empty lines
        if not line.strip() or "traceroute to" in line or "hops max" in line:
            continue

        # Split the line into parts
        parts = line.split()
        if len(parts) < 4:
            continue

        # Extract hop number
        hop_number = parts[0]

        # Extract IP address (handle cases where IP is missing)
        ip_address = None
        for part in parts:
            if "(" in part and ")" in part:  # IP address is in parentheses
                ip_address = part.strip("()")
                break

        # Extract RTT (use the first valid RTT value)
        rtt = None
        for part in parts:
            try:
                rtt = float(part)  # Try converting to float directly
                break  # If successful, break the loop
            except ValueError:
                continue # If not a float, continue to the next part

        # Append the hop to the list (skip if IP or RTT is missing)
        if ip_address and rtt:
            hops.append({
                "hop": int(hop_number),
                "ip": ip_address,
                "rtt": rtt
            })

    return hops

def perform_traceroute(target_ip):
    """
    Perform a traceroute to the specified IP address using the system command.

    Args:
        target_ip (str): The target IP address to traceroute to.

    Returns:
        list: A list of hops with their IP addresses and response times.
    """
    try:
        # Run the traceroute command
        result = subprocess.run(
            ["traceroute", target_ip],  # Use "tracert" on Windows
            capture_output=True,
            text=True
        )
        # Parse the raw output
        return parse_traceroute_output(result.stdout)  # Access result.stdout
    except Exception as e:
        return f"Error performing traceroute: {e}"

# Example usage
if __name__ == "__main__":
    target_ip = "1.1.1.1"  # Replace with the target IP address
    traceroute_result = perform_traceroute(target_ip)

    if isinstance(traceroute_result, list):
        traceroute_str = "\n".join([
            f"Hop {hop['hop']}: {hop['ip']} (RTT: {hop['rtt']:.2f} ms)"
            for hop in traceroute_result
        ])
        print(traceroute_str)
    else:
        print(traceroute_result)
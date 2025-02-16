import subprocess
import platform

class traceroute:
    def __init__(self):
        self.target_ip =  None

    def parse_traceroute_output(self, output_text):
        """Parse the raw traceroute output into a list of hops."""
        hops = []
        for line in output_text.splitlines():
            line = line.strip()  # Remove leading/trailing whitespace
            if not line or "traceroute to" in line or "hops max" in line or "max hops exceeded" in line:
                continue

            parts = line.split()
            if not parts[0].isdigit(): # Check if hop number is a digit
                continue

            try:
                hop_number = int(parts[0])
            except ValueError:
                continue

            ip_address = None
            rtt = None

            # Improved IP and RTT extraction to handle various traceroute formats
            for i in range(1, len(parts)):
                part = parts[i]
                if "(" in part and ")" in part:
                    ip_address = part.strip("()")
                elif ip_address is None and "." in part and ":" not in part: # Check for IP without parentheses
                    ip_address = part
                elif ip_address is None and "[" in part and "]" in part:  #IPv6
                    ip_address = part.strip("[]")
                elif rtt is None:
                    try:
                        rtt = float(part)
                    except ValueError:
                       pass # Ignore if not a float
            
            if ip_address and rtt is not None:
                hops.append({
                    "hop": hop_number,
                    "ip": ip_address,
                    "rtt": rtt
                })

        return hops

    def perform_traceroute(self, target_ip) :
        """Perform a traceroute to the specified IP address."""
        try:
            command = ["traceroute", target_ip]
            if platform.system() == "Windows":
                command = ["tracert", target_ip]  # Windows uses tracert

            result = subprocess.run(command, capture_output=True, text=True, timeout=10) # Added timeout

            if result.returncode != 0:
                error_message = f"Traceroute failed with error:\n{result.stderr}"
                return error_message

            return self.parse_traceroute_output(result.stdout)
        except subprocess.TimeoutExpired:
            return "Traceroute timed out."
        except FileNotFoundError:
            return "Traceroute command not found. Make sure it's installed."
        except Exception as e:
            return f"Error performing traceroute: {e}"

# Example usage
if __name__ == "__main__":
    traceroute_tool = traceroute()
    target_ip = "1.1.1.1"  # Or any other IP
    traceroute_result = traceroute_tool.perform_traceroute(target_ip)

    if isinstance(traceroute_result, list):
        if traceroute_result: # Check if the list is not empty
            traceroute_str = "\n".join([
                f"Hop {hop['hop']}: {hop['ip']} (RTT: {hop['rtt']:.2f} ms)"
                for hop in traceroute_result
            ])
            print(traceroute_str)
        else:
            print("No hops found.") # Indicate if no hops were found
    else:
        print(traceroute_result)  # Print the error message
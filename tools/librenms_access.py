import utils.librenms_api as librenms_tool


def fetch_logs(device_id: int) -> int:
    """Fetch logs for a specific device.

    Args:
        device_id: The ID of the device.

    Returns:
        A string containing the logs.
    """
    try:
        logs = librenms_tool.fetch_eventlog(device_id=int(device_id))  # Your actual tool function
        print("Raw logs data:", logs, "device_id",device_id)  # Debugging: Print raw logs data

        logs_str = "\n".join([
                            f"- {log['datetime']}: {log['message']} (Type: {log['type']}, Severity: {log['severity']})"
                            for log in logs
                        ])

        return logs_str
    except Exception as e:
        return f"Error fetching logs: {e}"


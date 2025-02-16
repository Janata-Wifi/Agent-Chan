import utils.librenms_api as librenms_module
from langchain.tools import tool
import json
librenms_tool = librenms_module.librenms_api()

@tool
def fetch_alerts() -> str:
    """Fetch alerts from LibreNMS.
    
    Returns:
        A string containing the alerts.
    """
    
    try:    
        alerts = librenms_tool.fetch_alerts()
        return alerts
    except Exception as e:
        return f"Error fetching alerts: {e}"

@tool   
def fetch_logs(device_id: str) -> str:
    """Fetch logs for a specific device.

    Args:
        device_id: The ID of the device. it has to be an string.

    Returns:
        A string containing the logs.
    """
    device_id = json.loads(device_id)   
    device_id = device_id["device_id"]
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


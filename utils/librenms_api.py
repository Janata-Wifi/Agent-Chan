import requests
from dotenv import load_dotenv
import os


# Define a relative path to your .env file
 # .env file is in a 'config' directory one level up
load_dotenv()

class librenms_api:
    def __init__(self):
        self.librenms_url = os.environ.get("LIBRENMS_URL")
        self.librenms_token = os.environ.get("LIBRENMS_API_KEY")


    def fetch_alerts(self):
        """Fetch current alerts from LibreNMS."""
        endpoint = f"{self.librenms_url}/api/v0/alerts"
        headers = {
            "X-Auth-Token": self.librenms_token
        }
        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes 
            return response.json()["alerts"]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching alerts from LibreNMS: {e}")
            return []

    def fetch_eventlog(self, device_id: str):
        """Fetch logs for a specific device or alert."""
 
        endpoint = f"{self.librenms_url}/api/v0/logs/eventlog/{device_id}"

        headers = {
            "X-Auth-Token": self.librenms_token
        }
        try:
            response = requests.get(endpoint, headers=headers)
            
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json().get("logs", [])  # Return the list of logs
        except requests.exceptions.RequestException as e:
            print(f"Error fetching logs from LibreNMS: {e}")
            return []
    
    def get_oxidized_config(self, hostname: str):
        """Get the oxidized config for a specific hostname."""
        endpoint = f"{self.librenms_url}/api/v0/oxidized/config/{hostname}"
        headers = {
            "X-Auth-Token": self.librenms_token
        }
        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching oxidized config from LibreNMS: {e}")
            return {}

# if __name__ == "__main__":

#     librenms_tool = librenms_api()
#     print(librenms_tool.fetch_alerts())
    

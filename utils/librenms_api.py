import requests
class librenms_api:
    def __init__(self, librenms_url, librenms_token):
        self.librenms_url = librenms_url
        self.librenms_token = librenms_token

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

    def fetch_eventlog(self, device_id):
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
    
    def get_oxidized_config(self, hostname):
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

if __name__ == "__main__":
    librenms_url = "https://example.com"
    librenms_token = "foo"
    librenms_tool = librenms_api(librenms_url, librenms_token)
    print(librenms_tool.fetch_alerts())
    print(librenms_tool.fetch_eventlog("bar"))
    print(librenms_tool.get_oxidized_config("foo"))

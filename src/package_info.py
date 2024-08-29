import requests
import logging

logger = logging.getLogger(__name__)

def get_package_info(package_name):
    """Get package information from PyPI."""
    print(f"Fetching info for package: {package_name}")  # Debug print
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=5)
        if response.status_code == 200:
            print(f"Successfully fetched info for {package_name}")  # Debug print
            return response.json()
        else:
            print(f"Failed to fetch info for {package_name}. Status code: {response.status_code}")  # Debug print
            logger.warning(f"Failed to fetch info for {package_name}. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching info for {package_name}: {str(e)}")  # Debug print
        logger.error(f"Error fetching info for {package_name}: {str(e)}")
        return None
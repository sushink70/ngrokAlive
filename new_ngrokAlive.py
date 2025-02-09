#!/usr/bin/env python3
"""
This module manages an ngrok tunnel for the Angler C2 project.
It ensures that ngrok is running, retrieves the public tunnel URL,
and (optionally) pushes the URL to a GitHub project page.
"""

import json
import logging
import subprocess
import time
from typing import List

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Constants
NGROK_PATH = "/home/ubuntu/ngrokFunctionalities/./ngrok"
NGROK_API_URL = "http://localhost:4040/api/tunnels"
LOCAL_TUNNEL_ADDRESS = "127.0.0.2:8081"


def get_public_url(api_response: str) -> str:
    """
    Extract the public URL from the ngrok API JSON response.

    Args:
        api_response (str): JSON response from the ngrok API.

    Returns:
        str: The public URL of the tunnel.

    Raises:
        ValueError: If the response is not valid or no tunnel is found.
    """
    try:
        data = json.loads(api_response)
        tunnels = data.get("tunnels", [])
        if not tunnels:
            raise ValueError("No tunnels found in ngrok API response")
        # Get the last tunnel's public_url
        public_url = tunnels[-1].get("public_url")
        if not public_url:
            raise ValueError("Tunnel data does not contain 'public_url'")
        return public_url
    except (json.JSONDecodeError, ValueError) as error:
        logging.error("Failed to parse ngrok API response: %s", error)
        raise


def run_ngrok() -> bool:
    """
    Start the ngrok process to forward traffic to the local address.

    Returns:
        bool: True if ngrok starts successfully; otherwise, False.
    """
    try:
        subprocess.Popen(
            [NGROK_PATH, "http", LOCAL_TUNNEL_ADDRESS],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(4)  # Allow time for ngrok to initialize
        logging.info("ngrok process started successfully.")
        return True
    except Exception as error:
        logging.error("Failed to start ngrok: %s", error)
        return False


def get_process_ids(process_name: str) -> List[int]:
    """
    Retrieve the process IDs of running processes that match the given name.

    Args:
        process_name (str): The name of the process to search for.

    Returns:
        List[int]: A list of matching process IDs. Returns an empty list if none are found.
    """
    try:
        result = subprocess.run(
            ["pgrep", process_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.stdout:
            return [int(pid) for pid in result.stdout.strip().split()]
    except Exception as error:
        logging.error("Error getting process IDs for '%s': %s", process_name, error)
    return []


def push_ngrok_url_to_github(ngrok_url: str) -> None:
    """
    Push the current ngrok URL to the GitHub project page.
    
    Note:
        This function is a placeholder and should be implemented with the
        appropriate GitHub API integration to update your project.

    Args:
        ngrok_url (str): The public ngrok URL to be pushed.
    """
    # TODO: Implement GitHub API integration to update the project page with ngrok_url.
    logging.info("Pushing ngrok URL to GitHub: %s", ngrok_url)
    pass


def ensure_ngrok_running() -> None:
    """
    Ensure that the ngrok tunnel is running and a valid HTTPS public URL is available.
    If ngrok is not running, it will start the process. Once the URL is obtained,
    it will optionally push it to GitHub.
    """
    while True:
        process_ids = get_process_ids("ngrok")
        if not process_ids:
            logging.info("ngrok is not running. Attempting to start ngrok...")
            if not run_ngrok():
                logging.error("Failed to start ngrok. Retrying in 2 seconds...")
                time.sleep(2)
                continue

        try:
            response = requests.get(NGROK_API_URL, timeout=5)
            response.raise_for_status()
            public_url = get_public_url(response.text)

            # Ensure the URL uses HTTPS.
            if not public_url.startswith("https"):
                public_url = public_url.replace("http://", "https://", 1)

            logging.info("ngrok is running at: %s", public_url)
            push_ngrok_url_to_github(public_url)
            break  # Exit once a valid URL is obtained and processed.
        except (requests.RequestException, ValueError) as error:
            logging.warning("Unable to obtain a valid ngrok URL: %s", error)
            logging.info("Retrying in 2 seconds...")
            time.sleep(2)


def main() -> None:
    """
    Main entry point of the script.
    """
    ensure_ngrok_running()


if __name__ == "__main__":
    main()

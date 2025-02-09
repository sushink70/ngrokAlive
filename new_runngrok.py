#!/usr/bin/env python3
"""
This script launches an ngrok tunnel pointing to the local address 127.0.0.2:8081.
It waits for a specified time to allow ngrok to initialize.
"""

import subprocess
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Constants
NGROK_PATH = "/home/ubuntu/ngrokFunctionalities/./ngrok"
NGROK_ARGS = ["http", "127.0.0.2:8081"]
INITIALIZATION_DELAY = 2  # seconds


def run_ngrok() -> subprocess.Popen:
    """
    Starts the ngrok process with the specified arguments.

    Returns:
        subprocess.Popen: The process object for the running ngrok instance.

    Raises:
        Exception: Propagates any exception encountered while starting the process.
    """
    try:
        command = [NGROK_PATH] + NGROK_ARGS
        logging.info("Starting ngrok with command: %s", " ".join(command))
        process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        logging.info("ngrok process started. Waiting %d seconds for initialization...", INITIALIZATION_DELAY)
        time.sleep(INITIALIZATION_DELAY)
        return process
    except Exception as error:
        logging.error("Error starting ngrok: %s", error)
        raise


def main() -> None:
    """
    Main entry point for running the ngrok tunnel.
    """
    run_ngrok()


if __name__ == "__main__":
    main()

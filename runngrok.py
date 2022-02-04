#!/usr/bin/python3

import subprocess
import time

def run():
    ngrok = subprocess.Popen(["/home/ubuntu/ngrokFunctionalities/./ngrok", "http", "127.0.0.2:8081"], stdout=subprocess.DEVNULL)
    time.sleep(2)

run()

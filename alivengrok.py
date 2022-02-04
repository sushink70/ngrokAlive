#This is written by Muhammad Anas
#Otovva INC
#This code is a part of Angler C2 project.

import os
import subprocess
import requests
import json
import time

# split the tunnel url from api output
def getUrlNgrok(ngrok_req):
    json_out = json.loads(ngrok_req)
    tunnel_url = json_out['tunnels'][len(json_out['tunnels'])-1]['public_url']
    return tunnel_url

# run ngrok with new process id. 
def runNgrok():
    ngrok = subprocess.Popen(["/home/ubuntu/ngrokFunctionalities/./ngrok", "http", "127.0.0.2:8081"], stdout=subprocess.DEVNULL)
    time.sleep(4)
    return True

# get process id. check the running status.
def getProcessId(name):
    child = subprocess.Popen(['pgrep', name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    return [int(pid) for pid in response.split()]

# push and commit the current runnning IP/url to github projetc page.
def pushNgrokUrlToGithub(ngrok_address):
    pass

# check ngrok running or not. if not running at the time of reboot or power on then start the ngrok with new process id by calling runNgrok fun. 
def isRunning():
    get_url = True
    run_get_url = True
    ngrok_api_url = "http://localhost:4040/api/tunnels"
    #ngrok_process_id = getProcessId("ngrok")
    #ngrok_pid =  (ngrok_process_id[0])
    while run_get_url:
        ngrok_process_id = getProcessId("ngrok")
        if ngrok_process_id:
            while get_url:
                ngrok_req = requests.get(ngrok_api_url).text
                ngrok_address = getUrlNgrok(ngrok_req)
                if "https" not in ngrok_address:
                    ngrok_address = ngrok_address[0:4] + "s" + ngrok_address[4:]
                    print ("ngrok is running on -> {ngrok_address}".format(ngrok_address = ngrok_address))
                    #push_status = pushNgrokUrlToGithub(ngrok_address)
                    get_url = False
                    run_get_url = False
                else:
                    print ("Unable to get https url :o")
                    print ("Retring to get the https url ;)...")
        else:
            print ("ngrok not running :(")
            print("starting ngrok with new url")
            ngrok_runing_status = runNgrok()
            if ngrok_runing_status == True:
                print ("ngrok started successfully :)")
            else:
                print ("Unable to start ngrok :(... with new url!")

def main():
    isRunning()

if __name__ == "__main__":
    main()

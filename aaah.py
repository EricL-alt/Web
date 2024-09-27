from flask import Flask, jsonify, request
import threading
import random
import time
import sys
import paramiko
import socket
import re

app = Flask(__name__)

running = False
loop_params = {}

def install_script_on_remote_server(hostname, port, username, password, local_script_path, remote_script_path, phone_numbers):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname,port, username, password)

        sftp = ssh.open_sftp()
        #local_script_path = 'checker.py'
        #remote_script_path = '/Users/pxl20//PycharmProjects/pythonProject11/checker.py'

        print(f"Local script path: {local_script_path}")
        print(f"Remote script path: {remote_script_path}")

        sftp.put(local_script_path, remote_script_path)

        stdin, stdout, stderr = ssh.exec_command(f"/usr/bin/python3 {remote_script_path} {phone_numbers}")

        for line in stdout.readlines():
            print(line.strip())
        for line in stderr.readlines():
            print(line.strip(), file=sys.stderr)
    finally:
        if ssh:
            ssh.close()

def run_script_on_remote_laptop(hostname, port, username, password, remote_script_path, phone_numbers):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password, timeout=30)
        stdin, stdout, stderr = ssh.exec_command(f"/usr/bin/python3 {remote_script_path} {phone_numbers}")

        for line in stdout.readlines():
            print(line.strip())
        for line in stderr.readlines():
            print(line.strip(), file=sys.stderr)
        print("Done:)")

    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your username and password.")
    except paramiko.SSHException as e:
        print(f"SSH error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if ssh:
            ssh.close()

def Scamer(ip):
    ip_add_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    port_min = 0
    port_max = 65535

    ip_add_entered = ip

    for port in range(port_min, port_max + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                s.connect((ip_add_entered, port))
                return(port)
        except Exception as e:
            pass
    return("None!?")
print("it works",Scamer('192.168.1.12'))

def NameIsMain(hostname,username,password,remote_script_path,phone_number):
    port = Scamer(hostname)
    remote3=remote_script_path
    install_script_on_remote_server(hostname,port,username,password,'checker.py',remote3,phone_number)
    run_script_on_remote_laptop(hostname,port,username,password,remote3,phone_number)

def run_loop(hostname,username,password,remote_script_path,phone_number):
    global running
    while running:
        NameIsMain(hostname,username,password,remote_script_path,phone_number)
        print("ran repitition 1")
        time.sleep(120)

@app.route('/<string:hostname>/<string:username>/<string:password>/<path:remote_script_path>/<string:phone_number>')
def start_loop(hostname,username,password,remote_script_path,phone_number):
    global running, loop_params
    if not running:
        running = True
        loop_params = (hostname,username,password,"/"+remote_script_path,phone_number)
        thread = threading.Thread(target=run_loop, args=loop_params)
        thread.start()
        return jsonify({"message": "Loop started!", "params": loop_params}), 200
    else:
        return jsonify({"message": "Loop is already running!"}), 200

@app.route('/stop-loop')
def stop_loop():
    global running
    print(running)
    if running:
        running = False
        return jsonify({"message": "Loop stopped!"}), 200
    else:
        return jsonify({"message": "Loop is not running!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
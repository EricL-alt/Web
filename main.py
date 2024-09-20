import sys
import paramiko
import socket
import re
from flask import Flask, request

def install_script_on_remote_server(hostname, port, username, password, local_script_path, remote_script_path):

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

        # Execute the script on the remote server
        stdin, stdout, stderr = ssh.exec_command(f"/usr/bin/python3 {remote_script_path}")

        # Print the output and errors
        for line in stdout.readlines():
            print(line.strip())
        for line in stderr.readlines():
            print(line.strip(), file=sys.stderr)

    #except paramiko.AuthenticationException:
    #    print("Authentication failed. Please check your username and password.")
    #except paramiko.SSHException as e:
    #    print(f"SSH error: {e}")
    #except Exception as e:
    #    print(f"Unexpected error: {e}")
    finally:
        if ssh:
            ssh.close()

def run_script_on_remote_laptop(hostname, port, username, password, remote_script_path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password, timeout=30)
        stdin, stdout, stderr = ssh.exec_command(f"/usr/bin/python3 {remote_script_path}")

        # Print the output and errors
        for line in stdout.readlines():
            print(line.strip())
        for line in stderr.readlines():
            print(line.strip(), file=sys.stderr)

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
        except:
            pass
    return("None!?")

app = Flask(__name__)

@app.route('/<string:hostname>/<string:username>/<string:password>/<path:remote_script_path>')
def hello(hostname,username,password,remote_script_path):
    print(hostname)
    print(username)
    print(password)
    print(str(remote_script_path))
    return(hostname+username+password+str(remote_script_path))

@app.route('/ok')
def ok():
    return("Succesfull")

import os
from flask import Flask, render_template, request
import paramiko

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def execute_command():
    # Get the command from the form
    word = request.form['command']
    #preview_command = "java PageRankMain "
    #command = preview_command + word
    command = word

    # Replace with your instance's IP address or hostname
    hostname = '34.136.208.229'
    # Replace with your SSH username
    username = 'joseguzmanch7'
    # Replace with the path to your SSH private key
    private_key = os.environ.get('PRIVATE_KEY')

    # Create an SSH client and load your private key
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_private_key = paramiko.RSAKey.from_private_key_file(private_key)

    # Connect to the VM using SSH
    ssh_client.connect(hostname=hostname, username=username, pkey=ssh_private_key)

    # Execute the command on the VM
    stdin, stdout, stderr = ssh_client.exec_command(command)

    # Read the output from the command
    output = stdout.read().decode('utf-8')

    # Close the SSH connection
    ssh_client.close()

    # Render the template with the output
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)

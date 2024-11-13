from flask import Flask, redirect, request, Response
import requests
import sys
import os
import random

app = Flask(__name__)
# Append the parent directory of `load_balancer` to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from load_balancer.tables import get_working_hosts

@app.route('/<path:path>', methods=['GET'])
def proxy(path):
    hosts = get_working_hosts()
    
    if not hosts:
        return Response("No available hosts to proxy", status=503)
    
    host = random.randint(0, len(hosts) - 1)
    print(f"Chosen host: {hosts[host]}")
    
    SITE_NAME = f"http://{hosts[host]}/"
    try:
        resp = requests.get(f'{SITE_NAME}{path}')
    except requests.exceptions.RequestException as e:
        return Response(f"Error contacting host: {str(e)}", status=500)

    excluded_headers = ['content-length', 'content-encoding', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    
    return Response(resp.content, resp.status_code, headers)


@app.route('/<path:path>', methods=['POST'])
def postproxy(path):
    hosts = get_working_hosts()
    
    if not hosts:
        return Response("No available hosts to proxy", status=503)
    
    host = random.randint(0, len(hosts) - 1)
    print(f"Chosen host: {hosts[host]}")
    
    SITE_NAME = f"http://{hosts[host]}/"
    try:
        resp = requests.post(f'{SITE_NAME}{path}', json=request.get_json())
    except requests.exceptions.RequestException as e:
        return Response(f"Error contacting host: {str(e)}", status=500)
    
    excluded_headers = ['content-length', 'content-encoding', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    
    return Response(resp.content, resp.status_code, headers)

if __name__ == '__main__':
    app.run(debug=False, port=8100)

import requests
import sys
import os

# Append the parent directory of `load_balancer` to the Python path
sys.path.append(os.path.abspath('/Documents/API/'))
# root_dir = '/API/'

# sys.path.append(root_dir)
from tables import get_all_hosts, update_host_status

host = get_all_hosts()

for host in host:
    url = f'http://{host}/api'
    try:
        res=requests.get(url,timeout=1,verify=False)
        if(res.status_code >= 200 and res.status_code<400):
            update_host_status(host, 'TRUE')
        else: 
            update_host_status(host, 'FALSE')
    except:
        update_host_status(host, 'FALSE')
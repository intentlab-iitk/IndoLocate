"""
File            : indolocate/wsgi.py  
Description     : Indolocate's wsgi file.  
"""

import sys
import socket
from indolocate.app import webserver

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

host, port = get_local_ip(), "9000"

for i, arg in enumerate(sys.argv):
    if arg in ("-b", "--bind") and i + 1 < len(sys.argv):
        try:
            bind = sys.argv[i + 1]
            if ':' in bind:
                port = bind.split(':')[1]
        except Exception:
            pass

print("\n==========================================")
print(f"indolocate is running at http://{host}:{port}\n")

app = webserver() 
server = app.server

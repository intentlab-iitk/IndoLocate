"""
File        : indolocate/__main__.py  
Description : indolocate command script.
"""

import logging
from math import log
import sys
import argparse
import socket

from indolocate import LOG_FORMAT, LOG_LEVEL
from .app import webserver
from .algorithms import init

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Create a socket connection to a dummy address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        # Fallback to localhost
        return "127.0.0.1"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start the indolocate file server.",
        epilog="Warning: This is a development server. Do not use in production."
    )
    parser.add_argument(
        "port",
        type=int,
        nargs="?",
        default=9000,
        help="Port to run the server on (default: 9000)."
    )
    parser.add_argument(
        "host",
        type=str,
        nargs="?",
        default="0.0.0.0",
        help="IP address to bind (use 0.0.0.0 for network access)."
    )
    args = parser.parse_args()

    try:
        model = init('BaseModel')
        model.fit([1], [0])

        logging.info(f"App is running at http://{get_local_ip()}:{args.port}")
        app = webserver(model)
        app.run(host=args.host, port=args.port, debug=True, use_reloader=False)
        print("")
    except PermissionError:
        logging.error(f"Error: Permission denied for port {args.port}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
        sys.exit(1)
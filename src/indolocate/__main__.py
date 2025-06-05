"""
File        : indolocate/__main__.py  
Description : indolocate command script.
"""

import sys
import argparse
from .web import webserver

def main():
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
        app = webserver()
        app.run(host=args.host, port=args.port, debug=True)
    except PermissionError:
        print(f"Error: Permission denied for port {args.port}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Server error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
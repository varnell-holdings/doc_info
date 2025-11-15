"""
Network Web Server for Doctor Preferences App

This starts a web server that can be accessed by other computers on your network.

Usage:
    python start_network_server.py

Then other computers can access it at: http://[THIS_COMPUTER_IP]:8000

For example: http://192.168.1.100:8000/doctor_preferences.html
"""

import http.server
import socketserver
import webbrowser
import socket
import os

PORT = 8000

# ===== CONFIGURATION =====
# Set the directory where your doctor preference files are located
# Change this to your shared network drive location
SERVE_DIRECTORY = r"D:\Nobue"

# You can also use the script's location by uncommenting this line:
# SERVE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
# ==========================


def get_local_ip():
    """Get the local IP address of this computer"""
    try:
        # Create a socket connection to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to Google DNS (doesn't actually send data)
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Unable to determine IP"


# Change to the specified directory
if not os.path.exists(SERVE_DIRECTORY):
    print(f"ERROR: Directory not found: {SERVE_DIRECTORY}")
    print("Please check the path and try again.")
    input("Press Enter to exit...")
    exit(1)

os.chdir(SERVE_DIRECTORY)

Handler = http.server.SimpleHTTPRequestHandler

# Get this computer's IP address
local_ip = get_local_ip()

print("=" * 70)
print("Doctor Preferences Web Server (Network Mode)")
print("=" * 70)
print(f"\n📁 Serving files from: {SERVE_DIRECTORY}")
print(f"\n🌐 Starting server on port {PORT}...")
print(f"\n📍 THIS COMPUTER can access at:")
print(f"   http://localhost:{PORT}/doctor_preferences.html")
print(f"\n🌐 OTHER COMPUTERS on the network can access at:")
print(f"   http://{local_ip}:{PORT}/doctor_preferences.html")
print(f"\n💡 Share this address with other computers: http://{local_ip}:{PORT}")
print("\nPress Ctrl+C to stop the server")
print("=" * 70)

# Automatically open browser on this computer
try:
    webbrowser.open(f"http://localhost:{PORT}/doctor_preferences.html")
    print("\n✓ Browser opened automatically on this computer")
except:
    print("\n! Could not open browser automatically - please open manually")

print("\n🔄 Server is running and waiting for connections...")
print("   (Leave this window open)")

# Start the server - bind to all network interfaces (0.0.0.0)
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")

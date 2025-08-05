#!/usr/bin/env python3
"""
Simple server for Simli integration
"""
import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8083

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    """Start the server"""
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create handler
    handler = MyHTTPRequestHandler
    
    # Create server
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"🚀 Simli Integration Server starting on port {PORT}")
        print(f"📁 Serving files from: {os.getcwd()}")
        print(f"🌐 Open: http://localhost:{PORT}/working_simli_integration.html")
        print("⏹️  Press Ctrl+C to stop")
        
        # Open browser
        webbrowser.open(f"http://localhost:{PORT}/working_simli_integration.html")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    main() 
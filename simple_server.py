#!/usr/bin/env python3
"""
Simple HTTP server for Railway deployment
"""
import http.server
import socketserver
import os

# Use Railway's PORT environment variable
PORT = int(os.environ.get('PORT', 8083))

def main():
    """Start the simple server"""
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create server
    with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"🚀 Simple Server starting on port {PORT}")
        print(f"📁 Serving files from: {os.getcwd()}")
        print(f"🌐 URL: http://localhost:{PORT}/")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    main() 
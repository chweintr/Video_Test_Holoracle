#!/usr/bin/env python3
"""
Simple test server for Railway deployment verification
"""
import http.server
import socketserver
import os
import json

# Use Railway's PORT environment variable, or default to 8083
PORT = int(os.environ.get('PORT', 8083))

class TestHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Indiana Oracle - Server Test</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .success { color: green; }
                    .info { color: blue; }
                </style>
            </head>
            <body>
                <h1>🚀 Indiana Oracle Server is Running!</h1>
                <p class="success">✅ Server is working correctly</p>
                <p class="info">📁 Current directory: """ + os.getcwd() + """</p>
                <p class="info">🌐 Port: """ + str(PORT) + """</p>
                <p><a href="/working_simli_integration.html">🎭 Go to Simli Integration</a></p>
                <p><a href="/index.html">🏠 Go to Home Page</a></p>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode())
        else:
            super().do_GET()

def main():
    """Start the test server"""
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create handler
    handler = TestHTTPRequestHandler
    
    # Create server
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"🚀 Test Server starting on port {PORT}")
        print(f"📁 Serving files from: {os.getcwd()}")
        print(f"🌐 Test URL: http://localhost:{PORT}/")
        print("⏹️  Press Ctrl+C to stop")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    main() 
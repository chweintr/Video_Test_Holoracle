#!/usr/bin/env python3
"""
Simple HTTP server for Railway deployment with very permissive CSP headers for Simli widget
"""
import http.server
import socketserver
import os

# Use Railway's PORT environment variable
PORT = int(os.environ.get('PORT', 8083))

class SimliHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS and very permissive CSP headers for Simli widget
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Very permissive Content Security Policy that allows everything
        csp_policy = (
            "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:; "
            "script-src * 'unsafe-inline' 'unsafe-eval' data: blob:; "
            "style-src * 'unsafe-inline' data: blob:; "
            "img-src * data: blob:; "
            "media-src * data: blob:; "
            "connect-src * data: blob:; "
            "frame-src * data: blob:; "
            "object-src * data: blob:; "
            "base-uri *; "
            "form-action *;"
        )
        self.send_header('Content-Security-Policy', csp_policy)
        
        super().end_headers()

def main():
    """Start the simple server"""
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create server with custom handler
    with socketserver.TCPServer(("", PORT), SimliHTTPRequestHandler) as httpd:
        print(f"🚀 Simple Server starting on port {PORT}")
        print(f"📁 Serving files from: {os.getcwd()}")
        print(f"🌐 URL: http://localhost:{PORT}/")
        print("🔓 Very permissive CSP headers configured for Simli widget")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    main() 
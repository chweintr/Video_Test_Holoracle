#!/usr/bin/env python3
"""
Simple HTTP server for Railway deployment with CSP headers for Simli widget
"""
import http.server
import socketserver
import os

# Use Railway's PORT environment variable
PORT = int(os.environ.get('PORT', 8083))

class SimliHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS and CSP headers for Simli widget
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Content Security Policy that allows Simli widget to work
        csp_policy = (
            "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://app.simli.com https://*.simli.com; "
            "style-src 'self' 'unsafe-inline' https://app.simli.com https://*.simli.com; "
            "img-src 'self' data: blob: https://app.simli.com https://*.simli.com https://*.cloudfront.net; "
            "media-src 'self' blob: https://app.simli.com https://*.simli.com; "
            "connect-src 'self' https://app.simli.com https://*.simli.com https://api.simli.com wss://*.simli.com ws://*.simli.com; "
            "frame-src 'self' https://app.simli.com https://*.simli.com; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
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
        print("🔒 CSP headers configured for Simli widget")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    main() 
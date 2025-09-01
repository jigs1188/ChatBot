#!/usr/bin/env python3
"""
Vercel API endpoint for PWA manifest
This creates a proper serverless function for manifest serving
"""

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve PWA manifest as Vercel API endpoint"""
        
        manifest_data = {
            "id": "rex-ai-assistant-app",
            "name": "Rex AI Assistant",
            "short_name": "Rex",
            "description": "Your intelligent AI assistant for productivity and task management",
            "start_url": "/",
            "display": "standalone",
            "display_override": ["window-controls-overlay", "standalone"],
            "background_color": "#0f172a",
            "theme_color": "#6366f1",
            "orientation": "portrait-primary",
            "scope": "/",
            "lang": "en-US",
            "dir": "ltr",
            "categories": ["productivity", "utilities", "business"],
            "iarc_rating_id": "e84b072d-71de-3dae-a8ea-1234567890ab",
            "launch_handler": {
                "client_mode": "focus-existing"
            },
            "icons": [
                {
                    "src": "https://rex-ai-assistant.vercel.app/api/icon?size=72",
                    "sizes": "72x72",
                    "type": "image/png",
                    "purpose": "any"
                },
                {
                    "src": "https://rex-ai-assistant.vercel.app/api/icon?size=96",
                    "sizes": "96x96",
                    "type": "image/png",
                    "purpose": "any"
                },
                {
                    "src": "https://rex-ai-assistant.vercel.app/api/icon?size=128",
                    "sizes": "128x128",
                    "type": "image/png",
                    "purpose": "any"
                },
                {
                    "src": "https://rex-ai-assistant.vercel.app/api/icon?size=144",
                    "sizes": "144x144",
                    "type": "image/png",
                    "purpose": "any"
                },
                {
                    "src": "https://rex-ai-assistant.vercel.app/api/icon?size=152",
                    "sizes": "152x152",
                    "type": "image/png",
                    "purpose": "any"
                },
                {
                    "src": "https://rex-ai-assistant.vercel.app/api/icon?size=192",
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "any"
                },
                {
                    "src": "https://rex-ai-assistant.vercel.app/api/icon?size=384",
                    "sizes": "384x384",
                    "type": "image/png",
                    "purpose": "any"
                },
                {
                    "src": "https://rex-ai-assistant.vercel.app/api/icon?size=512",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any"
                },
                {
                    "src": "https://rex-ai-assistant.vercel.app/api/icon?size=192&maskable=true",
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "maskable"
                },
                {
                    "src": "https://rex-ai-assistant.vercel.app/api/icon?size=512&maskable=true",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "maskable"
                }
            ],
            "file_handlers": [
                {
                    "action": "/handle-file",
                    "accept": {
                        "text/plain": [".txt"],
                        "application/json": [".json"]
                    }
                }
            ],
            "share_target": {
                "action": "/share",
                "method": "GET",
                "params": {
                    "title": "title",
                    "text": "text",
                    "url": "url"
                }
            },
            "shortcuts": [
                {
                    "name": "Add Todo",
                    "short_name": "Add",
                    "description": "Quickly add a new todo item",
                    "url": "/?action=add-todo",
                    "icons": [
                        {
                            "src": "https://rex-ai-assistant.vercel.app/api/icon?size=96",
                            "sizes": "96x96"
                        }
                    ]
                }
            ],
            "edge_side_panel": {
                "preferred_width": 400
            },
            "protocol_handlers": []
        }
        
        # Set proper headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/manifest+json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Send JSON response
        self.wfile.write(json.dumps(manifest_data, indent=2).encode())

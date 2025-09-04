#!/usr/bin/env python3
"""
Vercel API endpoint for PWA icons
Serves icons dynamically for PWA Builder
"""

from http.server import BaseHTTPRequestHandler
from PIL import Image, ImageDraw
import io
import urllib.parse


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve PWA icons dynamically"""

        # Parse query parameters
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        size = int(params.get("size", ["512"])[0])
        is_maskable = params.get("maskable", ["false"])[0].lower() == "true"

        # Generate icon
        img = self.create_icon(size, is_maskable)

        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG", optimize=True)
        img_bytes.seek(0)

        # Send response
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Cache-Control", "public, max-age=86400")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(img_bytes.getvalue())

    def create_icon(self, size, is_maskable=False):
        """Create professional Rex AI icon"""

        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Adjust padding for maskable icons
        padding = int(size * 0.1) if is_maskable else 0
        effective_size = size - (2 * padding)

        # Modern gradient background
        for i in range(effective_size):
            ratio = i / effective_size
            r = int(99 + (147 - 99) * ratio)
            g = int(102 + (51 - 102) * ratio)
            b = int(241 + (238 - 241) * ratio)
            draw.line(
                [(padding, i + padding), (size - padding, i + padding)],
                fill=(r, g, b, 255),
            )

        # Create circular mask
        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        circle_size = effective_size
        offset = padding
        mask_draw.ellipse(
            [offset, offset, offset + circle_size, offset + circle_size], fill=255
        )
        img.putalpha(mask)

        # Add text
        font_size = max(size // 6, 12)

        # REX text
        text = "REX"
        text_bbox = draw.textbbox((0, 0), text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        x = (size - text_width) // 2
        y = (size - text_height) // 2 - size // 20

        # Shadow
        shadow_offset = max(size // 200, 1)
        draw.text((x + shadow_offset, y + shadow_offset), text, fill=(0, 0, 0, 100))
        draw.text((x, y), text, fill=(255, 255, 255, 255))

        # AI badge
        badge_size = size // 8
        badge_y = y + text_height + size // 20
        badge_x = (size - badge_size * 2) // 2

        draw.rounded_rectangle(
            [badge_x, badge_y, badge_x + badge_size * 2, badge_y + badge_size],
            radius=badge_size // 4,
            fill=(255, 255, 255, 200),
        )

        ai_font_size = max(badge_size // 2, 8)
        ai_text = "AI"
        ai_x = badge_x + badge_size // 2
        ai_y = badge_y + badge_size // 4

        draw.text((ai_x, ai_y), ai_text, fill=(99, 102, 241, 255))

        return img

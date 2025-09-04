#!/usr/bin/env python3
"""
Generate professional PWA logo for Rex AI Assistant
Creates a modern, sleek logo suitable for PWABuilder APK generation
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_professional_logo():
    """Create a professional logo for Rex AI Assistant"""

    # Create high-resolution base image (1024x1024 for best quality)
    size = 1024
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Modern gradient background (indigo to purple)
    for i in range(size):
        # Create vertical gradient
        ratio = i / size
        r = int(99 + (147 - 99) * ratio)  # 99 to 147 (indigo to purple)
        g = int(102 + (51 - 102) * ratio)  # 102 to 51
        b = int(241 + (238 - 241) * ratio)  # 241 to 238
        draw.line([(0, i), (size, i)], fill=(r, g, b, 255))

    # Add circular mask for modern look
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0, size, size], fill=255)

    # Apply mask
    img.putalpha(mask)

    # Add "REX" text in the center
    try:
        # Try to use a system font, fallback to default
        font_size = size // 4
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    # Calculate text position for centering
    text = "REX"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 20  # Slightly above center

    # Add text shadow for depth
    shadow_offset = 4
    draw.text(
        (x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 100)
    )

    # Add main text in white
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

    # Add AI chip/badge below
    badge_y = y + text_height + 30
    badge_width = 120
    badge_height = 40
    badge_x = (size - badge_width) // 2

    # Draw badge background
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_width, badge_y + badge_height],
        radius=20,
        fill=(255, 255, 255, 200),
    )

    # Add "AI" text in badge
    try:
        badge_font_size = badge_height // 2
        try:
            badge_font = ImageFont.truetype("arial.ttf", badge_font_size)
        except:
            try:
                badge_font = ImageFont.truetype(
                    "C:/Windows/Fonts/arial.ttf", badge_font_size
                )
            except:
                badge_font = ImageFont.load_default()
    except:
        badge_font = ImageFont.load_default()

    ai_text = "AI"
    ai_bbox = draw.textbbox((0, 0), ai_text, font=badge_font)
    ai_width = ai_bbox[2] - ai_bbox[0]
    ai_height = ai_bbox[3] - ai_bbox[1]

    ai_x = badge_x + (badge_width - ai_width) // 2
    ai_y = badge_y + (badge_height - ai_height) // 2

    draw.text((ai_x, ai_y), ai_text, font=badge_font, fill=(99, 102, 241, 255))

    return img


def create_all_sizes():
    """Generate all required icon sizes for PWA"""
    logo = create_professional_logo()

    sizes = [72, 96, 128, 144, 152, 192, 384, 512]

    for size in sizes:
        # Resize with high quality
        resized = logo.resize((size, size), Image.Resampling.LANCZOS)

        # Save to static folder
        static_path = f"static/icon-{size}.png"
        resized.save(static_path, "PNG", optimize=True)
        print(f"✅ Created {static_path}")

    # Also create a larger version for PWABuilder
    large_logo = logo.resize((1024, 1024), Image.Resampling.LANCZOS)
    large_logo.save("static/logo-1024.png", "PNG", optimize=True)
    print("✅ Created static/logo-1024.png for PWABuilder")

    # Create favicon
    favicon = logo.resize((32, 32), Image.Resampling.LANCZOS)
    favicon.save("static/favicon.ico", "ICO")
    print("✅ Created static/favicon.ico")


if __name__ == "__main__":
    print("🎨 Generating professional Rex AI logo...")
    create_all_sizes()
    print("\n🎉 All logos generated successfully!")
    print("📱 Ready for PWABuilder APK generation!")

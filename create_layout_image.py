#!/usr/bin/env python3
"""
Create a layout template PNG for Photoshop reference
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_layout_template():
    # Create 1920x1080 canvas
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Try to use a basic font
    try:
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_medium = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Colors
    cyan = '#00ffff'
    magenta = '#ff00ff'
    yellow = '#ffff00'
    white = '#ffffff'
    red = '#ff0000'
    
    # Draw grid lines (every 100px)
    for x in range(0, width, 100):
        draw.line([(x, 0), (x, height)], fill='#333333', width=1)
    for y in range(0, height, 100):
        draw.line([(0, y), (width, y)], fill='#333333', width=1)
    
    # Center crosshair
    center_x, center_y = width // 2, height // 2
    draw.line([(center_x - 50, center_y), (center_x + 50, center_y)], fill=red, width=2)
    draw.line([(center_x, center_y - 50), (center_x, center_y + 50)], fill=red, width=2)
    
    # Title section (80px from top)
    title_y = 80
    title_text = "ECHOES OF INDIANA"
    title_bbox = draw.textbbox((0, 0), title_text, font=font_large)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    
    # Title background
    draw.rectangle([title_x - 40, title_y - 10, title_x + title_width + 40, title_y + 60], 
                  fill='#000000', outline=cyan, width=2)
    draw.text((title_x, title_y), title_text, fill=cyan, font=font_large)
    
    # Subtitle
    subtitle_y = title_y + 70
    subtitle_text = "HOLOGRAPHIC CONVERSATIONS POWERED BY RESEARCH"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=font_small)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    
    draw.rectangle([subtitle_x - 20, subtitle_y - 5, subtitle_x + subtitle_width + 20, subtitle_y + 25], 
                  fill='#000000', outline=magenta, width=1)
    draw.text((subtitle_x, subtitle_y), subtitle_text, fill=magenta, font=font_small)
    
    # Mount container (420x420, raised up by 50px)
    mount_size = 420
    mount_x = (width - mount_size) // 2
    mount_y = (height - mount_size) // 2 - 20  # Raised up from center
    
    # Mount background with glow effect
    draw.rectangle([mount_x - 5, mount_y - 5, mount_x + mount_size + 5, mount_y + mount_size + 5], 
                  fill=cyan, width=0)
    draw.rectangle([mount_x, mount_y, mount_x + mount_size, mount_y + mount_size], 
                  fill='#001a1a', outline=cyan, width=3)
    
    # Mount label
    mount_text = "420 x 420px\nVIDEO MOUNT\n(Simli Widget)"
    mount_text_bbox = draw.textbbox((0, 0), mount_text.split('\n')[0], font=font_medium)
    mount_text_width = mount_text_bbox[2] - mount_text_bbox[0]
    mount_text_x = mount_x + (mount_size - mount_text_width) // 2
    mount_text_y = mount_y + mount_size // 2 - 40
    
    lines = mount_text.split('\n')
    for i, line in enumerate(lines):
        line_bbox = draw.textbbox((0, 0), line, font=font_medium)
        line_width = line_bbox[2] - line_bbox[0]
        line_x = mount_x + (mount_size - line_width) // 2
        draw.text((line_x, mount_text_y + i * 30), line, fill=cyan, font=font_medium)
    
    # Buttons (100px from bottom)
    button_y = height - 100 - 40  # 40px button height
    button_width = 200
    button_height = 40
    button_gap = 30
    
    buttons = [
        ("BROWN COUNTY BIGFOOT", cyan),
        ("HOOSIER ORACLE", cyan),
        ("KURT VONNEGUT", yellow)
    ]
    
    total_width = len(buttons) * button_width + (len(buttons) - 1) * button_gap
    start_x = (width - total_width) // 2
    
    for i, (button_text, color) in enumerate(buttons):
        button_x = start_x + i * (button_width + button_gap)
        
        draw.rectangle([button_x, button_y, button_x + button_width, button_y + button_height], 
                      fill='#000000', outline=color, width=2)
        
        text_bbox = draw.textbbox((0, 0), button_text, font=font_small)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = button_x + (button_width - text_width) // 2
        text_y = button_y + 12
        
        draw.text((text_x, text_y), button_text, fill=color, font=font_small)
    
    # Dimension labels
    # Screen size
    draw.rectangle([10, 10, 200, 50], fill=yellow, outline='#000000')
    draw.text((15, 20), "1920 x 1080px", fill='#000000', font=font_small)
    
    # Title measurement
    draw.text((width//2 - 50, 50), "80px", fill=yellow, font=font_small)
    draw.line([(width//2, 60), (width//2, 80)], fill=yellow, width=1)
    
    # Mount measurement  
    draw.text((mount_x + mount_size + 10, mount_y + mount_size//2), 
             f"420x420px\nCenter - 20px up", fill=yellow, font=font_small)
    
    # Button measurement
    draw.text((width//2 - 30, button_y - 20), "100px", fill=yellow, font=font_small)
    draw.line([(width//2, button_y - 10), (width//2, height - 100)], fill=yellow, width=1)
    
    # Measurements panel
    panel_x = 50
    panel_y = 200
    panel_width = 300
    panel_height = 250
    
    draw.rectangle([panel_x, panel_y, panel_x + panel_width, panel_y + panel_height], 
                  fill='#000000', outline=white, width=2)
    
    measurements = [
        "EXACT POSITIONS:",
        "Canvas: 1920 x 1080px",
        "Title: 80px from top",
        "Subtitle: Below title",
        "Mount: 420 x 420px", 
        "Mount Y: Center - 20px",
        "Buttons: 100px from bottom",
        "Button gap: 30px",
        "Button width: 200px",
        "",
        "COLORS:",
        "Primary: #00ffff (cyan)",
        "Secondary: #ff00ff (magenta)", 
        "Enhanced: #ffff00 (yellow)"
    ]
    
    for i, text in enumerate(measurements):
        color = cyan if text.endswith(':') else white
        if '#' in text:
            color = text.split('#')[1][:6] if len(text.split('#')[1]) >= 6 else white
            color = f'#{color}'
        draw.text((panel_x + 10, panel_y + 10 + i * 16), text, fill=color, font=font_small)
    
    # Save the image
    img.save('layout_template.png', 'PNG')
    print("Layout template saved as layout_template.png")
    print("Specifications:")
    print(f"   Canvas: {width} x {height}px")
    print(f"   Mount: {mount_size}x{mount_size}px at center - 20px up")
    print("   Ready for Photoshop import!")

if __name__ == "__main__":
    create_layout_template()
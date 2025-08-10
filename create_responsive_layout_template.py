#!/usr/bin/env python3
"""
Create a responsive layout template PNG for screen-fitting design
Optimized for 1920x1080 but shows safe zones for smaller screens
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_responsive_layout_template():
    # Create 1920x1080 canvas (most common desktop resolution)
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color='#0a0a0f')
    draw = ImageDraw.Draw(img)
    
    # Try to use system fonts
    try:
        font_large = ImageFont.truetype("arial.ttf", 42)
        font_medium = ImageFont.truetype("arial.ttf", 20)
        font_small = ImageFont.truetype("arial.ttf", 14)
        font_tiny = ImageFont.truetype("arial.ttf", 12)
    except:
        try:
            font_large = ImageFont.truetype("Arial.ttf", 42)  # Windows
            font_medium = ImageFont.truetype("Arial.ttf", 20)
            font_small = ImageFont.truetype("Arial.ttf", 14)
            font_tiny = ImageFont.truetype("Arial.ttf", 12)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_tiny = ImageFont.load_default()
    
    # Colors
    cyan = '#00ffff'
    magenta = '#ff00ff'
    yellow = '#ffff00'
    white = '#ffffff'
    red = '#ff0000'
    green = '#00ff00'
    orange = '#ff8000'
    
    # Safe zones for different screen sizes
    safe_zones = {
        '1366x768': {'w': 1366, 'h': 768, 'color': red},      # Common laptop
        '1440x900': {'w': 1440, 'h': 900, 'color': orange},   # MacBook Air
        '1600x900': {'w': 1600, 'h': 900, 'color': yellow},   # Common widescreen
        '1920x1080': {'w': 1920, 'h': 1080, 'color': cyan}    # Full HD
    }
    
    # Draw safe zone indicators
    for name, zone in safe_zones.items():
        if zone['w'] <= width and zone['h'] <= height:
            x_margin = (width - zone['w']) // 2
            y_margin = (height - zone['h']) // 2
            draw.rectangle([
                x_margin, y_margin, 
                x_margin + zone['w'], y_margin + zone['h']
            ], outline=zone['color'], width=2)
            
            # Label the safe zone
            draw.text((x_margin + 10, y_margin + 10), 
                     f"{name} Safe Zone", 
                     fill=zone['color'], font=font_tiny)
    
    # RESPONSIVE LAYOUT DESIGN
    # Title area - higher up, larger safe margin from top
    title_y = 80
    title_text = "ECHOES OF INDIANA"
    title_bbox = draw.textbbox((0, 0), title_text, font=font_large)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    
    # Title container with padding
    title_padding = 30
    draw.rectangle([
        title_x - title_padding, title_y - 15, 
        title_x + title_width + title_padding, title_y + 55
    ], fill='#000000', outline=cyan, width=3)
    draw.text((title_x, title_y), title_text, fill=cyan, font=font_large)
    
    # Subtitle - closer to title
    subtitle_y = title_y + 80
    subtitle_text = "HOLOGRAPHIC CONVERSATIONS POWERED BY RESEARCH"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=font_small)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    
    subtitle_padding = 20
    draw.rectangle([
        subtitle_x - subtitle_padding, subtitle_y - 8, 
        subtitle_x + subtitle_width + subtitle_padding, subtitle_y + 25
    ], fill='#000000', outline=magenta, width=2)
    draw.text((subtitle_x, subtitle_y), subtitle_text, fill=magenta, font=font_small)
    
    # Mount container - centered vertically with more space
    mount_size = 380  # Slightly smaller for better fit
    mount_x = (width - mount_size) // 2
    mount_y = (height - mount_size) // 2 + 20  # Slight down adjustment
    
    # Mount with glow effect
    glow_size = 5
    draw.rectangle([
        mount_x - glow_size, mount_y - glow_size, 
        mount_x + mount_size + glow_size, mount_y + mount_size + glow_size
    ], fill='#001a33', outline=cyan, width=4)
    
    draw.rectangle([
        mount_x, mount_y, mount_x + mount_size, mount_y + mount_size
    ], fill='#000011', outline=cyan, width=2)
    
    # Mount label
    mount_label = f"{mount_size} x {mount_size}px\nVIDEO MOUNT\n(Hologram Display)"
    lines = mount_label.split('\n')
    line_height = 25
    start_y = mount_y + (mount_size - len(lines) * line_height) // 2
    
    for i, line in enumerate(lines):
        line_bbox = draw.textbbox((0, 0), line, font=font_medium)
        line_width = line_bbox[2] - line_bbox[0]
        line_x = mount_x + (mount_size - line_width) // 2
        draw.text((line_x, start_y + i * line_height), line, fill=cyan, font=font_medium)
    
    # Buttons - positioned with safe margins from bottom
    button_y = height - 120  # Safe margin from bottom
    button_width = 180
    button_height = 50
    button_gap = 25
    
    buttons = [
        ("BROWN COUNTY\nBIGFOOT", cyan),
        ("HOOSIER\nORACLE", cyan),  
        ("KURT\nVONNEGUT", yellow)
    ]
    
    total_buttons_width = len(buttons) * button_width + (len(buttons) - 1) * button_gap
    buttons_start_x = (width - total_buttons_width) // 2
    
    for i, (button_text, color) in enumerate(buttons):
        button_x = buttons_start_x + i * (button_width + button_gap)
        
        draw.rectangle([
            button_x, button_y, 
            button_x + button_width, button_y + button_height
        ], fill='#000000', outline=color, width=3)
        
        # Multi-line button text
        lines = button_text.split('\n')
        line_height = 20
        text_start_y = button_y + (button_height - len(lines) * line_height) // 2
        
        for j, line in enumerate(lines):
            line_bbox = draw.textbbox((0, 0), line, font=font_small)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = button_x + (button_width - line_width) // 2
            draw.text((line_x, text_start_y + j * line_height), line, fill=color, font=font_small)
    
    # Measurements and specifications panel
    specs_x = 50
    specs_y = 50
    specs_width = 350
    specs_height = 400
    
    draw.rectangle([
        specs_x, specs_y, 
        specs_x + specs_width, specs_y + specs_height
    ], fill='#000000', outline=white, width=2)
    
    # Specifications text
    specs = [
        "RESPONSIVE DESIGN SPECIFICATIONS:",
        "",
        "Background Image Size: 1920 x 1080px",
        "Safe zones marked in colors",
        "",
        "LAYOUT MEASUREMENTS:",
        f"Title Y: {title_y}px from top",
        f"Subtitle Y: {subtitle_y}px from top", 
        f"Mount: {mount_size}x{mount_size}px",
        f"Mount Center: {mount_x + mount_size//2}, {mount_y + mount_size//2}",
        f"Buttons Y: {button_y}px from top",
        f"Button size: {button_width}x{button_height}px",
        f"Button gap: {button_gap}px",
        "",
        "SAFE ZONES:",
        "Red: 1366x768 (min supported)",
        "Orange: 1440x900 (MacBook)",
        "Yellow: 1600x900 (common)",
        "Cyan: 1920x1080 (target)",
        "",
        "COLORS:",
        "Primary: #00ffff (cyan)",
        "Secondary: #ff00ff (magenta)",
        "Enhanced: #ffff00 (yellow)",
        "",
        "RESPONSIVE RULES:",
        "• Keep content in red safe zone",
        "• Scale mount 70-90% on mobile",
        "• Stack buttons vertically < 768px",
        "• Reduce font sizes 20% < 1366px"
    ]
    
    line_y = specs_y + 15
    for spec in specs:
        if spec.startswith("RESPONSIVE") or spec.startswith("LAYOUT") or spec.startswith("SAFE") or spec.startswith("COLORS"):
            color = green
            font = font_small
        elif spec.startswith("•"):
            color = yellow  
            font = font_tiny
        elif spec.startswith("Red:") or spec.startswith("Orange:") or spec.startswith("Yellow:") or spec.startswith("Cyan:"):
            color = white
            font = font_tiny
        else:
            color = white
            font = font_tiny
            
        draw.text((specs_x + 10, line_y), spec, fill=color, font=font)
        line_y += 16
    
    # Center crosshairs
    center_x, center_y = width // 2, height // 2
    draw.line([(center_x - 30, center_y), (center_x + 30, center_y)], fill=green, width=2)
    draw.line([(center_x, center_y - 30), (center_x, center_y + 30)], fill=green, width=2)
    draw.text((center_x + 35, center_y - 10), "CENTER", fill=green, font=font_tiny)
    
    # Dimension arrows and labels
    # Title to mount distance
    draw.line([(width//2 - 200, title_y + 55), (width//2 - 200, mount_y)], fill=yellow, width=1)
    draw.text((width//2 - 190, (title_y + 55 + mount_y)//2), 
             f"{mount_y - (title_y + 55)}px", fill=yellow, font=font_tiny)
    
    # Mount to buttons distance  
    draw.line([(width//2 + 220, mount_y + mount_size), (width//2 + 220, button_y)], fill=yellow, width=1)
    draw.text((width//2 + 230, (mount_y + mount_size + button_y)//2), 
             f"{button_y - (mount_y + mount_size)}px", fill=yellow, font=font_tiny)
    
    # Save the template
    filename = 'responsive_layout_template_1920x1080.png'
    img.save(filename, 'PNG')
    
    print(f"Responsive layout template saved as: {filename}")
    print("\nSPECIFICATIONS:")
    print(f"   Canvas: {width} x {height}px")
    print(f"   Mount: {mount_size}x{mount_size}px")
    print(f"   Title Y: {title_y}px")
    print(f"   Buttons Y: {button_y}px")
    print(f"   Safe zones marked for multiple screen sizes")
    print("\nUSAGE:")
    print("   1. Use this as background in Photoshop")
    print("   2. Keep all content within the RED safe zone for universal compatibility")
    print("   3. The CYAN outline shows the full 1920x1080 canvas")
    print("   4. Mount position is optimized for center-screen visibility")

if __name__ == "__main__":
    create_responsive_layout_template()
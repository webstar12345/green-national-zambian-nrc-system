#!/usr/bin/env python
"""
Create Zambian Coat of Arms Image
This script creates a detailed Zambian coat of arms image that can be used in NRC cards
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_detailed_coat_of_arms(width=200, height=240):
    """Create a professional and authentic Zambian coat of arms"""
    # Create image with transparent background
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Authentic Zambian government colors
    zambian_green = (0, 128, 0)
    zambian_red = (220, 20, 60)
    zambian_black = (25, 25, 25)
    zambian_orange = (255, 140, 0)
    white = (255, 255, 255)
    blue = (0, 100, 200)
    brown = (139, 69, 19)
    gold = (255, 215, 0)
    
    # Professional heraldic shield
    shield_center_x = width // 2
    shield_top_y = height // 8
    shield_width = int(width * 0.6)
    shield_height = int(height * 0.55)
    
    # Create authentic heraldic shield shape
    shield_points = [
        (shield_center_x, shield_top_y),  # Top point
        (shield_center_x - shield_width//2, shield_top_y + 15),  # Top left
        (shield_center_x - shield_width//2, shield_top_y + shield_height - 20),  # Left side
        (shield_center_x - 10, shield_top_y + shield_height),  # Bottom left curve
        (shield_center_x, shield_top_y + shield_height + 5),  # Bottom point
        (shield_center_x + 10, shield_top_y + shield_height),  # Bottom right curve
        (shield_center_x + shield_width//2, shield_top_y + shield_height - 20),  # Right side
        (shield_center_x + shield_width//2, shield_top_y + 15),  # Top right
    ]
    
    # Draw shield with professional styling
    draw.polygon(shield_points, fill=white, outline=zambian_black, width=3)
    
    # Add inner border for government authenticity
    inner_shield = [(x + (2 if i % 2 == 0 else -2), y + 2) for i, (x, y) in enumerate(shield_points)]
    draw.polygon(inner_shield, outline=zambian_black, width=1)
    
    # Zambian flag representation (professional layout)
    flag_y = shield_top_y + 20
    flag_height = (shield_height - 40) // 6
    flag_left = shield_center_x - shield_width//2 + 8
    flag_right = shield_center_x + shield_width//2 - 8
    
    # Flag stripes with proper government colors
    draw.rectangle([flag_left, flag_y, flag_right, flag_y + flag_height], fill=zambian_green)
    draw.rectangle([flag_left, flag_y + flag_height, flag_right, flag_y + flag_height*2], fill=zambian_red)
    draw.rectangle([flag_left, flag_y + flag_height*2, flag_right, flag_y + flag_height*3], fill=zambian_black)
    draw.rectangle([flag_left, flag_y + flag_height*3, flag_right, flag_y + flag_height*4], fill=zambian_orange)
    
    # Professional Fish Eagle (national bird of Zambia)
    eagle_center_x = shield_center_x
    eagle_center_y = shield_top_y + shield_height // 2 + 10
    
    # Eagle body with realistic proportions
    draw.ellipse([eagle_center_x - 15, eagle_center_y - 10, eagle_center_x + 15, eagle_center_y + 25], 
                 fill=zambian_black, outline=zambian_black, width=2)
    
    # Realistic eagle wings with proper curvature
    # Left wing
    left_wing_points = [
        (eagle_center_x - 15, eagle_center_y + 5),
        (eagle_center_x - 35, eagle_center_y - 5),
        (eagle_center_x - 40, eagle_center_y + 10),
        (eagle_center_x - 25, eagle_center_y + 18),
    ]
    draw.polygon(left_wing_points, fill=zambian_black, outline=zambian_black, width=1)
    
    # Right wing
    right_wing_points = [
        (eagle_center_x + 15, eagle_center_y + 5),
        (eagle_center_x + 35, eagle_center_y - 5),
        (eagle_center_x + 40, eagle_center_y + 10),
        (eagle_center_x + 25, eagle_center_y + 18),
    ]
    draw.polygon(right_wing_points, fill=zambian_black, outline=zambian_black, width=1)
    
    # Eagle head with proper proportions
    draw.ellipse([eagle_center_x - 8, eagle_center_y - 20, eagle_center_x + 8, eagle_center_y - 5], 
                 fill=zambian_black, outline=zambian_black, width=1)
    
    # Eagle beak (more realistic)
    beak_points = [
        (eagle_center_x, eagle_center_y - 12),
        (eagle_center_x - 5, eagle_center_y - 8),
        (eagle_center_x + 5, eagle_center_y - 8),
    ]
    draw.polygon(beak_points, fill=zambian_orange)
    
    # Eagle talons
    draw.ellipse([eagle_center_x - 3, eagle_center_y + 20, eagle_center_x + 3, eagle_center_y + 25], 
                 fill=zambian_orange)
    
    # Victoria Falls (stylized water representation)
    falls_y = shield_top_y + shield_height - 15
    # Create flowing water effect
    for i in range(3):
        wave_y = falls_y + (i * 2)
        # Natural wave pattern
        for wave_x in range(flag_left, flag_right, 4):
            wave_offset = 2 if (wave_x // 4) % 2 == 0 else -2
            draw.ellipse([wave_x, wave_y + wave_offset, wave_x + 3, wave_y + wave_offset + 2], 
                        fill=blue)
    
    # Professional supporters with authentic tools
    supporter_height = int(height * 0.4)
    supporter_top_y = shield_top_y + 25
    
    # Left supporter (man with pickaxe) - symbol of mining industry
    left_x = shield_center_x - shield_width//2 - 30
    
    # Body with proper proportions
    draw.rectangle([left_x, supporter_top_y + 20, left_x + 10, supporter_top_y + supporter_height], 
                   fill=brown, outline=zambian_black, width=1)
    # Head
    draw.ellipse([left_x - 2, supporter_top_y, left_x + 12, supporter_top_y + 20], 
                 fill=brown, outline=zambian_black, width=1)
    
    # Pickaxe with detailed handle and head
    draw.line([left_x - 8, supporter_top_y - 5, left_x + 15, supporter_top_y + 25], 
              fill=brown, width=3)
    draw.rectangle([left_x + 12, supporter_top_y - 8, left_x + 22, supporter_top_y + 2], 
                   fill=zambian_black)
    
    # Right supporter (woman with hoe) - symbol of agriculture
    right_x = shield_center_x + shield_width//2 + 20
    
    # Body with proper proportions
    draw.rectangle([right_x, supporter_top_y + 20, right_x + 10, supporter_top_y + supporter_height], 
                   fill=brown, outline=zambian_black, width=1)
    # Head
    draw.ellipse([right_x - 2, supporter_top_y, right_x + 12, supporter_top_y + 20], 
                 fill=brown, outline=zambian_black, width=1)
    
    # Hoe with detailed handle and blade
    draw.line([right_x + 15, supporter_top_y - 5, right_x - 8, supporter_top_y + 25], 
              fill=brown, width=3)
    draw.rectangle([right_x - 12, supporter_top_y - 8, right_x - 2, supporter_top_y + 2], 
                   fill=zambian_black)
    
    # Professional government motto banner
    banner_y = shield_top_y + shield_height + 20
    banner_width = width - 30
    banner_height = 30
    banner_x = 15
    
    # Create professional banner with government styling
    draw.rectangle([banner_x, banner_y, banner_x + banner_width, banner_y + banner_height], 
                   fill=white, outline=zambian_black, width=2)
    
    # Add banner decorative ends
    draw.arc([banner_x - 5, banner_y - 2, banner_x + 5, banner_y + banner_height + 2], 
             0, 180, fill=zambian_black, width=2)
    draw.arc([banner_x + banner_width - 5, banner_y - 2, banner_x + banner_width + 5, banner_y + banner_height + 2], 
             0, 180, fill=zambian_black, width=2)
    
    # Official motto text with government font
    try:
        motto_font = ImageFont.truetype("arial.ttf", 14)
    except:
        try:
            motto_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
        except:
            motto_font = ImageFont.load_default()
    
    # "One Zambia, One Nation" - official national motto
    motto = "One Zambia, One Nation"
    try:
        bbox = draw.textbbox((0, 0), motto, font=motto_font)
        text_width = bbox[2] - bbox[0]
        text_x = banner_x + (banner_width - text_width) // 2
        draw.text((text_x, banner_y + 8), motto, fill=zambian_black, font=motto_font)
    except:
        draw.text((banner_x + 10, banner_y + 8), motto, fill=zambian_black, font=motto_font)
    
    return img

def save_coat_of_arms():
    """Save the coat of arms to static directory"""
    # Create coat of arms
    coat_of_arms = create_detailed_coat_of_arms(200, 240)
    
    # Save to static directory
    static_dir = os.path.join('static', 'images')
    os.makedirs(static_dir, exist_ok=True)
    
    coat_path = os.path.join(static_dir, 'zambian_coat_of_arms.png')
    coat_of_arms.save(coat_path, 'PNG')
    
    print(f"✅ Zambian Coat of Arms saved to: {coat_path}")
    
    # Also create a smaller version for NRC cards
    small_coat = create_detailed_coat_of_arms(100, 120)
    small_path = os.path.join(static_dir, 'zambian_coat_of_arms_small.png')
    small_coat.save(small_path, 'PNG')
    
    print(f"✅ Small Coat of Arms saved to: {small_path}")
    
    return coat_path, small_path

if __name__ == '__main__':
    print("🇿🇲 Creating Zambian Coat of Arms...")
    save_coat_of_arms()
    print("🎯 Coat of Arms creation complete!")
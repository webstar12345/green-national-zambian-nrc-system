"""
Generate PWA icons for the NRC System
This script creates all required icon sizes with the Zambian flag colors
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Create icons directory if it doesn't exist
icons_dir = 'static/images/icons'
os.makedirs(icons_dir, exist_ok=True)

# Icon sizes needed for PWA (including iOS specific sizes)
sizes = [72, 96, 128, 144, 152, 167, 180, 192, 384, 512]

# Zambian flag colors
GREEN = '#00A651'
RED = '#DE2010'
BLACK = '#000000'
ORANGE = '#EF7D00'

def create_icon(size):
    """Create a simple NRC icon with Zambian colors"""
    # Create image with green background
    img = Image.new('RGB', (size, size), GREEN)
    draw = ImageDraw.Draw(img)
    
    # Add a border
    border_width = max(2, size // 40)
    draw.rectangle(
        [(border_width, border_width), (size - border_width, size - border_width)],
        outline=ORANGE,
        width=border_width
    )
    
    # Add "NRC" text in the center
    try:
        # Try to use a nice font
        font_size = size // 3
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    text = "NRC"
    
    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Draw text with shadow for better visibility
    shadow_offset = max(1, size // 100)
    draw.text((x + shadow_offset, y + shadow_offset), text, fill=BLACK, font=font)
    draw.text((x, y), text, fill='white', font=font)
    
    return img

# Generate all icon sizes
print("Generating PWA icons...")
for size in sizes:
    icon = create_icon(size)
    filename = f'{icons_dir}/icon-{size}x{size}.png'
    icon.save(filename, 'PNG')
    print(f"✓ Created {filename}")

print("\n✓ All PWA icons generated successfully!")
print(f"Icons saved to: {icons_dir}/")

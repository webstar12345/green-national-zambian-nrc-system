"""
NRC Card Generator - Authentic Zambian NRC Design
Generates a digital National Registration Card matching the exact design of real Zambian NRC cards
"""
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
from datetime import datetime
import random
import string

def generate_nrc_number():
    """Generate a unique NRC number in format: Z 17763276 (matching real format)"""
    from .models import NRCApplication
    
    max_attempts = 100  # Prevent infinite loop
    attempts = 0
    
    while attempts < max_attempts:
        # Generate 8-digit number starting with Z
        number = ''.join(random.choices(string.digits, k=8))
        nrc_number = f"Z {number}"
        
        # Check if this number already exists
        if not NRCApplication.objects.filter(nrc_number=nrc_number).exists():
            return nrc_number
        
        attempts += 1
    
    # If we can't generate a unique number after max_attempts, use timestamp
    timestamp = str(int(datetime.now().timestamp()))[-8:]
    return f"Z {timestamp}"

def generate_nrc_card(application):
    """
    Generate NRC card front and back images matching authentic Zambian NRC design
    Returns tuple of (front_path, back_path)
    """
    # Create media directory if it doesn't exist
    nrc_dir = os.path.join(settings.MEDIA_ROOT, 'nrc_cards')
    os.makedirs(nrc_dir, exist_ok=True)
    
    # Generate NRC number if not exists
    if not hasattr(application, 'nrc_number') or not application.nrc_number:
        nrc_number = generate_nrc_number()
    else:
        nrc_number = application.nrc_number
    
    # Authentic NRC card dimensions (matching real card proportions)
    width, height = 856, 540  # Standard ID card size ratio
    
    # Generate front side
    front_path = generate_front_side(application, nrc_number, width, height, nrc_dir)
    
    # Generate back side
    back_path = generate_back_side(application, nrc_number, width, height, nrc_dir)
    
    return front_path, back_path, nrc_number

def get_fonts():
    """Get fonts with fallback to default"""
    try:
        # Try to load system fonts
        title_font = ImageFont.truetype("arial.ttf", 36)
        header_font = ImageFont.truetype("arialbd.ttf", 28)
        text_font = ImageFont.truetype("arial.ttf", 22)
        small_font = ImageFont.truetype("arial.ttf", 18)
        label_font = ImageFont.truetype("arialbd.ttf", 20)
    except:
        try:
            # Try alternative font paths (Windows)
            title_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 36)
            header_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 28)
            text_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
            small_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
            label_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20)
        except:
            # Fallback to default font
            from PIL import ImageFont
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
    
    return title_font, header_font, text_font, small_font, label_font

def generate_front_side(application, nrc_number, width, height, nrc_dir):
    """Generate the front side of the NRC card - Enhanced Zambian design with better clarity"""
    # Create image with professional gradient background
    img = Image.new('RGB', (width, height), color=(245, 250, 245))
    draw = ImageDraw.Draw(img)
    
    # Green and Black color scheme only
    zambian_green = (0, 120, 50)      # Official Zambian green
    dark_green = (0, 80, 30)          # Darker green for contrast
    light_green = (200, 240, 200)     # Light green for backgrounds
    black = (0, 0, 0)                 # Pure black
    white = (255, 255, 255)           # Pure white
    dark_gray = (40, 40, 40)          # Dark gray (almost black)
    light_gray = (240, 240, 240)      # Light gray
    
    # Get fonts with better sizing
    title_font, header_font, text_font, small_font, label_font = get_fonts()
    
    # Draw enhanced border with green and black only
    draw.rectangle([5, 5, width-5, height-5], outline=zambian_green, width=4)
    draw.rectangle([10, 10, width-10, height-10], outline=black, width=2)
    
    # Header section with green and black styling
    header_y = 20
    # Draw header background
    draw.rectangle([15, 15, width-15, 65], fill=zambian_green, outline=black, width=1)
    
    # "REPUBLIC OF ZAMBIA" in white on green background
    draw.text((30, header_y + 5), "REPUBLIC OF ZAMBIA", fill=white, font=header_font)
    
    # Simple green and black stripe pattern
    stripe_y = header_y + 35
    stripe_width = (width - 60) // 2
    draw.rectangle([30, stripe_y, 30 + stripe_width, stripe_y + 8], fill=dark_green)
    draw.rectangle([30 + stripe_width, stripe_y, width - 30, stripe_y + 8], fill=black)
    
    # Card number in enhanced box
    card_no_x = width - 220
    card_no_y = header_y + 5
    draw.rectangle([card_no_x, card_no_y, width - 20, card_no_y + 35], fill=white, outline=black, width=1)
    draw.text((card_no_x + 10, card_no_y + 2), "CARD No.", fill=black, font=small_font)
    draw.text((card_no_x + 10, card_no_y + 18), nrc_number, fill=zambian_green, font=text_font)
    
    # "NATIONAL REGISTRATION CARD" title with enhanced styling
    title_y = 80
    title_bg_y = title_y - 5
    draw.rectangle([20, title_bg_y, width - 20, title_y + 65], fill=light_gray, outline=dark_gray, width=1)
    
    draw.text((30, title_y), "NATIONAL", fill=zambian_green, font=header_font)
    draw.text((30, title_y + 30), "REGISTRATION CARD", fill=zambian_green, font=header_font)
    
    # Add decorative elements in green and black
    draw.rectangle([width - 150, title_y + 10, width - 30, title_y + 50], fill=dark_green, outline=black, width=1)
    draw.text((width - 140, title_y + 20), "OFFICIAL", fill=white, font=small_font)
    draw.text((width - 140, title_y + 35), "DOCUMENT", fill=white, font=small_font)
    
    # Main content area with enhanced layout
    content_start_y = 160
    
    # Full Name field with enhanced styling
    name_y = content_start_y
    # Create field background
    draw.rectangle([20, name_y - 5, width - 20, name_y + 50], fill=white, outline=zambian_green, width=2)
    
    draw.text((30, name_y), "FULL NAME", fill=zambian_green, font=label_font)
    user = application.user
    full_name = f"{user.first_name} {user.last_name}".upper()
    draw.text((30, name_y + 22), full_name, fill=black, font=text_font)
    
    # Add decorative line
    draw.line([30, name_y + 47, width - 30, name_y + 47], fill=zambian_green, width=2)
    
    # Date of Birth, Place of Birth, and Sex (enhanced layout)
    dob_y = name_y + 70
    
    # Date of Birth section
    dob_width = 200
    draw.rectangle([20, dob_y - 5, 20 + dob_width, dob_y + 50], fill=white, outline=dark_green, width=2)
    draw.text((30, dob_y), "DATE OF BIRTH", fill=dark_green, font=label_font)
    draw.text((30, dob_y + 22), application.date_of_birth.strftime("%d.%m.%Y"), fill=black, font=text_font)
    
    # Place of Birth section (middle)
    pob_x = 240
    pob_width = 280
    draw.rectangle([pob_x, dob_y - 5, pob_x + pob_width, dob_y + 50], fill=white, outline=black, width=2)
    draw.text((pob_x + 10, dob_y), "PLACE OF BIRTH", fill=black, font=label_font)
    place_of_birth = f"{application.village}, {application.district}".upper()
    draw.text((pob_x + 10, dob_y + 22), place_of_birth[:25], fill=black, font=text_font)
    
    # Sex section (right side)
    sex_x = 540
    sex_width = width - sex_x - 20
    draw.rectangle([sex_x, dob_y - 5, width - 20, dob_y + 50], fill=white, outline=black, width=2)
    draw.text((sex_x + 10, dob_y), "SEX", fill=black, font=label_font)
    sex_display = "MALE" if application.sex == 'M' else "FEMALE"
    draw.text((sex_x + 10, dob_y + 22), sex_display, fill=black, font=text_font)
    
    # Parents' Place of Birth (enhanced)
    parents_y = dob_y + 70
    draw.rectangle([20, parents_y - 5, width - 20, parents_y + 50], fill=white, outline=zambian_green, width=2)
    draw.text((30, parents_y), "FATHER'S/MOTHER'S PLACE OF BIRTH", fill=zambian_green, font=label_font)
    parents_place = f"{application.mother_village}, {application.mother_district}".upper()
    draw.text((30, parents_y + 22), parents_place[:40], fill=black, font=text_font)
    
    # Village and District (enhanced side by side)
    village_y = parents_y + 70
    
    # Village section
    village_width = 300
    draw.rectangle([20, village_y - 5, 20 + village_width, village_y + 50], fill=white, outline=zambian_green, width=2)
    draw.text((30, village_y), "VILLAGE", fill=zambian_green, font=label_font)
    draw.text((30, village_y + 22), application.village.upper(), fill=black, font=text_font)
    
    # District section
    district_x = 340
    district_width = width - district_x - 20
    draw.rectangle([district_x, village_y - 5, width - 20, village_y + 50], fill=white, outline=black, width=2)
    draw.text((district_x + 10, village_y), "DISTRICT", fill=black, font=label_font)
    draw.text((district_x + 10, village_y + 22), application.district.upper(), fill=black, font=text_font)
    
    # Chief and Registration Date (enhanced)
    chief_y = village_y + 70
    
    # Chief section
    chief_width = 350
    draw.rectangle([20, chief_y - 5, 20 + chief_width, chief_y + 50], fill=white, outline=black, width=2)
    draw.text((30, chief_y), "CHIEF", fill=black, font=label_font)
    draw.text((30, chief_y + 22), application.chief_name.upper(), fill=black, font=text_font)
    
    # Registration Date section
    reg_date_x = 390
    draw.rectangle([reg_date_x, chief_y - 5, width - 20, chief_y + 50], fill=light_gray, outline=black, width=2)
    draw.text((reg_date_x + 10, chief_y), "REGISTRATION DATE", fill=black, font=label_font)
    reg_date = datetime.now().strftime("%d.%m.%Y")
    draw.text((reg_date_x + 10, chief_y + 22), reg_date, fill=black, font=text_font)
    
    # Special Marks and Date of Renunciation (enhanced)
    marks_y = chief_y + 70
    
    # Special Marks section
    marks_width = 350
    draw.rectangle([20, marks_y - 5, 20 + marks_width, marks_y + 50], fill=white, outline=dark_gray, width=2)
    draw.text((30, marks_y), "SPECIAL MARKS", fill=dark_gray, font=label_font)
    draw.text((30, marks_y + 22), "NONE", fill=black, font=text_font)
    
    # Date of Renunciation section
    renun_x = 390
    draw.rectangle([renun_x, marks_y - 5, width - 20, marks_y + 50], fill=white, outline=dark_gray, width=2)
    draw.text((renun_x + 10, marks_y), "DATE OF RENUNCIATION", fill=dark_gray, font=label_font)
    draw.text((renun_x + 10, marks_y + 22), "N/A", fill=black, font=text_font)
    
    # Enhanced footer with official styling
    footer_y = height - 70
    draw.rectangle([15, footer_y - 10, width - 15, height - 15], fill=zambian_green, outline=black, width=2)
    
    footer_text = "IF THIS CARD IS FOUND, PLEASE RETURN TO NEAREST REGISTRATION OFFICE"
    draw.text((25, footer_y), footer_text, fill=white, font=small_font)
    footer_text2 = "OR POLICE STATION - GOVERNMENT OF ZAMBIA"
    draw.text((25, footer_y + 18), footer_text2, fill=white, font=small_font)
    
    # Add official seal area
    seal_x = width - 120
    seal_y = footer_y - 5
    draw.ellipse([seal_x, seal_y, seal_x + 40, seal_y + 40], fill=white, outline=black, width=2)
    draw.text((seal_x + 8, seal_y + 15), "SEAL", fill=black, font=small_font)
    
    # Add watermark pattern (like real card)
    add_watermark_pattern(draw, width, height)
    
    # Save front side
    front_filename = f"nrc_front_{application.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    front_path = os.path.join(nrc_dir, front_filename)
    img.save(front_path, quality=95)
    
    return f"nrc_cards/{front_filename}"

def generate_back_side(application, nrc_number, width, height, nrc_dir):
    """Generate the back side of the NRC card - Green and Black design"""
    # Create image with light green background
    light_green = (200, 240, 200)  # Light green background
    img = Image.new('RGB', (width, height), color=light_green)
    draw = ImageDraw.Draw(img)
    
    # Green and Black color scheme only
    zambian_green = (0, 120, 50)
    dark_green = (0, 80, 30)
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    # Get fonts
    title_font, header_font, text_font, small_font, label_font = get_fonts()
    
    # Draw main border (black outline)
    draw.rectangle([10, 10, width-10, height-10], outline=black, width=3)
    
    # Photo area (left side) - matching real card layout
    photo_x, photo_y = 30, 50
    photo_width, photo_height = 200, 250
    
    # Draw photo border
    draw.rectangle([photo_x, photo_y, photo_x+photo_width, photo_y+photo_height], 
                   outline=black, width=2, fill=white)
    
    # Try to add applicant photo if available
    if application.photo:
        try:
            photo_path = application.photo.path
            photo = Image.open(photo_path)
            # Resize maintaining aspect ratio
            photo.thumbnail((photo_width-10, photo_height-10), Image.Resampling.LANCZOS)
            # Center the photo
            photo_paste_x = photo_x + (photo_width - photo.width) // 2
            photo_paste_y = photo_y + (photo_height - photo.height) // 2
            img.paste(photo, (photo_paste_x, photo_paste_y))
        except Exception as e:
            # Draw placeholder with person silhouette
            draw.rectangle([photo_x+5, photo_y+5, photo_x+photo_width-5, photo_y+photo_height-5], 
                          fill=(240, 240, 240))
            draw.text((photo_x + photo_width//2 - 30, photo_y + photo_height//2), 
                     "PHOTO", fill=black, font=text_font)
    else:
        # Draw placeholder
        draw.rectangle([photo_x+5, photo_y+5, photo_x+photo_width-5, photo_y+photo_height-5], 
                      fill=(240, 240, 240))
        draw.text((photo_x + photo_width//2 - 30, photo_y + photo_height//2), 
                 "PHOTO", fill=black, font=text_font)
    
    # Registration Number area (top right)
    reg_x = photo_x + photo_width + 30
    reg_y = 50
    draw.text((reg_x, reg_y), "REGISTRATION NUMBER", fill=black, font=small_font)
    
    # Draw registration number box with green pattern
    reg_box_y = reg_y + 25
    draw.rectangle([reg_x, reg_box_y, reg_x + 300, reg_box_y + 40], 
                   outline=black, width=2, fill=zambian_green)
    
    # Add the actual NRC number in white text on green background
    draw.text((reg_x + 10, reg_box_y + 10), nrc_number, fill=white, font=header_font)
    
    # Add wavy pattern inside registration box (white on green) - below the number
    for i in range(2):
        y_pos = reg_box_y + 30 + (i * 4)
        draw.line([reg_x + 10, y_pos, reg_x + 290, y_pos], fill=white, width=1)
    
    # Republic of Zambia text and coat of arms area
    coat_y = reg_y + 100
    draw.text((reg_x, coat_y), "REPUBLIC OF ZAMBIA", fill=black, font=header_font)
    
    # Simple coat of arms area (clean and professional)
    coat_x = reg_x + 50
    coat_arms_y = coat_y + 40
    draw.rectangle([coat_x, coat_arms_y, coat_x + 100, coat_arms_y + 80], 
                   outline=black, width=2, fill=white)
    
    # Simple text representation
    try:
        coat_font = ImageFont.truetype("arial.ttf", 12)
    except:
        coat_font = ImageFont.load_default()
    
    draw.text((coat_x + 15, coat_arms_y + 25), "COAT OF", fill=black, font=coat_font)
    draw.text((coat_x + 20, coat_arms_y + 45), "ARMS", fill=black, font=coat_font)
    
    # Signature areas (bottom section)
    sig_y = photo_y + photo_height + 30
    
    # Signature of Registration Officer
    draw.text((photo_x, sig_y), "SIGNATURE OF REGISTRATION OFFICER", fill=black, font=small_font)
    draw.line([photo_x, sig_y + 40, photo_x + 300, sig_y + 40], fill=black, width=1)
    
    # Signature of Holder
    holder_sig_y = sig_y + 60
    draw.text((photo_x, holder_sig_y), "SIGNATURE OF HOLDER", fill=black, font=small_font)
    draw.line([photo_x, holder_sig_y + 40, photo_x + 300, holder_sig_y + 40], fill=black, width=1)
    
    # Add holder's digital signature if available
    if hasattr(application, 'digital_signature') and application.digital_signature:
        try:
            # Decode base64 signature and add to card
            import base64
            from io import BytesIO
            
            signature_data = base64.b64decode(application.digital_signature)
            signature_img = Image.open(BytesIO(signature_data))
            
            # Resize signature to fit
            signature_img = signature_img.resize((150, 30), Image.Resampling.LANCZOS)
            
            # Paste signature (handle transparency)
            if signature_img.mode == 'RGBA':
                img.paste(signature_img, (photo_x + 10, holder_sig_y + 10), signature_img)
            else:
                img.paste(signature_img, (photo_x + 10, holder_sig_y + 10))
                
        except Exception as e:
            # Fallback to text signature
            user = application.user
            signature_text = f"{user.first_name[0]}. {user.last_name}"
            draw.text((photo_x + 10, holder_sig_y + 20), signature_text, fill=black, font=text_font)
    else:
        # Default text signature
        user = application.user
        signature_text = f"{user.first_name[0]}. {user.last_name}"
        draw.text((photo_x + 10, holder_sig_y + 20), signature_text, fill=black, font=text_font)
    
    # Barcode area (right side) - modern security feature
    barcode_x = reg_x + 150
    barcode_y = sig_y + 20
    draw.text((barcode_x, barcode_y), "SECURITY", fill=black, font=small_font)
    draw.text((barcode_x, barcode_y + 15), "BARCODE", fill=black, font=small_font)
    
    # Barcode box
    barcode_box_y = barcode_y + 35
    draw.rectangle([barcode_x, barcode_box_y, barcode_x + 80, barcode_box_y + 80], 
                   outline=black, width=2, fill=white)
    
    # Generate barcode pattern using NRC number
    generate_barcode_pattern(draw, barcode_x + 5, barcode_box_y + 5, 70, 70, nrc_number)
    
    # Add watermark pattern (like real card)
    add_watermark_pattern(draw, width, height)
    
    # Save back side
    back_filename = f"nrc_back_{application.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    back_path = os.path.join(nrc_dir, back_filename)
    img.save(back_path, quality=95)
    
    return f"nrc_cards/{back_filename}"



def generate_barcode_pattern(draw, x, y, width, height, nrc_number):
    """Generate a simple barcode pattern based on NRC number"""
    # Extract digits from NRC number for barcode pattern
    digits = ''.join(filter(str.isdigit, nrc_number))
    
    # Create barcode-like pattern
    bar_width = width // 20
    current_x = x
    
    for i, digit in enumerate(digits):
        # Convert digit to binary-like pattern
        digit_val = int(digit)
        
        # Create bars based on digit value
        for j in range(4):  # 4 bars per digit
            if (digit_val >> j) & 1:  # If bit is set, draw thick bar
                bar_height = height - 10
                draw.rectangle([current_x, y + 5, current_x + bar_width, y + 5 + bar_height], 
                              fill=(0, 0, 0))
            else:  # If bit not set, draw thin bar
                bar_height = height - 20
                draw.rectangle([current_x, y + 10, current_x + bar_width//2, y + 10 + bar_height], 
                              fill=(0, 0, 0))
            
            current_x += bar_width
            if current_x >= x + width - bar_width:
                break
        
        if current_x >= x + width - bar_width:
            break
    
    # Add barcode number at bottom
    try:
        barcode_font = ImageFont.truetype("arial.ttf", 8)
    except:
        barcode_font = ImageFont.load_default()
    
    draw.text((x, y + height - 15), digits[:8], fill=(0, 0, 0), font=barcode_font)

def add_watermark_pattern(draw, width, height):
    """Add subtle watermark pattern with coat of arms like real NRC card"""
    # Light green watermark color
    watermark_color = (220, 240, 220)
    
    # Add diagonal watermark lines (very light)
    for i in range(0, width + height, 30):
        draw.line([i, 0, i - height, height], fill=watermark_color, width=1)
    
    # Add coat of arms watermark in center
    add_coat_of_arms_watermark(draw, width, height, watermark_color)
    
    # Add some circular patterns (simplified)
    for x in range(100, width - 100, 150):
        for y in range(100, height - 100, 100):
            draw.ellipse([x - 20, y - 20, x + 20, y + 20], 
                        outline=watermark_color, width=1)

def add_coat_of_arms_watermark(draw, width, height, color):
    """Add Zambian coat of arms watermark in center of card"""
    center_x = width // 2
    center_y = height // 2
    
    # Simplified coat of arms design
    coat_width = 120
    coat_height = 140
    
    # Shield outline
    shield_points = [
        (center_x - coat_width//2, center_y - coat_height//2),
        (center_x + coat_width//2, center_y - coat_height//2),
        (center_x + coat_width//2, center_y + coat_height//4),
        (center_x, center_y + coat_height//2),
        (center_x - coat_width//2, center_y + coat_height//4)
    ]
    draw.polygon(shield_points, outline=color, width=2)
    
    # Eagle at top (simplified)
    eagle_y = center_y - coat_height//3
    draw.ellipse([center_x - 15, eagle_y - 10, center_x + 15, eagle_y + 10], outline=color, width=1)
    
    # Wavy lines representing water (Victoria Falls)
    for i in range(3):
        y_pos = center_y - 10 + (i * 8)
        for x in range(center_x - 40, center_x + 40, 8):
            draw.arc([x, y_pos, x + 8, y_pos + 6], 0, 180, fill=color, width=1)
    
    # Corn and mining tools (simplified as crossed lines)
    draw.line([center_x - 30, center_y + 10, center_x + 30, center_y + 30], fill=color, width=2)
    draw.line([center_x + 30, center_y + 10, center_x - 30, center_y + 30], fill=color, width=2)
    
    # "WORK PROGRESS UNITY" banner (simplified)
    banner_y = center_y + coat_height//3
    draw.rectangle([center_x - 50, banner_y, center_x + 50, banner_y + 15], outline=color, width=1)
    
    try:
        watermark_font = ImageFont.truetype("arial.ttf", 8)
        draw.text((center_x - 35, banner_y + 3), "WORK PROGRESS UNITY", fill=color, font=watermark_font)
    except:
        pass

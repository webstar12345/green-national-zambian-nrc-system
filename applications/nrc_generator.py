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
    # Generate 8-digit number starting with Z
    number = ''.join(random.choices(string.digits, k=8))
    return f"Z {number}"

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
    """Generate the front side of the NRC card - matching authentic Zambian design"""
    # Create image with light green background (matching real card)
    nrc_green = (200, 230, 200)  # Light green background like real card
    img = Image.new('RGB', (width, height), color=nrc_green)
    draw = ImageDraw.Draw(img)
    
    # Authentic colors from real NRC card
    black = (0, 0, 0)
    white = (255, 255, 255)
    dark_green = (0, 100, 0)
    
    # Get fonts
    title_font, header_font, text_font, small_font, label_font = get_fonts()
    
    # Draw main border (black outline)
    draw.rectangle([10, 10, width-10, height-10], outline=black, width=3)
    
    # Header section - "REPUBLIC OF ZAMBIA"
    header_y = 25
    draw.text((25, header_y), "REPUBLIC OF ZAMBIA", fill=black, font=header_font)
    
    # Card number in top right (matching real format)
    card_no_x = width - 200
    draw.text((card_no_x, header_y), "CARD No.", fill=black, font=small_font)
    draw.text((card_no_x, header_y + 25), nrc_number, fill=black, font=text_font)
    
    # "NATIONAL REGISTRATION CARD" title
    title_y = 70
    draw.text((25, title_y), "NATIONAL", fill=black, font=header_font)
    draw.text((25, title_y + 30), "REGISTRATION CARD", fill=black, font=header_font)
    
    # Main content area with grid lines (like real card)
    content_start_y = 140
    
    # Full Name field
    name_y = content_start_y
    draw.text((25, name_y), "FULL NAME", fill=black, font=small_font)
    user = application.user
    full_name = f"{user.first_name} {user.last_name}".upper()
    draw.text((25, name_y + 20), full_name, fill=black, font=text_font)
    draw.line([25, name_y + 45, width-25, name_y + 45], fill=black, width=1)
    
    # Date of Birth and Place of Birth (side by side)
    dob_y = name_y + 60
    draw.text((25, dob_y), "DATE OF BIRTH", fill=black, font=small_font)
    draw.text((25, dob_y + 20), application.date_of_birth.strftime("%d.%m.%Y"), fill=black, font=text_font)
    
    # Place of Birth (right side)
    pob_x = 300
    draw.text((pob_x, dob_y), "PLACE OF BIRTH", fill=black, font=small_font)
    place_of_birth = f"{application.village}, {application.district}".upper()
    draw.text((pob_x, dob_y + 20), place_of_birth[:25], fill=black, font=text_font)
    
    # Sex (right side)
    sex_x = width - 150
    draw.text((sex_x, dob_y), "SEX", fill=black, font=small_font)
    sex_display = "M" if application.sex == 'M' else "F"
    draw.text((sex_x, dob_y + 20), sex_display, fill=black, font=text_font)
    
    draw.line([25, dob_y + 45, width-25, dob_y + 45], fill=black, width=1)
    
    # Father's/Mother's Place of Birth
    parents_y = dob_y + 60
    draw.text((25, parents_y), "FATHER'S/MOTHER'S PLACE OF BIRTH", fill=black, font=small_font)
    parents_place = f"{application.mother_village}, {application.mother_district}".upper()
    draw.text((25, parents_y + 20), parents_place[:40], fill=black, font=text_font)
    draw.line([25, parents_y + 45, width-25, parents_y + 45], fill=black, width=1)
    
    # Village and District (side by side)
    village_y = parents_y + 60
    draw.text((25, village_y), "VILLAGE", fill=black, font=small_font)
    draw.text((25, village_y + 20), application.village.upper(), fill=black, font=text_font)
    
    # District (right side)
    district_x = 300
    draw.text((district_x, village_y), "DISTRICT", fill=black, font=small_font)
    draw.text((district_x, village_y + 20), application.district.upper(), fill=black, font=text_font)
    draw.line([25, village_y + 45, width-25, village_y + 45], fill=black, width=1)
    
    # Chief and Registration Date (side by side)
    chief_y = village_y + 60
    draw.text((25, chief_y), "CHIEF", fill=black, font=small_font)
    draw.text((25, chief_y + 20), application.chief_name.upper(), fill=black, font=text_font)
    
    # Registration Date (right side)
    reg_date_x = 400
    draw.text((reg_date_x, chief_y), "REGISTRATION DATE", fill=black, font=small_font)
    reg_date = datetime.now().strftime("%d.%m.%Y")
    draw.text((reg_date_x, chief_y + 20), reg_date, fill=black, font=text_font)
    draw.line([25, chief_y + 45, width-25, chief_y + 45], fill=black, width=1)
    
    # Special Marks and Date of Renunciation (side by side)
    marks_y = chief_y + 60
    draw.text((25, marks_y), "SPECIAL MARKS", fill=black, font=small_font)
    draw.text((25, marks_y + 20), "--", fill=black, font=text_font)
    
    # Date of Renunciation (right side)
    renun_x = 400
    draw.text((renun_x, marks_y), "DATE OF RENUNCIATION", fill=black, font=small_font)
    draw.text((renun_x, marks_y + 20), "--", fill=black, font=text_font)
    draw.line([25, marks_y + 45, width-25, marks_y + 45], fill=black, width=1)
    
    # Footer message
    footer_y = height - 60
    footer_text = "IF THIS CARD IS FOUND, PLEASE RETURN TO NEAREST REGISTRATION OFFICE"
    draw.text((25, footer_y), footer_text, fill=black, font=small_font)
    footer_text2 = "OR POLICE STATION."
    draw.text((25, footer_y + 15), footer_text2, fill=black, font=small_font)
    
    # Add watermark pattern (like real card)
    add_watermark_pattern(draw, width, height)
    
    # Save front side
    front_filename = f"nrc_front_{application.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    front_path = os.path.join(nrc_dir, front_filename)
    img.save(front_path, quality=95)
    
    return f"nrc_cards/{front_filename}"

def generate_back_side(application, nrc_number, width, height, nrc_dir):
    """Generate the back side of the NRC card - matching authentic Zambian design"""
    # Create image with light green background (matching real card)
    nrc_green = (200, 230, 200)  # Light green background like real card
    img = Image.new('RGB', (width, height), color=nrc_green)
    draw = ImageDraw.Draw(img)
    
    # Authentic colors from real NRC card
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (0, 100, 200)
    
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
    
    # Draw registration number box with pattern (like real card)
    reg_box_y = reg_y + 25
    draw.rectangle([reg_x, reg_box_y, reg_x + 300, reg_box_y + 40], 
                   outline=black, width=2, fill=(255, 200, 100))
    
    # Add wavy pattern inside registration box (simplified)
    for i in range(5):
        y_pos = reg_box_y + 8 + (i * 6)
        draw.line([reg_x + 10, y_pos, reg_x + 290, y_pos], fill=black, width=1)
    
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
    """Add subtle watermark pattern like real NRC card"""
    # Add diagonal watermark lines (very light)
    watermark_color = (220, 240, 220)
    
    # Diagonal lines across the card
    for i in range(0, width + height, 30):
        draw.line([i, 0, i - height, height], fill=watermark_color, width=1)
    
    # Add some circular patterns (simplified)
    for x in range(100, width - 100, 150):
        for y in range(100, height - 100, 100):
            draw.ellipse([x - 20, y - 20, x + 20, y + 20], 
                        outline=watermark_color, width=1)

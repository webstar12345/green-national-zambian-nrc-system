"""
NRC Card Generator
Generates a digital National Registration Card with front and back sides
"""
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
from datetime import datetime
import random
import string

def generate_nrc_number():
    """Generate a unique NRC number in format: 123456/78/9"""
    part1 = ''.join(random.choices(string.digits, k=6))
    part2 = ''.join(random.choices(string.digits, k=2))
    part3 = random.choice(string.digits)
    return f"{part1}/{part2}/{part3}"

def generate_nrc_card(application):
    """
    Generate NRC card front and back images
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
    
    # Card dimensions (reduced size for better display)
    width, height = 800, 500
    
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
    """Generate the front side of the NRC card"""
    # Create image with white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Colors
    zambian_green = (0, 166, 81)
    zambian_orange = (255, 130, 0)
    zambian_red = (222, 41, 16)
    black = (0, 0, 0)
    white = (255, 255, 255)
    light_gray = (240, 240, 240)
    dark_gray = (100, 100, 100)
    
    # Get fonts
    title_font, header_font, text_font, small_font, label_font = get_fonts()
    
    # Draw header with Zambian flag colors (thinner stripes)
    draw.rectangle([0, 0, width, 60], fill=zambian_green)
    draw.rectangle([0, 60, width, 75], fill=zambian_red)
    draw.rectangle([0, 75, width, 90], fill=black)
    draw.rectangle([0, 90, width, 105], fill=zambian_orange)
    
    # Draw title on green background
    title_text = "REPUBLIC OF ZAMBIA"
    try:
        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        text_width = bbox[2] - bbox[0]
        draw.text((width//2 - text_width//2, 20), title_text, fill=white, font=title_font)
    except:
        draw.text((width//2, 30), title_text, fill=white, font=title_font)
    
    # Draw "NATIONAL REGISTRATION CARD" text with background
    card_title_y = 130
    draw.rectangle([0, card_title_y-10, width, card_title_y+40], fill=light_gray)
    try:
        card_title = "NATIONAL REGISTRATION CARD"
        bbox = draw.textbbox((0, 0), card_title, font=header_font)
        text_width = bbox[2] - bbox[0]
        draw.text((width//2 - text_width//2, card_title_y), card_title, fill=zambian_green, font=header_font)
    except:
        draw.text((width//2, card_title_y + 10), "NATIONAL REGISTRATION CARD", fill=zambian_green, font=header_font)
    
    # Photo section (left side)
    photo_x, photo_y = 40, 200
    photo_width, photo_height = 200, 240
    
    # Draw photo border with shadow effect
    shadow_offset = 3
    draw.rectangle([photo_x+shadow_offset, photo_y+shadow_offset, 
                   photo_x+photo_width+shadow_offset, photo_y+photo_height+shadow_offset], 
                   fill=(180, 180, 180))
    draw.rectangle([photo_x, photo_y, photo_x+photo_width, photo_y+photo_height], 
                   fill=white, outline=zambian_green, width=3)
    
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
            # Draw placeholder
            draw.rectangle([photo_x+5, photo_y+5, photo_x+photo_width-5, photo_y+photo_height-5], 
                          fill=light_gray)
            try:
                bbox = draw.textbbox((0, 0), "PHOTO", font=header_font)
                text_width = bbox[2] - bbox[0]
                draw.text((photo_x + photo_width//2 - text_width//2, photo_y + photo_height//2), 
                         "PHOTO", fill=dark_gray, font=header_font)
            except:
                draw.text((photo_x + photo_width//2, photo_y + photo_height//2), 
                         "PHOTO", fill=dark_gray, font=header_font)
    else:
        # Draw placeholder
        draw.rectangle([photo_x+5, photo_y+5, photo_x+photo_width-5, photo_y+photo_height-5], 
                      fill=light_gray)
        try:
            bbox = draw.textbbox((0, 0), "PHOTO", font=header_font)
            text_width = bbox[2] - bbox[0]
            draw.text((photo_x + photo_width//2 - text_width//2, photo_y + photo_height//2), 
                     "PHOTO", fill=dark_gray, font=header_font)
        except:
            draw.text((photo_x + photo_width//2, photo_y + photo_height//2), 
                     "PHOTO", fill=dark_gray, font=header_font)
    
    # Information section (right side)
    info_x = 270
    info_y = 200
    line_height = 40
    label_width = 120
    
    # Draw information with better formatting
    user = application.user
    full_name = f"{user.first_name} {user.last_name}".upper()
    
    # NRC Number (prominent)
    draw.rectangle([info_x-10, info_y-10, width-40, info_y+35], fill=zambian_green)
    draw.text((info_x, info_y), "NRC NO:", fill=white, font=label_font)
    draw.text((info_x + label_width, info_y), nrc_number, fill=white, font=header_font)
    
    # Name
    current_y = info_y + line_height + 10
    draw.text((info_x, current_y), "NAME:", fill=zambian_green, font=label_font)
    draw.text((info_x + label_width, current_y), full_name[:25], fill=black, font=text_font)
    
    # Date of Birth
    current_y += line_height
    draw.text((info_x, current_y), "DOB:", fill=zambian_green, font=label_font)
    draw.text((info_x + label_width, current_y), 
              application.date_of_birth.strftime("%d/%m/%Y"), fill=black, font=text_font)
    
    # Sex
    current_y += line_height
    draw.text((info_x, current_y), "SEX:", fill=zambian_green, font=label_font)
    sex_display = "MALE" if application.sex == 'M' else "FEMALE"
    draw.text((info_x + label_width, current_y), sex_display, fill=black, font=text_font)
    
    # Village
    current_y += line_height
    draw.text((info_x, current_y), "VILLAGE:", fill=zambian_green, font=label_font)
    village_text = application.village.upper()[:22]
    draw.text((info_x + label_width, current_y), village_text, fill=black, font=small_font)
    
    # District
    current_y += line_height
    draw.text((info_x, current_y), "DISTRICT:", fill=zambian_green, font=label_font)
    district_text = application.district.upper()[:22]
    draw.text((info_x + label_width, current_y), district_text, fill=black, font=small_font)
    
    # Chief
    current_y += line_height
    draw.text((info_x, current_y), "CHIEF:", fill=zambian_green, font=label_font)
    chief_text = application.chief_name.upper()[:22]
    draw.text((info_x + label_width, current_y), chief_text, fill=black, font=small_font)
    
    # Issue date
    current_y += line_height
    issue_date = datetime.now().strftime("%d/%m/%Y")
    draw.text((info_x, current_y), "ISSUED:", fill=zambian_green, font=label_font)
    draw.text((info_x + label_width, current_y), issue_date, fill=black, font=small_font)
    
    # Footer with gradient effect
    draw.rectangle([0, height-50, width, height], fill=zambian_green)
    footer_text = "Department of National Registration"
    try:
        bbox = draw.textbbox((0, 0), footer_text, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text((width//2 - text_width//2, height-30), footer_text, fill=white, font=small_font)
    except:
        draw.text((width//2, height-25), footer_text, fill=white, font=small_font)
    
    # Save front side
    front_filename = f"nrc_front_{application.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    front_path = os.path.join(nrc_dir, front_filename)
    img.save(front_path)
    
    return f"nrc_cards/{front_filename}"

def generate_back_side(application, nrc_number, width, height, nrc_dir):
    """Generate the back side of the NRC card"""
    # Create image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Colors
    zambian_green = (0, 166, 81)
    zambian_orange = (255, 130, 0)
    zambian_red = (222, 41, 16)
    black = (0, 0, 0)
    white = (255, 255, 255)
    light_gray = (240, 240, 240)
    
    # Get fonts
    title_font, header_font, text_font, small_font, label_font = get_fonts()
    
    # Draw header with flag colors
    draw.rectangle([0, 0, width, 50], fill=zambian_green)
    draw.rectangle([0, 50, width, 70], fill=zambian_orange)
    
    # Title
    title_text = "NATIONAL REGISTRATION CARD"
    try:
        bbox = draw.textbbox((0, 0), title_text, font=header_font)
        text_width = bbox[2] - bbox[0]
        draw.text((width//2 - text_width//2, 15), title_text, fill=white, font=header_font)
    except:
        draw.text((width//2, 25), title_text, fill=white, font=header_font)
    
    # Parent information section
    info_y = 110
    line_height = 45
    margin = 50
    
    # Mother's information box
    box_y = info_y
    draw.rectangle([margin-10, box_y-10, width-margin+10, box_y+160], fill=light_gray, outline=zambian_orange, width=2)
    draw.text((margin, box_y), "MOTHER'S INFORMATION", fill=zambian_orange, font=header_font)
    draw.text((margin, box_y + line_height), f"Name: {application.mother_full_name.upper()[:35]}", fill=black, font=text_font)
    draw.text((margin, box_y + line_height*1.7), f"Village: {application.mother_village.upper()[:30]}", fill=black, font=small_font)
    draw.text((margin, box_y + line_height*2.3), f"District: {application.mother_district.upper()[:30]}", fill=black, font=small_font)
    draw.text((margin, box_y + line_height*2.9), f"Chief: {application.mother_chief_name.upper()[:30]}", fill=black, font=small_font)
    
    # Father's information box
    box_y = info_y + 200
    draw.rectangle([margin-10, box_y-10, width-margin+10, box_y+160], fill=light_gray, outline=zambian_green, width=2)
    draw.text((margin, box_y), "FATHER'S INFORMATION", fill=zambian_green, font=header_font)
    draw.text((margin, box_y + line_height), f"Name: {application.father_full_name.upper()[:35]}", fill=black, font=text_font)
    draw.text((margin, box_y + line_height*1.7), f"Village: {application.father_village.upper()[:30]}", fill=black, font=small_font)
    draw.text((margin, box_y + line_height*2.3), f"District: {application.father_district.upper()[:30]}", fill=black, font=small_font)
    draw.text((margin, box_y + line_height*2.9), f"Chief: {application.father_chief_name.upper()[:30]}", fill=black, font=small_font)
    
    # NRC Number at bottom with background
    nrc_box_y = height - 100
    draw.rectangle([margin-10, nrc_box_y-10, width-margin+10, nrc_box_y+40], fill=zambian_red)
    nrc_text = f"NRC: {nrc_number}"
    try:
        bbox = draw.textbbox((0, 0), nrc_text, font=header_font)
        text_width = bbox[2] - bbox[0]
        draw.text((width//2 - text_width//2, nrc_box_y), nrc_text, fill=white, font=header_font)
    except:
        draw.text((width//2, nrc_box_y + 10), nrc_text, fill=white, font=header_font)
    
    # Footer
    draw.rectangle([0, height-40, width, height], fill=zambian_green)
    footer_text = "Ministry of Home Affairs - Republic of Zambia"
    try:
        bbox = draw.textbbox((0, 0), footer_text, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text((width//2 - text_width//2, height-25), footer_text, fill=white, font=small_font)
    except:
        draw.text((width//2, height-20), footer_text, fill=white, font=small_font)
    
    # Save back side
    back_filename = f"nrc_back_{application.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    back_path = os.path.join(nrc_dir, back_filename)
    img.save(back_path)
    
    return f"nrc_cards/{back_filename}"

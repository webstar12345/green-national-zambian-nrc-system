# Carousel Image Guide

## Overview
The carousel now uses actual images with a smooth sliding animation showing the contrast between manual and online NRC application processes.

## Current Setup

### Slide 1: People in Long Queue (Manual Process)
- **Image**: People waiting in a long queue
- **Current**: Using Unsplash placeholder
- **Message**: "The Old Way" - Shows problems with manual applications

### Slide 2: Person Using Laptop (Online Process)
- **Image**: Person using laptop/computer
- **Current**: Using Unsplash placeholder
- **Message**: "The Modern Way" - Shows benefits of online application

### Slide 3: Crowded Registration Office
- **Image**: Crowded office with people waiting
- **Current**: Using Unsplash placeholder
- **Message**: "Manual Process Challenges" - Highlights the problems

### Slide 4: Happy Person with Device
- **Image**: Happy person using smartphone/laptop
- **Current**: Using Unsplash placeholder
- **Message**: "Join 10,000+ Satisfied Users" - Call to action

## How to Add Your Own Images

### Step 1: Prepare Your Images

1. **Take or collect photos** showing:
   - People in queues at registration offices
   - People using computers/phones for online applications
   - Crowded registration offices
   - Happy users with devices

2. **Image specifications**:
   - **Format**: JPG or PNG
   - **Size**: 1200x600 pixels (recommended)
   - **Aspect Ratio**: 2:1 (landscape)
   - **File size**: Under 500KB for fast loading

### Step 2: Save Images

Create a folder structure:
```
static/
  images/
    carousel/
      queue-manual.jpg
      online-laptop.jpg
      crowded-office.jpg
      happy-user.jpg
```

### Step 3: Update the HTML

Open `templates/applications/home.html` and replace the image URLs:

**Slide 1** (Line ~99):
```html
<!-- Replace this: -->
<img src="https://images.unsplash.com/photo-1528605105345-5344ea20e269?w=1200&h=600&fit=crop"

<!-- With this: -->
<img src="{% static 'images/carousel/queue-manual.jpg' %}"
```

**Slide 2** (Line ~127):
```html
<!-- Replace this: -->
<img src="https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=1200&h=600&fit=crop"

<!-- With this: -->
<img src="{% static 'images/carousel/online-laptop.jpg' %}"
```

**Slide 3** (Line ~155):
```html
<!-- Replace this: -->
<img src="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=1200&h=600&fit=crop"

<!-- With this: -->
<img src="{% static 'images/carousel/crowded-office.jpg' %}"
```

**Slide 4** (Line ~183):
```html
<!-- Replace this: -->
<img src="https://images.unsplash.com/photo-1556761175-b413da4baf72?w=1200&h=600&fit=crop"

<!-- With this: -->
<img src="{% static 'images/carousel/happy-user.jpg' %}"
```

### Step 4: Collect Static Files

After adding your images, run:
```bash
python manage.py collectstatic
```

## Animation Features

✅ **Smooth Sliding** - Images slide horizontally  
✅ **Auto-play** - Changes every 5 seconds  
✅ **Manual Controls** - Previous/Next arrows  
✅ **Indicators** - Dots showing current slide  
✅ **Keyboard Navigation** - Arrow keys work  
✅ **Hover Pause** - Stops when hovering  
✅ **Mobile Responsive** - Works on all devices  

## Customization Options

### Change Slide Duration

Edit `static/js/animations.js` (line ~280):
```javascript
// Change from 5000 (5 seconds) to your preferred time
carouselInterval = setInterval(() => {
    nextSlide();
}, 5000); // Change this number (in milliseconds)
```

### Change Animation Speed

Edit `static/css/animations.css` (line ~360):
```css
.carousel-slide {
    transition: transform 0.6s ease-in-out; /* Change 0.6s to your preference */
}
```

### Adjust Image Overlay Opacity

In `templates/applications/home.html`, find the overlay divs and adjust:
```html
<!-- Dark overlay -->
<div class="absolute inset-0 bg-black bg-opacity-60"></div>
<!-- Change bg-opacity-60 to any value from 0-100 -->
```

## Image Sources

### Free Stock Photo Sites:
- **Unsplash**: https://unsplash.com/
- **Pexels**: https://www.pexels.com/
- **Pixabay**: https://pixabay.com/

### Search Terms:
- "people waiting in queue"
- "office queue"
- "person using laptop"
- "online application"
- "crowded office"
- "happy person with phone"
- "african office"
- "zambian people" (if available)

## Tips for Best Results

1. **Use high-quality images** - Clear, well-lit photos work best
2. **Consistent style** - Try to use images with similar lighting/tone
3. **Show real scenarios** - Authentic photos are more engaging
4. **Consider diversity** - Show different age groups and genders
5. **Optimize file size** - Compress images to improve loading speed
6. **Test on mobile** - Ensure images look good on small screens

## Troubleshooting

**Images not showing?**
- Check file paths are correct
- Run `python manage.py collectstatic`
- Clear browser cache (Ctrl+F5)

**Images loading slowly?**
- Compress images using tools like TinyPNG
- Reduce image dimensions to 1200x600
- Use JPG format instead of PNG

**Carousel not sliding?**
- Check browser console for JavaScript errors
- Ensure animations.js is loaded
- Refresh the page (Ctrl+F5)

---

**The carousel is now ready with placeholder images. Replace them with your own photos for a personalized experience!** 📸✨

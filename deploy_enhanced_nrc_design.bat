@echo off
echo ========================================
echo 🎨 DEPLOYING ENHANCED NRC CARD DESIGN
echo ========================================
echo.

echo 📋 Step 1: Testing enhanced NRC design...
python test_enhanced_nrc_design.py

echo.
echo 🔄 Step 2: Regenerating existing NRC cards with new design...
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
django.setup()

from applications.models import NRCApplication
from applications.nrc_generator import generate_nrc_card

print('🔄 Regenerating NRC cards with enhanced design...')
approved_apps = NRCApplication.objects.filter(status='approved')

for app in approved_apps:
    try:
        print(f'   Regenerating NRC for Application #{app.id:05d}...')
        front_path, back_path, nrc_number = generate_nrc_card(app)
        
        app.nrc_front_image = front_path
        app.nrc_back_image = back_path
        if not app.nrc_number:
            app.nrc_number = nrc_number
        app.save()
        
        print(f'   ✅ Updated: {app.nrc_number}')
    except Exception as e:
        print(f'   ❌ Error: {e}')

print('✅ All NRC cards regenerated with enhanced design!')
"

echo.
echo 📊 Step 3: Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ========================================
echo ✅ ENHANCED NRC DESIGN DEPLOYED
echo ========================================
echo.
echo 🎨 DESIGN ENHANCEMENTS:
echo    ✅ Professional Zambian flag colors (Green, Orange, Red, Black)
echo    ✅ Enhanced typography and field layouts
echo    ✅ Color-coded sections for better readability
echo    ✅ Official government styling with seals
echo    ✅ Professional gradient backgrounds
echo    ✅ Better visual hierarchy and spacing
echo.
echo 📱 TEMPLATE IMPROVEMENTS:
echo    ✅ Personal information summary cards
echo    ✅ Enhanced 3D flip card animations
echo    ✅ Security features showcase
echo    ✅ Keyboard shortcuts (Space, F, D keys)
echo    ✅ Print functionality for both sides
echo    ✅ Mobile-responsive design
echo    ✅ Enhanced download controls with animations
echo    ✅ Loading states and visual feedback
echo.
echo 🎯 USER EXPERIENCE:
echo    ✅ Clear detail presentation
echo    ✅ Professional government appearance
echo    ✅ Interactive card flipping
echo    ✅ Multiple download formats
echo    ✅ Keyboard accessibility
echo    ✅ Print-ready layouts
echo    ✅ Mobile-friendly interface
echo.
echo 🔗 ACCESS POINTS:
echo    - View NRC Card: /application/[ID]/nrc-card/
echo    - My Applications: /my-applications/
echo    - Application Detail: /application/[ID]/
echo.
echo 💡 FEATURES:
echo    - Click card to flip or use Space/F keys
echo    - Press D key to download both sides
echo    - Print button for physical copies
echo    - Right-click protection for security
echo    - Auto-demo on page load
echo.
pause
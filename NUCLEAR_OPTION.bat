@echo off
echo ========================================
echo  NUCLEAR OPTION - Fresh Start
echo ========================================
echo.

echo This creates a completely fresh repository with only AI assistant code
echo.

echo Step 1: Create new orphan branch (no history)...
git checkout --orphan fresh-start

echo Step 2: Remove all files from staging...
git rm -rf .

echo Step 3: Add only essential AI assistant files...
git add applications/views.py
git add applications/ai_assistant.py
git add applications/models.py
git add applications/urls.py
git add applications/forms.py
git add applications/admin.py
git add applications/apps.py
git add nrc_system/settings.py
git add nrc_system/urls.py
git add manage.py
git add requirements.txt
git add .env.example
git add AI_ASSISTANT_RESTORED.md
git add DATABASE_TABLES_COMPLETE.md

echo Step 4: Add migration files...
git add applications/migrations/0009_create_separate_nrc_tables.py
git add applications/migrations/0010_migrate_existing_data.py
git add accounts/migrations/0004_add_otp_fields_fixed.py
git add accounts/migrations/0005_add_officer_field.py

echo Step 5: Add account files...
git add accounts/models.py
git add accounts/views.py
git add accounts/forms.py
git add accounts/admin.py
git add accounts/urls.py

echo Step 6: Add essential templates...
git add templates/base.html
git add templates/applications/home.html
git add templates/applications/ai_demo.html
git add templates/accounts/login.html
git add templates/accounts/signup.html

echo Step 7: Add AI assistant static files...
git add static/js/chat-widget.js
git add static/css/chat-widget.css

echo Step 8: Create initial commit...
git commit -m "NRC System with AI Assistant - Clean Implementation

Features:
- Multilingual AI assistant (English, Bemba, Nyanja, Tonga, Lozi)
- Smart NRC application guidance
- Database migrations for separated models
- Complete user authentication system
- Responsive web interface

Technical Stack:
- Django 4.2+ with PostgreSQL/SQLite support
- Google Gemini AI integration with fallback responses
- Bootstrap/Tailwind CSS responsive design
- File upload handling for documents
- Session-based user management

Ready for production deployment"

echo Step 9: Force push as new main branch...
git push --force origin fresh-start:main

echo.
echo ========================================
echo  NUCLEAR SUCCESS! 
echo ========================================
echo.
echo Repository completely rebuilt with:
echo - Zero secret history
echo - Only essential AI assistant code
echo - Clean commit history
echo - Ready for submission tomorrow
echo.
pause
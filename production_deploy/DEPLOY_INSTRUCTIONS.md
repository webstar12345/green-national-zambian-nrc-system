# AI Assistant Deployment Instructions 
 
## Files to Upload to Production: 
 
1. applications/views.py - Contains restored AI functions 
2. applications/ai_assistant.py - AI assistant core functionality 
3. applications/models.py - Updated database models 
4. applications/migrations/0009_create_separate_nrc_tables.py 
5. applications/migrations/0010_migrate_existing_data.py 
6. static/js/chat-widget.js - AI chat interface 
7. static/css/chat-widget.css - AI chat styling 
8. templates/applications/ai_demo.html - AI demo page 
 
## Environment Variables Needed: 
 
Add to your production environment: 
GEMINI_API_KEY=your_gemini_api_key_here 
 
## After Upload: 
 
1. Run migrations: python manage.py migrate 
2. Collect static files: python manage.py collectstatic 
3. Restart your production server 
 
## AI Assistant Features: 
 
- Multilingual support (English, Bemba, Nyanja, Tonga, Lozi) 
- Smart NRC guidance with context-aware responses 
- Fallback system when API quota exceeded 
- Quick response suggestions 
- Session-based language preferences 

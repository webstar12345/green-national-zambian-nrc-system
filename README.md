# 🇿🇲 Zambian National Registration Card System

A comprehensive online platform for Zambian National Registration Card applications and management, built with Django and styled with Tailwind CSS using the colors of the Zambian flag.

## Features

### User Features
- **User Registration & Authentication**: Secure account creation and login system
- **NRC Applications**: Apply for new NRC or replacement of lost/damaged cards
- **Document Upload**: Upload required documents (Birth Certificate, Under Five Card, Old NRC) in PDF format
- **Application Tracking**: Monitor application status and progress
- **AI Assistant**: Multilingual chatbot powered by Google Gemini AI (English, Bemba, Nyanja, Tonga, Lozi)
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Admin Features
- **Admin Dashboard**: Overview of all applications with statistics
- **Application Management**: Review, approve, or reject applications
- **User Management**: Manage user accounts and information
- **Document Review**: View uploaded documents for verification
- **Status Updates**: Update application status with admin notes

### Required Information
- **Personal Details**: Village, date of birth, place of birth, chief name
- **Mother's Information**: Village, date of birth, place of birth, chief name
- **Father's Information**: Village, date of birth, place of birth, chief name
- **Documents**: Birth certificate, under five card, old NRC (for replacements)

## Technology Stack

- **Backend**: Python Django 4.2.7
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Database**: SQLite (development) / PostgreSQL (production)
- **File Handling**: Django file uploads with PDF support
- **Authentication**: Django's built-in authentication system
- **AI Integration**: Google Gemini AI for multilingual chat assistant
- **UI Framework**: Tailwind CSS with Zambian flag colors

## Color Scheme (Zambian Flag)
- **Green** (#00A651): Primary color for navigation and buttons
- **Orange** (#FF8200): Secondary color for accents
- **Red** (#DE2910): Used for status indicators
- **Black** (#000000): Footer and text elements

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Setup
1. **Clone or download the project files**

2. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Get your Gemini API key from https://makersuite.google.com/app/apikey
   - Add your API key to `.env`:
     ```
     GEMINI_API_KEY=your-api-key-here
     ```

3. **Run the setup script**:
   ```bash
   python setup.py
   ```
   This will:
   - Install all dependencies
   - Create database migrations
   - Apply migrations
   - Create a superuser account
   - Collect static files

4. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the application**:
   - Main site: http://127.0.0.1:8000
   - Admin panel: http://127.0.0.1:8000/admin

### Manual Setup (Alternative)
If the setup script doesn't work, follow these steps:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create and apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

5. **Run the server**:
   ```bash
   python manage.py runserver
   ```

## Usage

### For Citizens
1. **Create Account**: Register with your personal information
2. **Login**: Access your account dashboard
3. **Use AI Assistant**: 
   - Click the chat button in the bottom-right corner
   - Ask questions in English, Bemba, Nyanja, Tonga, or Lozi
   - Get instant help with NRC requirements and processes
   - Switch languages anytime using the language selector
4. **Apply for NRC**: 
   - Choose "New NRC" or "Replacement"
   - Fill in all required information
   - Upload required documents (PDF format)
   - Submit application
5. **Track Status**: Monitor your application progress

### For Administrators
1. **Access Admin Panel**: Login at `/admin/` with superuser credentials
2. **Dashboard**: View application statistics and recent submissions
3. **Review Applications**: 
   - View all applications at `/admin-dashboard/`
   - Click "Review" to examine application details
   - Approve or reject applications with notes
4. **Manage Users**: Handle user accounts and information

## File Structure

```
nrc_system/
├── accounts/                 # User authentication app
├── applications/            # NRC applications app
├── templates/              # HTML templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # Uploaded files
├── nrc_system/           # Main project settings
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
└── README.md           # This file
```

## Configuration

### Environment Variables
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key-here
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

### Database
- Development: SQLite (default)
- Production: Configure PostgreSQL in `settings.py`

### File Uploads
- Uploaded documents are stored in `media/documents/`
- Supported format: PDF only
- File size limits can be configured in Django settings

## Security Features

- CSRF protection on all forms
- User authentication required for applications
- Admin-only access to management features
- Secure file upload handling
- Input validation and sanitization

## Deployment

### Production Checklist
1. Set `DEBUG=False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving (nginx/Apache)
4. Configure media file serving
5. Set up HTTPS
6. Configure email backend for notifications
7. Set proper file permissions

### Environment Variables for Production
```
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com
GEMINI_API_KEY=your-gemini-api-key
```

## AI Assistant Features

The system includes an intelligent multilingual AI assistant powered by Google Gemini:

### Supported Languages
- **English**: Full support for all NRC-related queries
- **Bemba**: Native language support for Bemba speakers
- **Nyanja**: Native language support for Nyanja speakers
- **Tonga**: Native language support for Tonga speakers
- **Lozi**: Native language support for Lozi speakers

### Capabilities
- Answer questions about NRC requirements
- Guide users through the application process
- Explain document requirements
- Provide step-by-step instructions
- Switch languages mid-conversation
- Context-aware responses based on user queries

### Usage
1. Click the green chat button in the bottom-right corner
2. Select your preferred language from the dropdown
3. Type your question or click a quick response suggestion
4. Get instant, helpful responses in your chosen language
5. Switch languages anytime without losing conversation context

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For support or questions:
- Check the Django documentation
- Review the code comments
- Test with sample data

## License

This project is developed for the Republic of Zambia's National Registration Card system.

---

**Built with ❤️ for Zambia 🇿🇲**
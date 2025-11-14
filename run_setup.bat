@echo off
echo Zambian NRC System Setup
echo ========================

echo Installing dependencies...
pip install -r requirements.txt

echo Creating migrations...
python manage.py makemigrations

echo Applying migrations...
python manage.py migrate

echo Creating superuser (admin account)...
python manage.py createsuperuser

echo Setup complete!
echo.
echo To start the server, run: python manage.py runserver
echo Then open: http://127.0.0.1:8000
echo Admin panel: http://127.0.0.1:8000/admin
echo.
pause
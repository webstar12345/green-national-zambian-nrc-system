@echo off
echo Pushing PostgreSQL driver fix...
git add requirements.txt
git commit -m "Fix: Update to psycopg3 for Python 3.13 compatibility"
git push
echo.
echo Done! Render will auto-deploy with PostgreSQL support.
pause

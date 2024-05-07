@echo off
cd C:\Users\siana\OneDrive\Desktop\ExpertEcho\ExpertEcho
echo Activating virtual environment...
call venv\Scripts\activate

echo Installing required Python packages...
pip install -r requirements.txt

echo Running migrations...
python manage.py migrate

echo Starting Django development server...
python manage.py runserver

pause

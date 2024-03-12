@echo off

rem Creating virtual environment
virtualenv venv

rem Activating virtual environment
echo Activating virtual environment
call venv\Scripts\activate

rem Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo Something went wrong. Virtual environment is not activated. Nothing will be executed further. Please follow maual setup instructions
    @REM exit /b 1
) else (
    rem Install dependencies
    echo Running pip install --no-cache-dir -r requirements.txt
    pip install -r --no-cache-dir requirements.txt

    rem Change into the drone_management directory
    echo Changing into drone_management/
    cd drone_management

    rem Database setup
    echo Making migrations
    python manage.py makemigrations
    echo Migrating
    python manage.py migrate

    rem Starting development server
    echo Starting development server
    python manage.py runserver
)

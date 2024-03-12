
python -m venv venv # Creating virtual environment
# Linux or macOS
# Activating virtual environment on Linux or macOS
echo "source venv/bin/activate"
source venv/bin/activate

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then

    echo "Something went wrong. Virtual environment is not activated. Nothing will be executed further."
    # exit 1

else

    # Install dependencies
    echo "running pip install --no-cache-dir -r requirements.txt"
    pip install -r requirements.txt

    # Change into the drone_management directory
    echo "Changing into drone_management/"
    cd drone_management

    # Database setup
    echo "Making migrations"
    python manage.py makemigrations
    echo "Migrating"
    python manage.py migrate

    # Starting development server
    echo "Starting development server"
    python manage.py runserver
fi
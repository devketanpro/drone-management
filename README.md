# Drone_Assessment

### Tech stack

    - Python
    - Django
    - Django Rest Framework
    - Postgres
    - Celery and django-celery-beat (for tasks management)
    - Redis (for a message broker)


### Setup locally using docker
    - Docker must be installed on your system
    - Clone the repo using `git clone https://github.com/devketanpro/drone-management.git`
    - From the root directory run this command in terminal `make start`
    - Now you can access the application `http://localhost:8000/`
    - To run the test cases execute `make test` in another termial tab.
    - To load the initial data execute `make load_data`.


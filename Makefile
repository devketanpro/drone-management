migrate:
	docker exec drone_management python ./drone_management/manage.py migrate

migrations:
	docker exec drone_management python ./drone_management/manage.py makemigrations

start:
	docker compose up --build

test:
	docker exec drone_management python ./drone_management/manage.py test drones_api

load_data:
	docker exec drone_management python ./drone_management/manage.py preload_data

from celery import shared_task
from django.utils import timezone
from .models import Drone, BatteryLog

@shared_task
def battery_use_and_log():
    drones = Drone.objects.all()

    for drone in drones:
        # Simulation of gradual depletion of the drone
        if drone.battery_capacity > 0:
            if drone.state != 'IDLE':
                drone.battery_capacity -= 5
                drone.save()
        
        # Create a log entry after updating the drone status
        BatteryLog.objects.create(drone=drone, battery_capacity=drone.battery_capacity)

@shared_task
def recharge_batteries():
    drones = Drone.objects.all()
    for drone in drones:
        if drone.battery_capacity == 0: #Only recharge battery if it's depleted
            drone.battery_capacity = 100 # Recharge battery to full capacity
            drone.save()

STATES_ARR = ['IDLE', 'LOADING', 'LOADED', 'DELIVERING', 'DELIVERED', 'RETURNING']
STATES_N = len(STATES_ARR)
@shared_task
def change_drone_state():
    drones = Drone.objects.all()
    for drone in drones:
        if drone.state != 'IDLE': #Check if drone is in use
            index = STATES_ARR.index(drone.state)
            #Automatically update drone state such to the next state. The time intervals are in celery.py
            if drone.state == 'RETURNING':
                drone.state = STATES_ARR[0]
            else:
                if drone.state == 'DELIVERING':
                    drone.load_weight = 0.0
                    drone.medication_loaded.clear()
                drone.state = STATES_ARR[index + 1]
            drone.save()
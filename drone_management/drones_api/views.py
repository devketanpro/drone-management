from .models import Drone, BatteryLog
from django.db.models import Q
from .serializers import *
from rest_framework.generics import (ListAPIView, RetrieveAPIView,
                                      CreateAPIView, UpdateAPIView)

class BatteryStatus(RetrieveAPIView):
    """
    API endpoint to retrieve battery status of a drone.

    """
    serializer_class = BatteryStatusSerializer
    queryset = Drone.objects.prefetch_related('medication_loaded')
    lookup_field = 'id'


class RegisterDrone(CreateAPIView):
    """
    API endpoint to register a new drone.

    """
    serializer_class = DroneSerializer


class LoadMedication(UpdateAPIView):
    """
    API endpoint to load medication onto a drone.

    """
    serializer_class = LoadMedicationSerializer
    queryset = Drone.objects.prefetch_related('medication_loaded')
    lookup_field = 'id'


class UnAvailableDrone(ListAPIView):
    """
    API endpoint to retrieve unavailable drones.

    """
    serializer_class = DroneGetSerializer
    queryset = Drone.objects.filter(Q(load_weight__gt=0) | Q(battery_capacity__lt=25))


class AvailableDrone(ListAPIView):
    """
    API endpoint to retrieve available drones.

    """
    serializer_class = DroneGetSerializer
    queryset = Drone.objects.filter(state="IDLE", battery_capacity__gte=25).prefetch_related('medication_loaded')


class DroneLoadView(RetrieveAPIView):
    """
    API endpoint to retrieve details of a drone.

    """
    serializer_class = DroneGetSerializer
    lookup_field = 'id'
    queryset = Drone.objects.prefetch_related('medication_loaded')


class BatteryHistory(ListAPIView):
    """
    API endpoint to retrieve battery history of drones.

    """
    serializer_class = BatteryLogSerializer
    lookup_field = 'id'
    queryset = BatteryLog.objects.select_related('drone')

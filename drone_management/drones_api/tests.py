from django.test import TestCase
from .models import Medication, Drone, BatteryLog
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient
from .serializers import *


class MedicationTestCase(TestCase):
    def setUp(self):
        self.medication = Medication.objects.create(name="Med1", weight=50, code="ABC123")
    
    def test_medication_creation(self):
        self.assertEqual(self.medication.name, "Med1")
        self.assertEqual(self.medication.weight, 50)
        self.assertEqual(self.medication.code, "ABC123")


class DroneTestCase(TestCase):
    def setUp(self):
        self.medication = Medication.objects.create(name="Med1", weight=50, code="ABC123")
        self.drone = Drone.objects.create(serial_number="12345", model="L", weight_limit=100, battery_capacity=50)

    def test_drone_creation(self):
        self.assertEqual(self.drone.serial_number, "12345")
        self.assertEqual(self.drone.model, "L")
        self.assertEqual(self.drone.weight_limit, 100)
        self.assertEqual(self.drone.battery_capacity, 50)

    def test_drone_load_medication(self):
        # Test loading medication onto the drone
        self.assertTrue(self.drone.good_weight_and_sufficient_energy(self.medication))
        self.assertTrue(self.drone.load_medication(self.medication))
        self.assertEqual(self.drone.load_weight, 50)
        self.assertEqual(self.drone.medication_loaded.count(), 1)

    def test_drone_battery_log_creation(self):
        # Test creating a battery log entry for the drone
        battery_log = BatteryLog.objects.create(drone=self.drone, battery_capacity=40)
        self.assertEqual(battery_log.drone, self.drone)
        self.assertEqual(battery_log.battery_capacity, 40)


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.drone = Drone.objects.create(serial_number="12345", model="L", weight_limit=100, battery_capacity=50)

    def test_battery_status_api(self):
        url = reverse('battery_status', kwargs={'id': self.drone.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['serial_number'], self.drone.serial_number)

    def test_register_drone_api(self):
        data = {
            'serial_number': '67890',
            'model': 'M',
            'weight_limit': 200,
            'battery_capacity': 80
        }
        response = self.client.post(reverse('register_drone'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Drone.objects.count(), 2)

    def test_load_medication_api(self):
        medication = Medication.objects.create(name="Med1", weight=50, code="ABC123")
        data = {'medication_loaded': [medication.id]}
        url = reverse('load_medication', kwargs={'id': self.drone.id})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.drone.medication_loaded.exists())

    def test_unavailable_drone_api(self):
        response = self.client.get(reverse('unavailable_drones'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)  # Assuming no drones are loaded or have low battery initially

    def test_available_drone_api(self):
        response = self.client.get(reverse('available_drones'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Assuming only one drone is initially available

    def test_drone_load_view_api(self):
        url = reverse('drone_load', kwargs={'id': self.drone.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['serial_number'], self.drone.serial_number)

    def test_battery_history_api(self):
        url = reverse('battery_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)  # Assuming no battery logs initially

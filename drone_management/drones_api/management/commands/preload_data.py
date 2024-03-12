from django.core.management.base import BaseCommand
from drones_api.models import Drone, Medication
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Create default data for the application'

    def handle(self, *args, **options):
        # Create categories
        drone1 = Drone.objects.create(serial_number='Drone-1', model='M')
        drone2 = Drone.objects.create(serial_number='Drone-2', model='H')
        drone3 = Drone.objects.create(serial_number='Drone-3', model='M')
        drone4 = Drone.objects.create(serial_number='Drone-4', model='H')
        drone5 = Drone.objects.create(serial_number='Drone-5', model='M')
        drone6 = Drone.objects.create(serial_number='Drone-6', model='H')
        drone7 = Drone.objects.create(serial_number='Drone-7', model='M')
        drone8 = Drone.objects.create(serial_number='Drone-8', model='H')
        drone9 = Drone.objects.create(serial_number='Drone-9', model='M')
        drone10 = Drone.objects.create(serial_number='Drone-10', model='H')

        # Create medications with images and link to categories
        medication1 = Medication.objects.create(name='Gaviscon dual action liquid sachets', weight=150.0, code="MD-1")
        # medication1.image.save('gaviscon-dual-action-liquid-sachets.jpg', File(open('media/images/gaviscon-dual-action-liquid-sachets.jpg', 'rb')))
        medication2 = Medication.objects.create(name='Laxido', weight=80.0, code="MD-2")
        # medication2.image.save('laxido.jpg', File(open('media/images/laxido.jpg', 'rb')))
        medication3 = Medication.objects.create(name='Smecta 30s Sachets', weight=270.0, code="MD-3")
        # medication3.image.save('smecta-sachets-30s.jpg', File(open('media/images/smecta-sachets-30s.jpg', 'rb')))
        medication4 = Medication.objects.create(name='Med-lemon', weight=155.0, code="MD-4")
        # medication4.image.save('med-lemon.jpg', File(open('media/images/med-lemon.jpeg', 'rb')))

        self.stdout.write(self.style.SUCCESS('Default data created successfully'))

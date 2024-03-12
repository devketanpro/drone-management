from rest_framework import serializers
from .models import Drone, Medication, BatteryLog


class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ['id', 'serial_number', 'model', 'weight_limit', 'battery_capacity', 'state']

    def create(self, validated_data):
        medications_data = validated_data.pop('medication_loaded', [])
        drone = Drone.objects.create(**validated_data)
        for medication_data in medications_data:
            medication = Medication.objects.create(**medication_data)
            if drone.good_weight_and_sufficient_energy(medication):
                drone.state = 'LOADING'
                drone.medication_loaded.add(medication)
                drone.load_weight += medication.weight
        drone.save()
        
        return drone


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'name', 'weight', 'code', 'image']

    def create(self, validated_data):
        medication = Medication.objects.create(
            name=validated_data['name'],
            weight=validated_data['weight'],
            code=validated_data['code'],
            image=validated_data.get('image', None),
        )
        return medication


class BatteryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatteryLog
        fields = '__all__'

    def create(self, validated_data):
        log = BatteryLog.objects.create(**validated_data)
        return log


class DroneGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ['id', 'serial_number', 'model', 'weight_limit', 'battery_capacity', 'state', 'medication_loaded', 'load_weight']


class BatteryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ['id', 'battery_capacity', 'state', 'serial_number']


class LoadMedicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Drone
        fields = ['id', 'medication_loaded']

    def validate(self, data):
        medications = data.get('medication_loaded', [])
        total_weight = sum(medication.weight for medication in medications)
        capacity = self.instance.load_weight + total_weight
        if self.instance.battery_capacity < 25:
            raise serializers.ValidationError({'error': "Drone battery is low."})
        elif self.instance.weight_limit < capacity:
            raise serializers.ValidationError({'error': "Medication's weigth is more than drones capacity"})
        return data

from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator

class Medication(models.Model):
    name_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_-]*$',
        message='Sorry! Please use letters, numbers, hyphens, and underscores only.',
    )
    code_validator = RegexValidator(
        regex=r'^[A-Z0-9_-]*$',
        message='Sorry! Please use uppercase letters, numbers, and underscores only.',
    )
    
    name = models.CharField(max_length=100,validators=[name_validator])
    weight = models.FloatField(validators=[MaxValueValidator(100)])# 
    code = models.CharField(max_length=20, validators=[code_validator])# (allowed only upper case letters, underscore and numbers);
    image = models.ImageField(upload_to='images/') #(picture of the medication case).

class Drone(models.Model):
    MODELS = [
        ('L', 'Lightweight'), ('M', 'Middleweight'),
        ('C', 'Cruiserweight'), ('H', 'Heavyweight'),
    ]
    STATES = [
        ('IDLE', 'Idle'), ('LOADING', 'Loading'), ('LOADED', 'Loaded'),
        ('DELIVERING', 'Delivering'), ('DELIVERED', 'Delivered'), ('RETURNING', 'Returning'),
    ]

    serial_number = models.CharField(max_length=100)
    model = models.CharField(max_length=1, choices=MODELS, default='L') # Lightweight is the default
    weight_limit = models.FloatField(validators=[MaxValueValidator(500)], default=500.0)# limit (100gr max);
    battery_capacity = models.IntegerField(default=100, validators=[MaxValueValidator(100)],)#(percentage)
    state = models.CharField(max_length=10,choices=STATES,default='IDLE',) #(IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING).
    medication_loaded = models.ManyToManyField(Medication, related_name='medication_loaded', blank=True)
    load_weight = models.FloatField(default=0)

    def good_weight_and_sufficient_energy(self, medication):
        return (self.load_weight + medication.weight) <= self.weight_limit and self.battery_capacity >= 25

    def load_medication(self, medication):
        if not self.load_weight>0 and self.good_weight_and_sufficient_energy(medication):
            self.state = 'LOADING'
            self.save()
            self.medication_loaded.add(medication)
            self.load_weight += medication.weight
            self.save()
            return True
        else:
            return False

class BatteryLog(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    battery_capacity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
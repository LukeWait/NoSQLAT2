from django.db import models

# Create your models here.
'''
class ClimateData(models.Model):
    time = models.DateTimeField()
    device_id = models.CharField(max_length=50)
    device_name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    ttn_metadata = models.TextField()
    ttn_payload_fields = models.TextField()
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    atmospheric_pressure = models.DecimalField(max_digits=4, decimal_places=1)
    lightning_average_distance = models.DecimalField(max_digits=4, decimal_places=1)
    lightning_strike_count = models.IntegerField()
    maximum_wind_speed = models.DecimalField(max_digits=4, decimal_places=1)
    precipitation = models.DecimalField(max_digits=4, decimal_places=1)
    solar_radiation = models.DecimalField(max_digits=4, decimal_places=1)
    vapor_pressure = models.DecimalField(max_digits=4, decimal_places=1)
    humidity = models.DecimalField(max_digits=4, decimal_places=1)
    wind_direction = models.DecimalField(max_digits=4, decimal_places=1)
    wind_speed = models.DecimalField(max_digits=4, decimal_places=1)
'''
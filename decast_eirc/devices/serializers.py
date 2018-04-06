from rest_framework import serializers
from .models import EIRCDevice

class EIRCDeviceSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = EIRCDevice
    fields = '__all__'
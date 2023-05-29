from rest_framework import serializers
from .models import runTaskManage

class runTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = runTaskManage
        fields = '__all__'
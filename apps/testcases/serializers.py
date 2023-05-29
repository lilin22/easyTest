from rest_framework import serializers
from .models import testCasesKcpManage,testCasesKcpRun,testCasesOneManage,testCasesOneRun

class testCasesKcpSerializer(serializers.ModelSerializer):
    class Meta:
        model = testCasesKcpManage
        fields = '__all__'

class testCasesKcpRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = testCasesKcpRun
        fields = '__all__'

class testCasesOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = testCasesOneManage
        fields = '__all__'

class testCasesOneRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = testCasesOneRun
        fields = '__all__'
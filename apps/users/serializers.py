from rest_framework import serializers
from rest_framework_simplejwt.tokens import SlidingToken

# from .models import userProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class getTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print('get userTokenObtainPairSerializer')
        token = super().get_token(user)
        token['username'] = user.username
        token['code'] = 2000
        print(token)
        return token
    def validate(self, attrs):
        data = super().validate(attrs)
        re_data = {}
        re_data['data']=data
        re_data['code']=2000
        re_data['message']='success'
        return re_data

    # class Meta:
    #     model = userProfile
    #     fields = ('usename','password','token')

# class userSerializer(serializers.ModelSerializer):
#     # token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段
#     class Meta:
#         model = userProfile
#         fields = ('usename','password','token')

    # def create(self, validated_data):
    #     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    #     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    #     payload = jwt_payload_handler(userProfile)
    #     token = jwt_encode_handler(payload)
    #     userProfile.token = token
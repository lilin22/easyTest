from django.shortcuts import render
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
import json
from config import code_success,msg_success,code_fail,msg_fail
# from .models import userProfile
# from .serializers import userSerializer,userTokenObtainPairSerializer
from rest_framework.response import Response
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
import logging

vst_logger = logging.getLogger("visit")
svr_logger = logging.getLogger("server")

# Create your views here.
# class usersView(APIView):
#     '''用户列表'''
#
#     @csrf_exempt
#     def get(self,request,format=None):
#         upf = userProfile.objects.all()
#         us = userSerializer(upf, many=True)
#         return Response(us.data)
#
#     @csrf_exempt
#     def post(self,request,format=None):
#         dt = userSerializer(data=request.data)
#         name = request.data.get("username")
#         psw = request.data.get("password")
#         print(dt)
#         print(name)
#         upf = userProfile.objects.all()
#         us = userSerializer(upf, many=True)
#         return Response(us.data)
#
from users.serializers import getTokenObtainPairSerializer

class getTokenObtainPairView(TokenObtainPairView):
    # @csrf_exempt
    def __init__(self):
        serializer_class = getTokenObtainPairSerializer
        # Response.setHeader("Access-Control-Allow-Headers", "x-requested-with,Authorization,token, content-type")

class userSetPasswordView(APIView):
    '''修改密码'''
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        rqtdata = request.body
        tcrdata = json.loads(rqtdata)
        user = request.user
        old_password = tcrdata['old_password']
        new_password = tcrdata['new_password']
        repeat_password = tcrdata['repeat_password']
        vst_logger.info(user.username + "修改密码提交参数：" + json.dumps(tcrdata, ensure_ascii=False))
        if user.check_password(old_password):
            if not new_password:
                err_msg = '新密码不能为空'
            elif new_password != repeat_password:
                err_msg = '两次密码不一致'
            elif old_password == new_password == repeat_password:
                err_msg = '新密码与原密码一致'
            else:
                user.set_password(new_password)
                user.save()
                res_data = {}
                res_data['code'] = code_success
                res_data['message'] = msg_success
                vst_logger.info("修改密码返回内容：" + json.dumps(res_data, ensure_ascii=False))
                return Response(res_data)
        else:
            err_msg = '原密码输入错误'
        res_data = {}
        res_data['code'] = code_fail
        res_data['message'] = msg_fail
        res_data['err_msg'] = err_msg
        vst_logger.error("修改密码返回内容：" + json.dumps(res_data, ensure_ascii=False))
        return Response(res_data)
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import robotMsgManage
import json,requests
from config import code_success, msg_success,code_fail,msg_fail
import logging

vst_logger = logging.getLogger("visit")
svr_logger = logging.getLogger("server")

# Create your views here.

class robotSendMsgView(APIView):
    '''发送消息'''
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        res_data = {}
        projectId = request.data.get('projectId')
        msgtype = request.data.get('msgtype')
        content = request.data.get('content')

        vst_logger.info("发送消息参数：" + json.dumps(request.data, ensure_ascii=False))
        rmm = robotMsgManage.objects.filter(projectId=projectId).last()
        sendStatus = rmm.sendStatus
        if sendStatus == '1':
            robotUrl = rmm.robotUrl
            headers = {"Content-Type": "application/json"}
            data = {"msgtype": msgtype, "text": {"content": content}}
            vst_logger.info('发送消息通知请求参数：' + json.dumps(data, ensure_ascii=False))
            res = requests.post(url=robotUrl, headers=headers, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
            rsn = json.loads(res.text)
            if rsn['errcode'] == 0:
                vst_logger.info('发送消息通知成功，返回内容：' + res.text)
                res_data["code"] = code_success
                res_data["msg"] = msg_success
                return Response(res_data)
            else:
                vst_logger.error('发送消息通知失败，返回内容：' + res.text)
                res_data["code"] = code_fail
                res_data["msg"] = msg_fail
                return Response(res_data)
        else:
            res_data["code"] = code_fail
            res_data["msg"] = msg_fail + '，不发送消息'
            return Response(res_data)

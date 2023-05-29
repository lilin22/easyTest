from django.shortcuts import render
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from base.parseconf import parsekcpcf,parseonecf
import requests
import logging

# Create your views here.
vst_logger = logging.getLogger("visit")
svr_logger = logging.getLogger("server")

class appsDeteView(APIView):
    '''服务和设备在线检测'''
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        project_id = request.GET.get('project')
        # testBusServer = projectManage.objects.get(id=project_id).testBusServer
        if int(project_id) == 1:
            kcpCtlStatus = "false"
            allureStatus = "false"
            lgURL, username, password, appsDete_uri,kcpCtlAppId,allureDete_uri,sttURL = parsekcpcf(r'apps\common.conf')
            headers = {'Content-Type': 'application/json;charset=utf-8'}
            data = {"username": username, "password": password}
            vst_logger.info('kcpBridge登录请求参数：' + json.dumps(data, ensure_ascii=False))
            response = requests.post(url=lgURL, headers=headers,
                                     data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
            res = response.text
            res = json.loads(res)
            vst_logger.info('kcpBridge登录返回内容：' + json.dumps(res, ensure_ascii=False))
            if res['code'] == 2000:
                token = res['token']
                headers = {'token': token}
                params = {"appId":kcpCtlAppId}
                vst_logger.info('查询kcpCtl是否在线参数：' + json.dumps(params, ensure_ascii=False))
                response = requests.get(url=appsDete_uri, headers=headers,
                                        params=params)
                res = response.text
                res = json.loads(res)
                vst_logger.info('查询kcpCtl是否在线返回内容：' + json.dumps(res, ensure_ascii=False))
                if res['code'] == 2000 and res['onLine'] == "true":
                    kcpCtlStatus = "true"

                params = {"app": "allure"}
                vst_logger.info('查询allure是否在线参数：' + json.dumps(params, ensure_ascii=False))
                response = requests.get(url=allureDete_uri, headers=headers,
                                        params=params)
                res = response.text
                res = json.loads(res)
                vst_logger.info('查询allure是否在线返回内容：' + json.dumps(res, ensure_ascii=False))
                if res['code'] == 2000 and res['allureStatus'] == "true":
                    allureStatus = "true"


                res_data = {"code":2000,"msg":"操作成功","kcpCtlStatus":kcpCtlStatus,"allureStatus":allureStatus}
                vst_logger.info('查询kcp自动化测试服务是否在线返回内容汇总：' + json.dumps(res_data, ensure_ascii=False))
                return Response(res_data)
        elif int(project_id) == 2:
            oneCtlStatus = "false"
            allureStatus = "false"
            lgURL, username, password, appsDete_uri,oneCtlAppId,allureDete_uri,sttURL = parseonecf(r'apps\common.conf')
            headers = {'Content-Type': 'application/json;charset=utf-8'}
            data = {"username": username, "password": password}
            vst_logger.info('oneBridge登录请求参数：' + json.dumps(data, ensure_ascii=False))
            response = requests.post(url=lgURL, headers=headers,
                                     data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
            res = response.text
            res = json.loads(res)
            vst_logger.info('oneBridge登录返回内容：' + json.dumps(res, ensure_ascii=False))
            if res['code'] == 2000:
                token = res['token']
                headers = {'token': token}
                params = {"appId":oneCtlAppId}
                vst_logger.info('查询oneCtl是否在线参数：' + json.dumps(params, ensure_ascii=False))
                response = requests.get(url=appsDete_uri, headers=headers,
                                        params=params)
                res = response.text
                res = json.loads(res)
                vst_logger.info('查询oneCtl是否在线返回内容：' + json.dumps(res, ensure_ascii=False))
                if res['code'] == 2000 and res['onLine'] == "true":
                    oneCtlStatus = "true"

                params = {"app": "allure"}
                vst_logger.info('查询allure是否在线参数：' + json.dumps(params, ensure_ascii=False))
                response = requests.get(url=allureDete_uri, headers=headers,
                                        params=params)
                res = response.text
                res = json.loads(res)
                vst_logger.info('查询allure是否在线返回内容：' + json.dumps(res, ensure_ascii=False))
                if res['code'] == 2000 and res['allureStatus'] == "true":
                    allureStatus = "true"


                res_data = {"code":2000,"msg":"操作成功","oneCtlStatus":oneCtlStatus,"allureStatus":allureStatus}
                vst_logger.info('查询one自动化测试服务是否在线返回内容汇总：' + json.dumps(res_data, ensure_ascii=False))
                return Response(res_data)
        else:
            res_data = {"code": 6000, "msg": "不存在该项目，请联系管理员！"}
            return res_data

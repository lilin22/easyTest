import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from projects.models import projectManage
from .models import runTaskManage
from base.pagePagination import Pagination
from rest_framework import mixins,viewsets
from .filters import rtmFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from base.parseconf import parsekcpcf,parseonecf
from .serializers import runTaskSerializer
import logging

# Create your views here.
vst_logger = logging.getLogger("visit")
svr_logger = logging.getLogger("server")

class testRunStartView(APIView):
    '''启动测试任务'''
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        project_id = request.GET.get('project')
        # testBusServer = projectManage.objects.get(id=project_id).testBusServer
        if int(project_id) == 1:
            lgURL, username, password, appsDete_uri, kcpCtlAppId, allureDete_uri, sttURL = parsekcpcf(r'apps\common.conf')
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
                params = {'appId': 'b4ff3e1888dee3bc24c720a9fd2a7c816a0377822eb658b0ab37141d06d563b2'}
                vst_logger.info('查询kcpBridge是否有进行中的测试任务参数：' + json.dumps(params, ensure_ascii=False))
                response = requests.get(url=sttURL, headers=headers,
                                        params=params)
                res = response.text
                res = json.loads(res)
                vst_logger.info('查询kcpBridge是否有进行中的测试任务返回内容：' + json.dumps(res, ensure_ascii=False))
                return Response(res)
        elif int(project_id) == 2:
            lgURL, username, password, appsDete_uri, oneCtlAppId, allureDete_uri, sttURL = parseonecf(r'apps\common.conf')
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
                params = {'appId': 'b4ff3e1888dee3bc24c720a9fd2a7c816a0377822eb658b0ab37141d06d563b2'}
                vst_logger.info('查询oneBridge是否有进行中的测试任务参数：' + json.dumps(params, ensure_ascii=False))
                response = requests.get(url=sttURL, headers=headers,
                                        params=params)
                res = response.text
                res = json.loads(res)
                vst_logger.info('查询oneBridge是否有进行中的测试任务返回内容：' + json.dumps(res, ensure_ascii=False))
                return Response(res)
        else:
            res_data = {"code":6000,"msg":"操作失败，项目不存在"}
            return res_data

    def post(self, request, format=None):
        testTask_id = request.data.get('taskId')
        project_id = request.data.get('project_id')
        taskName = request.data.get('taskName')
        runFlag = request.data.get('runFlag')
        runMode = request.data.get('runMode')
        runNum = request.data.get('runNum')
        repeatMode = request.data.get('repeatMode')
        runTime = request.data.get('runTime')
        reRunFlag = request.data.get('reRunFlag')
        currentUser = request.user
        vst_logger.info(
            '用户【%s】启动项目ID为%d的测试任务：%s，状态：%s' % (currentUser.username, project_id, taskName, runFlag))
        if int(project_id) == 1:
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
                headers = {'Content-Type': 'application/json;charset=utf-8', 'token': token}
                currentUser = request.user
                data = {'project_id': project_id, 'testTask_id': testTask_id, 'taskName': taskName,
                        'opUser': currentUser.username, 'runFlag': runFlag,
                        'runMode': runMode, 'runNum': runNum, 'repeatMode': repeatMode,
                        'runTime': runTime, 'reRunFlag': reRunFlag}
                vst_logger.info('提交kcpBridge启动测试任务参数：' + json.dumps(data, ensure_ascii=False))
                response = requests.post(url=sttURL, headers=headers,
                                         data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
                res = response.text
                res = json.loads(res)
                vst_logger.info('kcpBridge接收测试任务返回内容：' + json.dumps(res, ensure_ascii=False))
                if res['code'] == 2000:
                    return Response(res)
                else:
                    return Response(res)
        elif int(project_id) == 2:
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
                headers = {'Content-Type': 'application/json;charset=utf-8', 'token': token}
                currentUser = request.user
                data = {'project_id': project_id, 'testTask_id': testTask_id, 'taskName': taskName,
                        'opUser': currentUser.username, 'runFlag': runFlag,
                        'runMode': runMode, 'runNum': runNum, 'repeatMode': repeatMode,
                        'runTime': runTime, 'reRunFlag': reRunFlag}
                vst_logger.info('提交oneBridge启动测试任务参数：' + json.dumps(data, ensure_ascii=False))
                response = requests.post(url=sttURL, headers=headers,
                                         data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
                res = response.text
                res = json.loads(res)
                vst_logger.info('oneBridge接收测试任务返回内容：' + json.dumps(res, ensure_ascii=False))
                if res['code'] == 2000:
                    return Response(res)
                else:
                    return Response(res)
        else:
            res_data = {"code": 6000, "msg": "操作失败，项目不存在"}
            return res_data
class runTestHistoryListViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.CreateModelMixin):
    '''测试任务列表'''
    permission_classes = (IsAuthenticated,)
    queryset = runTaskManage.objects.all()
    pagination_class = Pagination
    serializer_class = runTaskSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filter_class = rtmFilter
    search_fields = ('taskName','projectGroup_id','taskRunFlag','createTime',)
    # 配置排序
    ordering_fields = ('id','taskRunFlag','createTime',)

from django.shortcuts import render
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import kcpModulesManage,oneModulesManage
import logging

# Create your views here.
vst_logger = logging.getLogger("visit")
svr_logger = logging.getLogger("server")

class busModulesView(APIView):
    '''模块获取'''
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        project_id = request.GET.get('project')
        if int(project_id) == 1:
            modules = kcpModulesManage.objects.filter(status='1')
        elif int(project_id) == 2:
            modules = oneModulesManage.objects.filter(status='1')
        results = []
        for ms in modules:
            rs = {}
            rs["value"] = ms.id
            rs["label"] = ms.busmodule
            results.append(rs)
        res_data = {"code": 2000, "msg": "操作成功", "results": results}
        vst_logger.info('查询模块返回内容：' + json.dumps(res_data, ensure_ascii=False))
        return Response(res_data)

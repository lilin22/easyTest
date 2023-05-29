import json,pymysql
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from config import *
from projects.models import projectManage
from .serializers import testCasesKcpSerializer,testCasesKcpRunSerializer,testCasesOneSerializer,testCasesOneRunSerializer
from .models import testCasesKcpManage,testCasesKcpRun,testCasesOneManage,testCasesOneRun
from rest_framework.response import Response
from .filters import tcsKcpFilter,tcsOneFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import mixins,viewsets
from apps.base.pagePagination import Pagination
import logging
# Create your views here.

vst_logger = logging.getLogger("visit")
svr_logger = logging.getLogger("server")

class testCasesListKcpViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.CreateModelMixin):
    '''测试用例列表'''
    permission_classes = (IsAuthenticated,)
    queryset = testCasesKcpManage.objects.all()
    pagination_class = Pagination
    serializer_class = testCasesKcpSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filter_class = tcsKcpFilter
    search_fields = ('casename',)
    # 配置排序
    ordering_fields = ('id','caseNo','caseType','caseLevel','addTime','modifyTime')

class testCasesKcpSearchView(APIView):
    '''搜索测试用例'''
    permission_classes = (IsAuthenticated,)
    def post(self,request,format=None):
        vst_logger.info('搜索测试用例请求参数：' + json.dumps(request.data, ensure_ascii=False))
        project_id = request.data.get('project_id')
        busmodule = request.data.get('busmodule')
        caseNo = request.data.get('caseNo')
        casename = request.data.get('casename')
        caseType = request.data.get('caseType')
        caseLevel = request.data.get('caseLevel')
        status = request.data.get('status')
        # caseRunPlatform = request.data.get('caseRunPlatform')
        # pt = Pagination()
        res_data = {}
        data = []
        rdata = []
        if busmodule == []:
            for ct in caseType:
                # print(ct)
                for cl in caseLevel:
                    # for crp in caseRunPlatform:
                    tcsv = testCasesKcpManage.objects.filter(project_id=project_id, caseNo__icontains=caseNo,
                                                           casename__contains=casename, caseType=ct, caseLevel=cl,
                                                           status=status)
                    # print(tcsv)
                    tcser = testCasesKcpSerializer(tcsv, many=True)
                    # print(tcser)
                    if tcser.data != []:
                        data.append(tcser.data)
        else:
            for bm in busmodule:
                for ct in caseType:
                    for cl in caseLevel:
                        # for crp in caseRunPlatform:
                        tcsv = testCasesKcpManage.objects.filter(project_id=project_id, busmodule=bm,
                                                               caseNo__icontains=caseNo, casename__contains=casename,
                                                               caseType=ct, caseLevel=cl, status=status)
                        # print(tcsv)
                        tcser = testCasesKcpSerializer(tcsv, many=True)
                        # print(tcser)
                        if tcser.data != []:
                            data.append(tcser.data)
        for dt in data:
            # print(dt)
            for d in dt:
                # print(d)
                rdata.append(d)
        sortid_data = sorted(rdata,key = lambda c:c.__getitem__('id'))
        res_data['data'] = sortid_data
        res_data['code'] = code_success
        res_data['message'] = msg_success
        vst_logger.info('搜索测试用例返回内容：' + json.dumps(res_data, ensure_ascii=False))
        return Response(res_data)

class testCasesListOneViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.CreateModelMixin):
    '''测试用例列表'''
    permission_classes = (IsAuthenticated,)
    queryset = testCasesOneManage.objects.all()
    pagination_class = Pagination
    serializer_class = testCasesOneSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filter_class = tcsOneFilter
    search_fields = ('casename',)
    # 配置排序
    ordering_fields = ('id','caseNo','caseType','caseLevel','addTime','modifyTime')

class testCasesOneSearchView(APIView):
    '''搜索测试用例'''
    permission_classes = (IsAuthenticated,)
    def post(self,request,format=None):
        vst_logger.info('搜索测试用例请求参数：' + json.dumps(request.data, ensure_ascii=False))
        project_id = request.data.get('project_id')
        busmodule = request.data.get('busmodule')
        caseNo = request.data.get('caseNo')
        casename = request.data.get('casename')
        caseType = request.data.get('caseType')
        caseLevel = request.data.get('caseLevel')
        status = request.data.get('status')
        # caseRunPlatform = request.data.get('caseRunPlatform')
        # pt = Pagination()
        res_data = {}
        data = []
        rdata = []
        if busmodule == []:
            for ct in caseType:
                # print(ct)
                for cl in caseLevel:
                    # for crp in caseRunPlatform:
                    tcsv = testCasesOneManage.objects.filter(project_id=project_id, caseNo__icontains=caseNo,
                                                           casename__contains=casename, caseType=ct, caseLevel=cl,
                                                           status=status)
                    # print(tcsv)
                    tcser = testCasesOneSerializer(tcsv, many=True)
                    # print(tcser)
                    if tcser.data != []:
                        data.append(tcser.data)
        else:
            for bm in busmodule:
                for ct in caseType:
                    for cl in caseLevel:
                        # for crp in caseRunPlatform:
                        tcsv = testCasesOneManage.objects.filter(project_id=project_id, busmodule=bm,
                                                               caseNo__icontains=caseNo, casename__contains=casename,
                                                               caseType=ct, caseLevel=cl, status=status)
                        # print(tcsv)
                        tcser = testCasesOneSerializer(tcsv, many=True)
                        # print(tcser)
                        if tcser.data != []:
                            data.append(tcser.data)
        for dt in data:
            # print(dt)
            for d in dt:
                # print(d)
                rdata.append(d)
        sortid_data = sorted(rdata,key = lambda c:c.__getitem__('id'))
        res_data['data'] = sortid_data
        res_data['code'] = code_success
        res_data['message'] = msg_success
        vst_logger.info('搜索测试用例返回内容：' + json.dumps(res_data, ensure_ascii=False))
        return Response(res_data)

class testCasesRunView(APIView):
    '''测试用例执行列表'''
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        '''获取测试用例执行列表'''
        currentUser = request.user
        project_id = request.query_params['project_id']
        taskId = request.query_params['taskId']
        vst_logger.info("用户【%s】请求%s的用例执行列表" % (currentUser.username,project_id))
        if int(project_id) == 1:
            # tcr = testCaseHcRun.objects.all()
            tcr = testCasesKcpRun.objects.filter(taskId=taskId)
            tcrs = testCasesKcpRunSerializer(tcr,many=True)
            # print(tcrs.data)
            res_data = {}
            res_data['data'] = tcrs.data
            res_data['code'] = code_success
            res_data['message'] = msg_success
            vst_logger.info("请求用例执行列表返回内容：" + json.dumps(res_data, ensure_ascii=False))
            return Response(res_data)
        elif int(project_id) == 2:
            # tcr = testCaseHcRun.objects.all()
            tcr = testCasesOneRun.objects.filter(taskId=taskId)
            tcrs = testCasesOneRunSerializer(tcr,many=True)
            # print(tcrs.data)
            res_data = {}
            res_data['data'] = tcrs.data
            res_data['code'] = code_success
            res_data['message'] = msg_success
            vst_logger.info("请求用例执行列表返回内容：" + json.dumps(res_data, ensure_ascii=False))
            return Response(res_data)
        else:
            res_data = {"code":6000,"msg":"获取测试用例执行列表失败，请联系管理员"}
            return Response(res_data)

    def post(self,request,format=None):
        '''
        提交测试用例执行列表
        '''
        rqtdata = request.body
        tcrdata = json.loads(rqtdata)
        currentUser = request.user
        # print(currentUser.username)
        projectGroup_id = tcrdata['projectGroup']
        project_id = tcrdata['project']
        runType = tcrdata['runType']
        taskId = tcrdata['taskId']
        vst_logger.info("用户【%s】提交项目ID为%d的测试用例执行列表：%s" % (currentUser.username, project_id,tcrdata))
        if int(project_id) == 1:
            testCasesKcpRun.objects.filter(taskId__lte=taskId - 10).delete()
            # data = parsedbcf(r'apps\common.conf')
            # host = data['host']
            # username = data['username']
            # password = data['password']
            # dbname = data['dbname']
            # port = data['port']
            # # conn = sqlConct(host,username,password,dbname,port)
            # conn = pymysql.connect(host, username, password, dbname, port)
            # sql = "TRUNCATE TABLE testcases_" + caseRunList.lower()
            # truncateData(conn,sql)
            # sqlcls(conn)
            # testCaseHcRun.objects.all().delete()
            # rqtdata = request.body
            # tcrdata = json.loads(rqtdata)
            # print(testCaseHcRun)
            batchCases = []
            for tcr in tcrdata['data']:
                # print(tcr)
                # print(tcr['casename'])
                # tctdata = {}
                opUser = currentUser.username
                # cnid = testCaseCpManage.objects.get(casename=tcr['casename']).id
                # cnid = tcr['id']
                # projectGroup_id = testCaseCpManage.objects.get(id=cnid).projectGroup_id
                # project_id = testCaseCpManage.objects.get(id=cnid).project_id
                busmodule = tcr['busmodule']
                caseNo = tcr['caseNo']
                casename = tcr['casename']
                caseType = tcr['caseType']
                caseLevel = tcr['caseLevel']
                caseFile = tcr['caseFile']
                caseModule = tcr['caseModule']
                casePcFunction = tcr['casePcFunction']
                data = testCasesKcpRun(projectGroup_id=projectGroup_id,
                                   project_id=project_id,
                                   taskId=taskId,
                                   busmodule=busmodule,
                                   caseNo=caseNo,
                                   casename=casename,
                                   caseType=caseType,
                                   caseLevel=caseLevel,
                                   caseFile=caseFile,
                                   caseModule=caseModule,
                                   casePcFunction=casePcFunction,
                                   opUser=opUser,
                                   # casename_id=cnid,
                                   runType=runType)
                # data.save()
                batchCases.append(data)
            testCasesKcpRun.objects.bulk_create(batchCases)
            res_data = {}
            res_data['code'] = code_success
            res_data['runningTaskFlag'] = 'ture'
            res_data['message'] = msg_success
            vst_logger.info("提交测试用例执行列表返回内容：" + json.dumps(res_data,ensure_ascii=False))
            return Response(res_data)
        elif int(project_id) == 2:
            testCasesOneRun.objects.filter(taskId__lte=taskId - 10).delete()
            # data = parsedbcf(r'apps\common.conf')
            # host = data['host']
            # username = data['username']
            # password = data['password']
            # dbname = data['dbname']
            # port = data['port']
            # # conn = sqlConct(host,username,password,dbname,port)
            # conn = pymysql.connect(host, username, password, dbname, port)
            # sql = "TRUNCATE TABLE testcases_" + caseRunList.lower()
            # truncateData(conn,sql)
            # sqlcls(conn)
            # testCaseHcRun.objects.all().delete()
            # rqtdata = request.body
            # tcrdata = json.loads(rqtdata)
            # print(testCaseHcRun)
            batchCases = []
            for tcr in tcrdata['data']:
                # print(tcr)
                # print(tcr['casename'])
                # tctdata = {}
                opUser = currentUser.username
                # cnid = testCaseCpManage.objects.get(casename=tcr['casename']).id
                # cnid = tcr['id']
                # projectGroup_id = testCaseCpManage.objects.get(id=cnid).projectGroup_id
                # project_id = testCaseCpManage.objects.get(id=cnid).project_id
                busmodule = tcr['busmodule']
                caseNo = tcr['caseNo']
                casename = tcr['casename']
                caseType = tcr['caseType']
                caseLevel = tcr['caseLevel']
                caseFile = tcr['caseFile']
                caseModule = tcr['caseModule']
                casePcFunction = tcr['casePcFunction']
                data = testCasesOneRun(projectGroup_id=projectGroup_id,
                                   project_id=project_id,
                                   taskId=taskId,
                                   busmodule=busmodule,
                                   caseNo=caseNo,
                                   casename=casename,
                                   caseType=caseType,
                                   caseLevel=caseLevel,
                                   caseFile=caseFile,
                                   caseModule=caseModule,
                                   casePcFunction=casePcFunction,
                                   opUser=opUser,
                                   # casename_id=cnid,
                                   runType=runType)
                # data.save()
                batchCases.append(data)
            testCasesOneRun.objects.bulk_create(batchCases)
            res_data = {}
            res_data['code'] = code_success
            res_data['runningTaskFlag'] = 'ture'
            res_data['message'] = msg_success
            vst_logger.info("提交测试用例执行列表返回内容：" + json.dumps(res_data,ensure_ascii=False))
            return Response(res_data)
        else:
            res_data = {"code":6000,"message":"指定查询项目的用例执行列表不存在，请联系管理员"}
            vst_logger.error("提交测试用例执行列表返回内容：" + json.dumps(res_data,ensure_ascii=False))
            return Response(res_data)
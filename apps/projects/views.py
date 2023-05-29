import json

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from config import code_success, msg_success
from users.models import userProfile
from projects.models import projectGroupManage,projectManage
import logging
# Create your views here.
vst_logger = logging.getLogger("visit")
svr_logger = logging.getLogger("server")

class userProjectView(APIView):
    '''用户项目列表列表'''
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        '''根据用户获取所属项目组和项目列表'''
        currentUser = request.user
        vst_logger.info("用户【%s】请求所属项目组和项目列表" % (currentUser.username))
        # projectGroup_id = userProfile.objects.get(username=currentUser.username).projectGroup_id
        user = userProfile.objects.get(username=currentUser.username)
        data = []
        for i in range(0,len(user.projectGroup.all())):
            projectGroup_project = {}
            projectGroup_id = user.projectGroup.all()[i].id
            projectGroup = projectGroupManage.objects.get(id=projectGroup_id).projectGroup
            pm = projectManage.objects.filter(projectGroup_id=projectGroup_id,status="1")
            # print(list(pm))
            if list(pm) != []:
                projectGroup_project['projectGroup_id'] = projectGroup_id
                projectGroup_project['projectGroup'] = projectGroup
                dt = []
                for p in pm:
                    project = {"project_id":p.id,"project":p.project}
                    dt.append(project)
                    projectGroup_project['data'] = dt
                data.append(projectGroup_project)
        res_data = {}
        res_data['data'] = data
        res_data['code'] = code_success
        res_data['message'] = msg_success
        vst_logger.info("用户【" + currentUser.username + "】请求所属项目组和项目列表返回内容：" + json.dumps(res_data, ensure_ascii=False))
        return Response(res_data)
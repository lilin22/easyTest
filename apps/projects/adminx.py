import xadmin
from .models import projectGroupManage,projectManage

class pjtgmanage(object):
    list_display = ['projectGroup','addTime','modifyTime']

    model_icon = 'fa fa-pinterest-square'

class pjtmanage(object):
    list_display = ['project','projectGroup','status','addTime','modifyTime']

    model_icon = 'fa fa-pinterest'

xadmin.site.register(projectGroupManage,pjtgmanage)
xadmin.site.register(projectManage,pjtmanage)

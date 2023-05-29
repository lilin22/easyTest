from django.db import models
from projects.models import projectManage,projectGroupManage
from busModule.models import kcpModulesManage,oneModulesManage

# Create your models here.

class testCasesKcpManage(models.Model):
    '''kcp测试用例列表'''
    CASETYPE_CHOICES = {
        ('1', '冒烟测试'),
        ('2', '回归测试')
    }

    CASELEVEL_CHOICES = {
        ('1', '高'),
        ('2', '中'),
        ('3', '低')
    }

    TCSTATUS_CHOICES = {
        ('1', '启用'),
        ('0', '禁用')
    }

    busmodule = models.ForeignKey(kcpModulesManage,verbose_name='业务模块',on_delete=models.CASCADE)
    caseNo = models.CharField(verbose_name='用例编号', max_length=100,default="",unique=True)
    casename = models.CharField(verbose_name='用例标题', max_length=500)
    project = models.ForeignKey(projectManage, verbose_name='项目',on_delete=models.CASCADE)
    projectGroup = models.ForeignKey(projectGroupManage, verbose_name='项目组', on_delete=models.CASCADE)
    caseType = models.CharField(verbose_name='类型', max_length=10,choices=CASETYPE_CHOICES)
    caseLevel = models.CharField( verbose_name='等级',max_length=10,choices=CASELEVEL_CHOICES)
    caseFile = models.CharField(verbose_name='脚本文件', max_length=100)
    caseModule = models.CharField(verbose_name='类名', max_length=100,default="")
    casePcFunction = models.CharField(verbose_name='函数', max_length=100)
    status = models.CharField(verbose_name='状态', max_length=10,choices=TCSTATUS_CHOICES)
    addTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modifyTime = models.DateTimeField(verbose_name='更新时间',auto_now=True)

    class Meta:
        verbose_name = 'kcp测试用例'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.casename

class testCasesKcpRun(models.Model):
    '''kcp提交用例执行列表'''
    RUNTYPE_CHOICES = {
        ('1', '冒烟测试'),
        ('2', '全部')
    }
    taskId = models.IntegerField(verbose_name='任务Id', default=0)
    busmodule = models.CharField(verbose_name='业务模块', max_length=500)
    caseNo = models.CharField(verbose_name='用例编号', max_length=100,default="")
    casename = models.CharField(verbose_name='用例标题', max_length=500,default="")
    projectGroup = models.ForeignKey(projectGroupManage, verbose_name='项目组', on_delete=models.CASCADE, default="")
    project = models.ForeignKey(projectManage, verbose_name='项目', on_delete=models.CASCADE, default="")
    caseType = models.CharField(verbose_name='用例类型', max_length=50)
    caseLevel = models.CharField(verbose_name='用例等级', max_length=50)
    caseFile = models.CharField(verbose_name='脚本文件', max_length=100)
    caseModule = models.CharField(verbose_name='类名', max_length=100,default="")
    casePcFunction = models.CharField(verbose_name='函数', max_length=100)
    runType = models.CharField(verbose_name='执行类型', max_length=10,choices=RUNTYPE_CHOICES, default='2')
    opUser = models.CharField(verbose_name='操作用户', max_length=50)
    addTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '用例执行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.casename.casename

class testCasesOneManage(models.Model):
    '''one测试用例列表'''
    CASETYPE_CHOICES = {
        ('1', '冒烟测试'),
        ('2', '回归测试')
    }

    CASELEVEL_CHOICES = {
        ('1', '高'),
        ('2', '中'),
        ('3', '低')
    }

    TCSTATUS_CHOICES = {
        ('1', '启用'),
        ('0', '禁用')
    }

    busmodule = models.ForeignKey(oneModulesManage,verbose_name='业务模块',on_delete=models.CASCADE)
    caseNo = models.CharField(verbose_name='用例编号', max_length=100,default="",unique=True)
    casename = models.CharField(verbose_name='用例标题', max_length=500)
    project = models.ForeignKey(projectManage, verbose_name='项目',on_delete=models.CASCADE)
    projectGroup = models.ForeignKey(projectGroupManage, verbose_name='项目组', on_delete=models.CASCADE)
    caseType = models.CharField(verbose_name='类型', max_length=10,choices=CASETYPE_CHOICES)
    caseLevel = models.CharField( verbose_name='等级',max_length=10,choices=CASELEVEL_CHOICES)
    caseFile = models.CharField(verbose_name='脚本文件', max_length=100)
    caseModule = models.CharField(verbose_name='类名', max_length=100,default="")
    casePcFunction = models.CharField(verbose_name='函数', max_length=100)
    status = models.CharField(verbose_name='状态', max_length=10,choices=TCSTATUS_CHOICES)
    addTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modifyTime = models.DateTimeField(verbose_name='更新时间',auto_now=True)

    class Meta:
        verbose_name = 'one测试用例'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.casename

class testCasesOneRun(models.Model):
    '''one提交用例执行列表'''
    RUNTYPE_CHOICES = {
        ('1', '冒烟测试'),
        ('2', '全部')
    }
    taskId = models.IntegerField(verbose_name='任务Id', default=0)
    busmodule = models.CharField(verbose_name='业务模块', max_length=500)
    caseNo = models.CharField(verbose_name='用例编号', max_length=100,default="")
    casename = models.CharField(verbose_name='用例标题', max_length=500,default="")
    projectGroup = models.ForeignKey(projectGroupManage, verbose_name='项目组', on_delete=models.CASCADE, default="")
    project = models.ForeignKey(projectManage, verbose_name='项目', on_delete=models.CASCADE, default="")
    caseType = models.CharField(verbose_name='用例类型', max_length=50)
    caseLevel = models.CharField(verbose_name='用例等级', max_length=50)
    caseFile = models.CharField(verbose_name='脚本文件', max_length=100)
    caseModule = models.CharField(verbose_name='类名', max_length=100,default="")
    casePcFunction = models.CharField(verbose_name='函数', max_length=100)
    runType = models.CharField(verbose_name='执行类型', max_length=10,choices=RUNTYPE_CHOICES, default='2')
    opUser = models.CharField(verbose_name='操作用户', max_length=50)
    addTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '用例执行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.casename.casename
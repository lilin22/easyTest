from django.db import models

# Create your models here.
class runTaskManage(models.Model):
    taskName = models.CharField(verbose_name='任务名称', max_length=200,null=True,blank=True)
    casesTotal = models.CharField(verbose_name='用例数', max_length=20, null=True, blank=True)
    projectGroup_id = models.IntegerField(verbose_name='项目组',null=True,blank=True)
    project_id = models.IntegerField(verbose_name='项目',null=True, blank=True)
    taskRunFlag = models.CharField(verbose_name='任务状态', max_length=10,null=True,blank=True)
    optUser = models.CharField(verbose_name='操作人', max_length=10,null=True,blank=True)
    runMode = models.CharField(verbose_name='运行模式', max_length=10, null=True, blank=True)
    runNum = models.IntegerField(verbose_name='次数',null=True,blank=True)
    runTime = models.CharField(verbose_name='运行时间', max_length=50, null=True, blank=True)
    reRunFlag = models.CharField(verbose_name='是否失败重跑', max_length=50, null=True, blank=True)
    successedTotal = models.IntegerField(verbose_name='成功用例数', default=0)
    failedTotal = models.IntegerField(verbose_name='失败用例数', default=0)
    pendingTotal = models.IntegerField(verbose_name='待执行用例数', default=0)
    process = models.CharField(verbose_name='进度', max_length=50, default="0.00%")
    ratio = models.CharField(verbose_name='通过率', max_length=50, null=True, blank=True)
    isDisplayReRun = models.CharField(verbose_name='是否显示失败重跑', max_length=50, null=True, blank=True)
    createTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modifyTime = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = '任务列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.taskName
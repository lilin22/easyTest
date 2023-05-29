from django.db import models

# Create your models here.
class projectGroupManage(models.Model):
    '''项目组列表'''
    projectGroup = models.CharField(verbose_name='项目组', max_length=20,default='')
    addTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modifyTime = models.DateTimeField(verbose_name='更新时间',auto_now=True)

    class Meta:
        verbose_name = '项目组列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.projectGroup

class projectManage(models.Model):
    '''项目列表'''
    PJTSTATUS_CHOICES = {
        ('1', '启用'),
        ('0', '禁用')
    }

    project = models.CharField(verbose_name='项目', max_length=50,default='')
    projectGroup = models.ForeignKey(projectGroupManage, verbose_name='项目组',on_delete=models.CASCADE, default="")
    status = models.CharField(verbose_name='状态', max_length=10,choices=PJTSTATUS_CHOICES, default='1')
    addTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modifyTime = models.DateTimeField(verbose_name='更新时间',auto_now=True)

    class Meta:
        verbose_name = '项目列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project
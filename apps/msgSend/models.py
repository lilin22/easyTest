from django.db import models
from projects.models import projectManage

# Create your models here.

class robotMsgManage(models.Model):
    '''消息管理'''
    STATUS_CHOICES = {
        ('1', '启用'),
        ('0', '禁用')
    }

    SENDSTATUS_CHOICES = {
        ('1', '发送'),
        ('0', '不发送')
    }

    robotUrl = models.CharField(verbose_name='机器人URL', max_length=500, default='')
    projectId = models.ForeignKey(projectManage, verbose_name='项目', on_delete=models.CASCADE, default='')
    status = models.CharField(verbose_name='状态', max_length=10, choices=STATUS_CHOICES, default='1')
    sendStatus = models.CharField(verbose_name='是否发送', max_length=10, choices=SENDSTATUS_CHOICES, default='1')
    createTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updateTime = models.DateTimeField(verbose_name='更新时间', auto_now_add=True)

    class Meta:
        verbose_name = '机器人消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.status

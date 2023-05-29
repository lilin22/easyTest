from django.db import models

# Create your models here.
class kcpModulesManage(models.Model):
    STATUS_CHOICES = {
        ('1', '启用'),
        ('0', '禁用')
    }

    busmodule = models.CharField(verbose_name='业务模块', max_length=500, default='')
    status = models.CharField(verbose_name='状态', max_length=10, choices=STATUS_CHOICES, default='1')
    createTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updateTime = models.DateTimeField(verbose_name='更新时间', auto_now_add=True)

    class Meta:
        verbose_name = 'kcp'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.busmodule
    
class oneModulesManage(models.Model):
    STATUS_CHOICES = {
        ('1', '启用'),
        ('0', '禁用')
    }

    busmodule = models.CharField(verbose_name='业务模块', max_length=500, default='')
    status = models.CharField(verbose_name='状态', max_length=10, choices=STATUS_CHOICES, default='1')
    createTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updateTime = models.DateTimeField(verbose_name='更新时间', auto_now_add=True)

    class Meta:
        verbose_name = 'one'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.busmodule

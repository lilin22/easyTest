from django.contrib.auth.models import AbstractUser
from django.db import models
from projects.models import projectGroupManage

# Create your models here.
class userProfile(AbstractUser):
    phone = models.CharField(verbose_name='手机号码',max_length=20,null=True,blank=True)
    projectGroup = models.ManyToManyField(projectGroupManage, verbose_name='项目组',null=True,blank=True)
    # projectGroup = models.ForeignKey(projectGroupManage, verbose_name='项目组', on_delete=models.CASCADE, null=True,blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
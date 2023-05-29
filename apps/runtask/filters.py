import django_filters
from .models import runTaskManage

class rtmFilter(django_filters.rest_framework.FilterSet):
    id = django_filters.NumberFilter(field_name='id', lookup_expr='exact')
    projectGroup_id = django_filters.NumberFilter(field_name='projectGroup_id',lookup_expr='exact')
    project_id = django_filters.NumberFilter(field_name='project_id',lookup_expr='exact')
    taskName = django_filters.CharFilter(field_name='taskName', lookup_expr='icontains')
    casesTotal = django_filters.NumberFilter(field_name='casesTotal', lookup_expr='exact')
    optUser = django_filters.CharFilter(field_name='optUser', lookup_expr='exact')
    taskRunFlag = django_filters.CharFilter(field_name='taskRunFlag', lookup_expr='exact')
    timeZone = django_filters.CharFilter(field_name='timeZone', lookup_expr='exact')
    appId = django_filters.CharFilter(field_name='appId', lookup_expr='exact')
    mcd = django_filters.CharFilter(field_name='mcd', lookup_expr='exact')
    createTime = django_filters.CharFilter(field_name='createTime',lookup_expr='icontains')

    class Meta:
        model = runTaskManage
        fields = ['id','projectGroup_id','project_id','taskName','casesTotal','optUser','taskRunFlag','timeZone','appId','mcd','createTime']
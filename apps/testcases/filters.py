import django_filters
from .models import testCasesKcpManage,testCasesOneManage

class tcsKcpFilter(django_filters.rest_framework.FilterSet):
    projectGroup = django_filters.NumberFilter(field_name='projectGroup_id',lookup_expr='exact')
    project = django_filters.NumberFilter(field_name='project_id',lookup_expr='exact')
    caseNo = django_filters.CharFilter(field_name='caseNo', lookup_expr='exact')
    casename = django_filters.CharFilter(field_name='casename',lookup_expr='icontains')
    caseType = django_filters.CharFilter(field_name='caseType', lookup_expr='exact')
    caseFile = django_filters.CharFilter(field_name='caseFile', lookup_expr='exact')
    caseModule = django_filters.CharFilter(field_name='caseModule', lookup_expr='icontains')
    casePcFunction = django_filters.CharFilter(field_name='casePcFunction', lookup_expr='exact')
    caseLevel = django_filters.CharFilter(field_name='caseLevel', lookup_expr='exact')
    status = django_filters.CharFilter(field_name='status',lookup_expr='exact')

    class Meta:
        model = testCasesKcpManage
        fields = ['projectGroup','project','casename', 'caseType', 'caseLevel', 'caseFile','casePcFunction','status']
        
class tcsOneFilter(django_filters.rest_framework.FilterSet):
    projectGroup = django_filters.NumberFilter(field_name='projectGroup_id',lookup_expr='exact')
    project = django_filters.NumberFilter(field_name='project_id',lookup_expr='exact')
    caseNo = django_filters.CharFilter(field_name='caseNo', lookup_expr='exact')
    casename = django_filters.CharFilter(field_name='casename',lookup_expr='icontains')
    caseType = django_filters.CharFilter(field_name='caseType', lookup_expr='exact')
    caseFile = django_filters.CharFilter(field_name='caseFile', lookup_expr='exact')
    caseModule = django_filters.CharFilter(field_name='caseModule', lookup_expr='icontains')
    casePcFunction = django_filters.CharFilter(field_name='casePcFunction', lookup_expr='exact')
    caseLevel = django_filters.CharFilter(field_name='caseLevel', lookup_expr='exact')
    status = django_filters.CharFilter(field_name='status',lookup_expr='exact')

    class Meta:
        model = testCasesOneManage
        fields = ['projectGroup','project','casename', 'caseType', 'caseLevel', 'caseFile','casePcFunction','status']
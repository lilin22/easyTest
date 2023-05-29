import xadmin
from .models import testCasesKcpManage,testCasesOneManage
from import_export import resources
from django.apps import apps

class testCasesKcpManageResource(resources.ModelResource):
    # def __init__(self):
    #     super(testCaseCpManageResource, self).__init__()
    #     field_list = apps.get_model('testcases', 'testCaseCpManage')._meta.fields
    #     # field_list = testCaseCpManage._meta.fields
    #     # 应用名与模型名
    #     self.verbose_name_dict = {}
    #     self.fkey = []
    #     # 获取所有字段的verbose_name并存放在verbose_name_dict字典里
    #     for i in field_list:
    #         self.verbose_name_dict[i.name] = i.verbose_name
    #         if(isinstance(i,ForeignKey)):
    #             self.fkey.append(i.name)
    #     # print(self.verbose_name_dict)
    #
    # # 重载resources.py的export方法，修改将要导出的data的某些外键相关数据。默认导出外键id，这里修改为导出外键对应的值
    # def export(self, queryset=None, *args, **kwargs):
    #     self.before_export(queryset, *args, **kwargs)
    #
    #     if queryset is None:
    #         queryset = self.get_queryset()
    #     headers = self.get_export_headers()
    #     data = tablib.Dataset(headers=headers)
    #
    #     # --------------------- #
    #     # 获取所有外键名称在headers中的位置
    #     fk_index = {}
    #     for fk in self.fkey:
    #         fk_index[fk] = headers.index(self.vname_dict[fk])
    #     # --------------------- #
    #
    #     if isinstance(queryset, QuerySet):
    #         # Iterate without the queryset cache, to avoid wasting memory when
    #         # exporting large datasets.
    #         iterable = queryset.iterator()
    #     else:
    #         iterable = queryset
    #     for obj in iterable:
    #         # --------------------- #
    #         # 获取将要导出的源数据，这里export_resource返回的是列表，便于更改。替换到外键的值
    #         res = self.export_resource(obj)
    #         res[fk_index['project']] = projectManage.objects.get(id=res[fk_index['project']]).project
    #         res[fk_index['projectGroup']] = projectGroupManage.objects.get(id=res[fk_index['projectGroup']]).projectGroup
    #         data.append(res)
    #         # --------------------- #
    #     self.after_export(queryset, data, *args, **kwargs)
    #     return data
    #
    # def get_export_fields(self):
    #     fields = self.get_fields()
    #     # print("111")
    #     # print(fields)
    #     # 默认导入导出field的column_name为字段的名称
    #     # 这里修改为字段的verbose_name
    #     for field in fields:
    #         # print(222)
    #         # print(field)
    #         field_name = self.get_field_name(field)
    #         # print(field_name)
    #         if field_name in self.verbose_name_dict.keys():
    #             field.column_name = self.verbose_name_dict[field_name]
    #             # 如果设置过verbose_name，则将column_name替换为verbose_name
    #             # 否则维持原有的字段名
    #     print(fields)
    #     return fields
    def __init__(self):
        super(testCasesKcpManageResource,self).__init__()
        # 应用名与模型名
        field_list = apps.get_model('testcases','testCasesKcpManage')._meta.fields
        # field_list = testCaseCpManage._meta.fields
        # print(field_list)
        # 获取所有字段的verbose_name并存放在verbose_name_dict字典里
        self.verbose_name_dict = {}
        for i in field_list:
            self.verbose_name_dict[i.name] = i.verbose_name

    def get_export_fields(self):
        # 默认导入导出field的column_name为字段的名称
        # 这里修改为字段的verbose_name
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            if field_name in self.verbose_name_dict.keys():
                # 如果设置过verbose_name，则将column_name替换为verbose_name,否则维持原有的字段名
                field.column_name = self.verbose_name_dict[field_name]
        return fields

    class Meta:
        model = testCasesKcpManage
        # 导入数据时，如果该条数据未修改过，则会忽略
        skip_unchanged = True
        # 在导入预览页面中显示跳过的记录
        report_skipped = True
        # 对象标识的默认字段是id，您可以选择在导入时设置哪些字段用作id
        import_id_fields = ('id',)

        # 白名单
        fields = ('id','caseNo','busmodule','casename','project','projectGroup','caseType','caseLevel','caseFile','caseModule','casePcFunction','status',)
        # 黑名单
        exclude = ('addTime','modifyTime',)

class tcKcpmanage(object):
    # import_excel = True

    # def post(self, request, *args, **kwargs):
    #     #  导入逻辑
    #     if 'excel' in request.FILES:
    #         pass  # 此处是一系列的操作接口, 通过  request.FILES 拿到数据随意操作
    #     return super(testCaseCpManage, self).post(request, args, kwargs)  # 此返回值必须是这样


    # ordering = ['id']
    list_display = ['caseNo','busmodule','casename','project','projectGroup','caseType','caseLevel','caseFile','caseModule','casePcFunction','status','addTime','modifyTime']
    search_fields = ['caseNo','casename','caseFile','caseModule','casePcFunction']
    list_editable = ['caseNo','busmodule','caseNo','casename','project','projectGroup','caseType','caseLevel','caseFile','caseModule','casePcFunction','status']
    # 分页
    list_per_page = 10
    # 配置模型图标，也可以在GlobalSetting里面配置
    model_icon = 'fa fa-star'

    # 配置导入按钮
    import_export_args = {
        'import_resource_class': testCasesKcpManageResource,
        'export_resource_class': testCasesKcpManageResource
    }

class testCasesOneManageResource(resources.ModelResource):
    # def __init__(self):
    #     super(testCaseCpManageResource, self).__init__()
    #     field_list = apps.get_model('testcases', 'testCaseCpManage')._meta.fields
    #     # field_list = testCaseCpManage._meta.fields
    #     # 应用名与模型名
    #     self.verbose_name_dict = {}
    #     self.fkey = []
    #     # 获取所有字段的verbose_name并存放在verbose_name_dict字典里
    #     for i in field_list:
    #         self.verbose_name_dict[i.name] = i.verbose_name
    #         if(isinstance(i,ForeignKey)):
    #             self.fkey.append(i.name)
    #     # print(self.verbose_name_dict)
    #
    # # 重载resources.py的export方法，修改将要导出的data的某些外键相关数据。默认导出外键id，这里修改为导出外键对应的值
    # def export(self, queryset=None, *args, **kwargs):
    #     self.before_export(queryset, *args, **kwargs)
    #
    #     if queryset is None:
    #         queryset = self.get_queryset()
    #     headers = self.get_export_headers()
    #     data = tablib.Dataset(headers=headers)
    #
    #     # --------------------- #
    #     # 获取所有外键名称在headers中的位置
    #     fk_index = {}
    #     for fk in self.fkey:
    #         fk_index[fk] = headers.index(self.vname_dict[fk])
    #     # --------------------- #
    #
    #     if isinstance(queryset, QuerySet):
    #         # Iterate without the queryset cache, to avoid wasting memory when
    #         # exporting large datasets.
    #         iterable = queryset.iterator()
    #     else:
    #         iterable = queryset
    #     for obj in iterable:
    #         # --------------------- #
    #         # 获取将要导出的源数据，这里export_resource返回的是列表，便于更改。替换到外键的值
    #         res = self.export_resource(obj)
    #         res[fk_index['project']] = projectManage.objects.get(id=res[fk_index['project']]).project
    #         res[fk_index['projectGroup']] = projectGroupManage.objects.get(id=res[fk_index['projectGroup']]).projectGroup
    #         data.append(res)
    #         # --------------------- #
    #     self.after_export(queryset, data, *args, **kwargs)
    #     return data
    #
    # def get_export_fields(self):
    #     fields = self.get_fields()
    #     # print("111")
    #     # print(fields)
    #     # 默认导入导出field的column_name为字段的名称
    #     # 这里修改为字段的verbose_name
    #     for field in fields:
    #         # print(222)
    #         # print(field)
    #         field_name = self.get_field_name(field)
    #         # print(field_name)
    #         if field_name in self.verbose_name_dict.keys():
    #             field.column_name = self.verbose_name_dict[field_name]
    #             # 如果设置过verbose_name，则将column_name替换为verbose_name
    #             # 否则维持原有的字段名
    #     print(fields)
    #     return fields
    def __init__(self):
        super(testCasesOneManageResource,self).__init__()
        # 应用名与模型名
        field_list = apps.get_model('testcases','testCasesOneManage')._meta.fields
        # field_list = testCaseCpManage._meta.fields
        # print(field_list)
        # 获取所有字段的verbose_name并存放在verbose_name_dict字典里
        self.verbose_name_dict = {}
        for i in field_list:
            self.verbose_name_dict[i.name] = i.verbose_name

    def get_export_fields(self):
        # 默认导入导出field的column_name为字段的名称
        # 这里修改为字段的verbose_name
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            if field_name in self.verbose_name_dict.keys():
                # 如果设置过verbose_name，则将column_name替换为verbose_name,否则维持原有的字段名
                field.column_name = self.verbose_name_dict[field_name]
        return fields

    class Meta:
        model = testCasesOneManage
        # 导入数据时，如果该条数据未修改过，则会忽略
        skip_unchanged = True
        # 在导入预览页面中显示跳过的记录
        report_skipped = True
        # 对象标识的默认字段是id，您可以选择在导入时设置哪些字段用作id
        import_id_fields = ('id',)

        # 白名单
        fields = ('id','caseNo','busmodule','casename','project','projectGroup','caseType','caseLevel','caseFile','caseModule','casePcFunction','status',)
        # 黑名单
        exclude = ('addTime','modifyTime',)

class tcOnemanage(object):
    # import_excel = True

    # def post(self, request, *args, **kwargs):
    #     #  导入逻辑
    #     if 'excel' in request.FILES:
    #         pass  # 此处是一系列的操作接口, 通过  request.FILES 拿到数据随意操作
    #     return super(testCaseCpManage, self).post(request, args, kwargs)  # 此返回值必须是这样


    # ordering = ['id']
    list_display = ['caseNo','busmodule','casename','project','projectGroup','caseType','caseLevel','caseFile','caseModule','casePcFunction','status','addTime','modifyTime']
    search_fields = ['caseNo','casename','caseFile','caseModule','casePcFunction']
    list_editable = ['caseNo','busmodule','caseNo','casename','project','projectGroup','caseType','caseLevel','caseFile','caseModule','casePcFunction','status']
    # 分页
    list_per_page = 10
    # 配置模型图标，也可以在GlobalSetting里面配置
    model_icon = 'fa fa-star'

    # 配置导入按钮
    import_export_args = {
        'import_resource_class': testCasesOneManageResource,
        'export_resource_class': testCasesOneManageResource
    }

xadmin.site.register(testCasesKcpManage,tcKcpmanage)
xadmin.site.register(testCasesOneManage,tcOnemanage)

import xadmin
from .models import robotMsgManage
from import_export import resources
from django.apps import apps

class robotMsgManageResource(resources.ModelResource):
    def __init__(self):
        super(robotMsgManageResource,self).__init__()
        # 应用名与模型名
        field_list = apps.get_model('msgSend','robotMsgManage')._meta.fields
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
        model = robotMsgManage
        # 导入数据时，如果该条数据未修改过，则会忽略
        skip_unchanged = True
        # 在导入预览页面中显示跳过的记录
        report_skipped = True
        # 对象标识的默认字段是id，您可以选择在导入时设置哪些字段用作id
        import_id_fields = ('id',)

        # 白名单
        fields = ()
        # 黑名单
        exclude = ()

class rbtmsgmanage(object):
    # import_excel = True

    # def post(self, request, *args, **kwargs):
    #     #  导入逻辑
    #     if 'excel' in request.FILES:
    #         pass  # 此处是一系列的操作接口, 通过  request.FILES 拿到数据随意操作
    #     return super(testCaseCpManage, self).post(request, args, kwargs)  # 此返回值必须是这样

    # ordering = ['id']
    list_display = ['id','robotUrl','projectId','status','sendStatus','createTime','updateTime']
    search_fields = []
    list_editable = ['robotUrl', 'projectId', 'status','sendStatus']
    # 分页
    list_per_page = 10
    # 配置模型图标，也可以在GlobalSetting里面配置
    model_icon = 'fa fa-comment-o'

    # 配置导入按钮
    import_export_args = {
        'import_resource_class': robotMsgManageResource,
        'export_resource_class': robotMsgManageResource
    }

xadmin.site.register(robotMsgManage,rbtmsgmanage)

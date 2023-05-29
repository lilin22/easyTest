import xadmin
from xadmin import views
from .models import userProfile

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "soEasy管理后台系统"
    site_footer = "版权：http://www.cpy.com"
    menu_style = "accordion"

# class usersManage(object):
#     list_display = ['username', 'phone']

    # search_fields = ['username', 'phone']

# xadmin.site.unregister(userProfile)
# xadmin.site.register(userProfile, usersManage)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)

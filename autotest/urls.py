"""autotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url
from django.urls import include

from testcases import views as tcviews
import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from users.views import getTokenObtainPairView
from users import views as usviews
from projects import views as upviews
from busModule import views as bmviews
from appsdete import views as adviews
from runtask import views as rtviews
from msgSend import views as msviews
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'testCases/testCasesKcpList',tcviews.testCasesListKcpViewSet)
router.register(r'testCases/testCasesOneList',tcviews.testCasesListOneViewSet)
router.register(r'testTask/taskHistoryList',rtviews.runTestHistoryListViewSet)

urlpatterns = [
    #    path('admin/', admin.site.urls),
    url(r'admin/',xadmin.site.urls),
    url(r'docs',include_docs_urls(title='自动化测试中心')),
    url(r'^',include(router.urls)),
    url(r'user/modifyPassword',usviews.userSetPasswordView.as_view()),
    url(r'projectManage/getProjects',upviews.userProjectView.as_view()),
    url(r'projectManage/busModules',bmviews.busModulesView.as_view()),
    url(r'projectManage/appsDete',adviews.appsDeteView.as_view()),
    url(r'testCases/testCasesSearchKcpList',tcviews.testCasesKcpSearchView.as_view()),
    url(r'testCases/testCasesSearchOneList',tcviews.testCasesOneSearchView.as_view()),
    url(r'testCases/testCasesRunList',tcviews.testCasesRunView.as_view()),
    url(r'testTask/testRunStart',rtviews.testRunStartView.as_view()),
    url(r'projects/robotSendMsg',msviews.robotSendMsgView.as_view()),
    url(r'login',getTokenObtainPairView.as_view()),
    url(r'api/token',TokenObtainPairView.as_view()),
    url(r'api/token/refresh',TokenRefreshView.as_view()),
    url(r'api/token/verify',TokenVerifyView.as_view()),
]

# urlpatterns = urlpatterns + router.urls
import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Login from '@/components/login'
import CasesList from '@/components/casesList'
import TestTaskList from '@/components/testTaskList'
import download from '@/components/toolDownLoad'
import projectsGraph from '@/components/projectsGraph'
import webIDE from '@/components/webIDE'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/autoTest/login',
      name: 'login',
      component: Login,
      meta: {
        title: '登录'
      }
    },
    {
      path: '/autoTest/projects/testCasesList',
      name: 'casesList',
      component: CasesList,
      meta: {
        title: '测试用例列表'
      }
    },
    {
      path: '/autoTest/projects/testTaskList',
      name: 'taskList',
      component: TestTaskList,
      meta: {
        title: '测试任务列表'
      }
    },
    {
      path: '/autoTest/python-web',
      name: 'webIDE',
      component: webIDE,
      meta: {
        title: 'python编辑器'
      }
    },
    {
      path: '/autoTest/download',
      name: 'download',
      component: download,
      meta: {
        title: '下载列表'
      }
    },
    {
      path: '/autoTest/projects/graph',
      name: 'projectsGraph',
      component: projectsGraph,
      meta: {
        title: '图表分析'
      }
    }
  ]
})

router.beforeEach((to,from,next) => {
  const token = JSON.parse(sessionStorage.getItem('token'))
  if (to.path === '/autoTest/login') {
    next()
  } else {
    if (!token) {
      next('/autoTest/login')
    } else {
      next()
    }
  }
})

export default router

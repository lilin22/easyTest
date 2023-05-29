// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import elementUI from 'element-ui'
// import Vuex from 'vuex'
import moment from 'moment'
import store from './store'
import 'element-ui/lib/theme-chalk/index.css'
// import axios from 'axios'
import './style/theme.css'
import './style/character.css'
import UmyUi from 'umy-ui'
import 'umy-ui/lib/theme-chalk/index.css'
import VeRing from 'v-charts/lib/ring.common'
// import { UTable, UTableColumn } from 'umy-ui'
// import plTable from 'pl-table'
// import 'pl-table/themes/index.css'
// import 'pl-table/themes/plTableStyle.css'

//定义为全局
// Vue.prototype.$axios = axios
Vue.prototype.$moment = moment
Vue.config.productionTip = false
Vue.use(elementUI)
Vue.use(UmyUi)
Vue.component(VeRing.name, VeRing)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
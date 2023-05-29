import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  username: "",
  projectGroup_id:0,
}

//创建改变状态的方法
const mutations = {
  setUsername (state,payload) {
    state.username = payload.username
  },
  setProjectGroupId (state,payload) {
    state.projectGroup_id = payload
  }
}

export default new Vuex.Store({
  state,
  mutations
})

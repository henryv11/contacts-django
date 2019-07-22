import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: {}
  },
  mutations: {
    authRequest(state) {
      Vue.set(state, 'status', 'loading')    
    },
    authSuccess(state, payload) {
      Vue.set(state, 'status', 'success') 
      state.token = payload.token
    },
    authError(state) {
      Vue.set(state, 'status', 'error')
    },
    logout(state) {
      Vue.set(state, 'status', '')
      state.token = ''
      state.user = {}
    },
    setUser(state, payload) {
      state.user = payload
    }
  },
  actions: {
    login({commit}, user) {
      return new Promise((resolve, reject) => {
        commit('authRequest')
        Vue.prototype.axios({url: Vue.prototype.$apiBaseUrl + '/api/auth/token/obtain/', data: user, method: 'POST' })
        .then(resp => {
          const token = resp.data.token
          localStorage.setItem('token', token)
          commit('authSuccess', { token })
          resolve(resp)
        })
        .catch(err => {
          commit('authError')
          localStorage.removeItem('token')
          reject(err)
        })
      })
    },
    register({commit}, user) {
      return new Promise((resolve, reject) => {
        commit('authRequest')
        Vue.prototype.axios(
          {
            url: Vue.prototype.$apiBaseUrl + '/api/users/create/', 
            headers: { "Content-Type": "application/json" },
            data: user, method: 'POST' 
          })
        .then(resp => {
          commit('authSuccess', { token: undefined, user: undefined })
          resolve(resp)
        })
        .catch(err => {
          commit('authError', err)
          localStorage.removeItem('token')
          reject(err)
        })
      })
    },
    logout({commit}) {
      return new Promise((resolve, reject) => {
        commit('logout')
        localStorage.removeItem('token')
        resolve()
      })
    },
    userInfo({getters, commit}) {
      if (getters.isAuthenticated) {
        return new Promise((resolve, reject) => {
          Vue.prototype.axios.get(Vue.prototype.$apiBaseUrl + '/api/users/me/', { headers: {'Authorization': getters.bearerToken}})
          .then(resp => {
            commit('setUser', resp.data)
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
        })
      } 
    }
  },
  getters: {
    bearerToken: state => `Bearer ${state.token}`,
    isAuthenticated: state => !!state.token,
    authStatus: state => state.status,
    userId: state => state.user.id,
    username: state => state.user.username
  }
})

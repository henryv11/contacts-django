import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
 
Vue.prototype.$apiBaseUrl = "http://django-contacts-env.bdsipiypqj.us-east-2.elasticbeanstalk.com";

//Vue.prototype.$apiBaseUrl = "http://127.0.0.1:8000";

const api = axios.create({
})

api.interceptors.request.use(request => {
    //console.log('Starting Request', request)
    return request
  })
  
api.interceptors.response.use(response => {
    //console.log('Response:', response)
    return response
  })
Vue.use(VueAxios, api)

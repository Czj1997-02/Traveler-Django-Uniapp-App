import App from './App.vue'

// #ifndef VUE3
import Vue from 'vue'
// 引入vmeitime-http请求方式，作用同axios
import api from '@/common/vmeitime-http/'
// import config from '@/common/vmeitime-http/interface.js'
// config.baseUrl = 'http://127.0.0.1:8000'
// config.header = {
// 			'Content-Type': 'application/json;charset=UTF-8',
// 			'Content-Type': 'application/x-www-form-urlencoded',
// 			'Authorization': 'Bearer ' + uni.getStorageSync('token')
// 		},

Vue.prototype.$http = api

Vue.config.productionTip = false
// https://www.lervor.com/archives/128/
// Vue.prototype.$onLaunched = new Promise(resolve => {
//     Vue.prototype.$isResolve = resolve
// })
App.mpType = 'app'
const app = new Vue({
	...App
})
app.$mount()
// #endif

// #ifdef VUE3
import {
	createSSRApp
} from 'vue'
export function createApp() {
	const app = createSSRApp(App)
	return {
		app
	}
}
// #endif

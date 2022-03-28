import http from './interface'

/**
 * 将业务所有接口统一起来便于维护
 * 如果项目很大可以将 url 独立成文件，接口分成不同的模块
 * 
 */

// 单独导出(测试接口) import {test} from '@/common/vmeitime-http/'
export const post = (api,param) => {
	// http.config.baseUrl = 'http://192.168.42.86:8002'
	// //设置请求前拦截器
	// http.interceptor.request = (config) => {
	// 	// 添加通用参数
	// 	config.header = {
	// 		"Authorization": 'Bearer ' + uni.getStorageSync('token')
	// 	}
	// }
	// // 设置请求结束后拦截器
	// http.interceptor.response = (response) => {
	// 	// console.log('个性化response....')
	// 	//判断返回状态 执行相应操作
	// 	return response;
	// }
	return http.request({
		// baseUrl: 'http://192.168.42.86:8002',
		url: '/'+api,
		dataType: 'json',
		data: param,
		method: 'POST'
	})
}


export const get = (api,param) => {
	return http.request({
		url: '/'+api,
		method: 'GET',
		data:param
		// handle:true
	})
}

export const del = (api,param) => {
	return http.request({
		url: '/'+api,
		method: 'DELETE',
		data:param
		// handle:true
	})
}
// export const patch = (api,param) => {
// 	return http.request({
// 		url: '/'+api,
// 		method: 'GET',
// 		data:param
// 		// handle:true
// 	})
// }
export const put = (api,param) => {
	return http.request({
		url: '/'+api,
		method: 'PUT',
		data:param
		// handle:true
	})
}
export const options = (api,param) => {
	return http.request({
		url: '/'+api,
		method: 'OPTIONS',
		data:param
		// handle:true
	})
}
// 默认全部导出  import api from '@/common/vmeitime-http/'
export default {
	post,
	get,
	put,
	del,
	options
}

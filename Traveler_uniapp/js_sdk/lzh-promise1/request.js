// options = uni.request()所使用的动态的参数
export function fetch(options) {
	return new Promise((resolve, reject) => {
		// 这里根据你的需求去添加请求参数
		uni.request({
			url: options.url,
			method: options.method,
			headers: {
				'Content-Type': 'application/json',
			},
			data: options.data,
			success(res) {
				resolve(res);
			},
			fail(err) {
				reject(err);
			}
		});
	});
}
// options = uni.request()所使用的动态的参数
export function ajax(url, data, method) {
	return fetch({
		// #ifdef H5
		// url: '/api' + url,//h5跨域请求
		url:  url,//h5跨域请求
		// #endif
		// #ifndef H5
		// url: 'https://uniapp.dcloud.io/' + url,//非H5端正常请求
		url: url,//非H5端正常请求
		// #endif
		data: data,
		method: method,
	})
}


<template>
	<view class="content">
		<view class="login-bg">
			<view class="login-card">
				<view class="login-head">登录</view>
				<view class="login-input login-margin-b">
					<!-- <input v-model="username" placeholder="请输入账号" /> -->
					<uni-easyinput type="text" prefixIcon="contact" v-model="username" placeholder="请输入您的账号"/>
				</view>
				<view class="login-input">
					<!-- <input type="password" v-model="password" placeholder="请输入密码(8-16位)"/> -->
					<uni-easyinput  type="password" prefixIcon="locked" v-model="password" placeholder="请输入密码(8-16位)" />
				</view>
				<view class="login-input">
				<uni-data-picker :localdata="items" popup-title="请选择服务器" @change="onchange" @nodeclick="onnodeclick" v-model="urlip"></uni-data-picker>
				</view>
				<view class="login-function">
					<view class="login-forget" @click="go_forget">忘记密码(Forget)</view>
					<view class="login-register" @click="go_register">注册(Register)></view>
				</view>
			</view>
		</view>
		<view class="login-btn">
			<button class="landing" type="primary" @click="login">登陆 / Login</button>
		</view>
	</view>
</template>

<script>
	import config from '../../common/vmeitime-http/interface.js'
	export default {
		data() {
			return {
				urlip: 'https://samle.top:8065',
				username: '',
				password: '',
				items: [
					{
						text: '8000端口测试服务器',
						value: 'http://127.0.0.1:8000'
					},
					// {
					// 	text: '8000端口家庭服务器',
					// 	value: 'http://192.168.3.9:8000'
					// },
					{
						text: '8066端口阿里云服务器',
						value: 'https://www.eatqionline.top:8066'
					},
					{
						text: '8065端口腾讯云服务器',
						value: 'https://samle.top:8065'
					}
				]
			}
		},
		created() {
			if (config.baseURL) {
				console.log(1,config.baseURL)
				this.urlip = config.baseURL
				uni.showToast({
					title:config.baseURL,
					icon:'none',
				})
			} else if (uni.getStorageSync('urlip')) {
				console.log(2,uni.getStorageSync('urlip'))
				this.urlip = uni.getStorageSync('urlip')
				uni.showToast({
					title:uni.getStorageSync('urlip'),
					icon:'none',
				})
			} else {
				console.log(3,null)
				this.urlip = 'https://samle.top:8065'
				uni.showToast({
					title:'null-->https://samle.top:8065',
					icon:'none',
				})
			}
			
		},
		onLoad() {
			// uni.setStorageSync('urlip', this.urlip)
			// config.baseURL = this.urlip
		},
		onPullDownRefresh() {
			// this.$router.go(0)
			
			uni.navigateTo({
				url: '/pages/JudeLoginPage/JudeLoginPage'
			});

			// uni.navigateBack({
			// 	success: () => {
			// 		// 因为直接跳转影响返回,所以到tab页面后再跳转
			// 		uni.navigateTo({
			// 			url: '/pages/Eider/TripEider' +'?id='+ encodeURIComponent(this.tripID) + '&name=' + encodeURIComponent(this.tripname)
			// 		});
			// 	}
			// })

			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		methods: {
			go_forget(){
				uni.navigateTo({
				    url: '/pages/Login/forget'
				})
			},
			go_register(){
				uni.navigateTo({
					url: '/pages/Login/register'
				})
			},
			onchange(e) {
				const value = e.detail.value
				// console.log(e.detail.value[0].value)
				// uni.setStorageSync('urlip', e.detail.value[0].value)
				// config.baseURL = e.detail.value[0].value
			},
			onnodeclick(node) {
				// uni.setStorageSync('urlip', node.value)
				// config.baseURL = node.value
				// console.log('当前选择:', node.value,'当前地址:',config.baseURL)

				async function foo () {
					uni.setStorageSync('urlip', node.value)
					config.baseURL = node.value
					console.log('当前选择:', node.value,'当前地址:',config.baseURL)
					return 'info'
				}
				foo().then(val => {
				  console.log(val) // info
				  this.$router.go(0)
				  uni.navigateTo({
					url: '/pages/JudeLoginPage/JudeLoginPage'
			      });
				})
				
			},
			login () {
				// config.baseURL = uni.getStorageSync('urlip')
				// const data = http.get(url).then(res=> console.log(res.data))
				this.$http.post('login/', {username: this.username, password: this.password}).then(res=> {
				// console.log(res.data)
				uni.showToast({
					title:config.baseURL,
					icon:'none',
				})
				if (res.data.code !== 200) {
					return uni.showModal({
						title: '通知',
						content: res.data.msg,
						showCancel: false
					})
				}
				// 存储token
				// uni.setStorage({
				// 	key:'token',
				// 	data:res.data.data.token,
				// 	success() {
				// 		uni.showToast({
				// 			title:'储存成功'
				// 		});
				// 	}
				// })
				uni.setStorageSync('token', res.data.data.token)
				uni.setStorageSync('superuser', res.data.data.is_superuser)
				uni.setStorageSync('city', res.data.data.city)
				uni.setStorageSync('user', res.data.data.user);
				uni.setStorageSync('username', this.username);
				uni.setStorageSync('password', this.password);
				console.log(res.data.data)
				// 跳转到主页
				uni.reLaunch({
					url: '/pages/tabbar/tabbar-1/tabbar-1'
				}).then(this.$router.go(0))
			})
			}
		}
	}
</script>

<style>
	.landing{
		height: 84upx;
		line-height: 84upx;
		border-radius: 44upx;
		font-size: 32upx;
		background: linear-gradient(#b3ccd0, #bedb74);
	}
	.login-btn{
		padding: 10upx 20upx;
		margin-top: 350upx;
	}
	.login-function{
		overflow: auto;
		padding: 20upx 20upx 30upx 20upx;
	}
	.login-forget{
		float: left;
		font-size: 26upx;
		color: #999;
	}
	.login-register{
		color: #666;
		float: right;
		font-size: 26upx;

	}
	.login-input input{
		background: #F2F5F6;
		font-size: 28upx;
		padding: 10upx 25upx;
		height: 62upx;
		line-height: 62upx;
		border-radius: 8upx;
	}
	.login-margin-b{
		margin-bottom: 25upx;
	}
	.login-input{
		padding: 10upx 20upx;
	}
	.login-head{
		font-size: 34upx;
		text-align: center;
		padding: 25upx 10upx 55upx 10upx;
	}
	.login-card{
		background: #fff;
		border-radius: 12upx;
		padding: 10upx 25upx;
		box-shadow: 0 6upx 18upx rgba(0,0,0,0.12);
		position: relative;
		margin-top: 120upx;
	}
	.login-bg {
		height: 260upx;
		padding: 25upx;
		background: linear-gradient(#b3ccd0, #bedb74);
	}
</style>

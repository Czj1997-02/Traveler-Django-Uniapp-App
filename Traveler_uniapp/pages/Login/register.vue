<template>
	<view class="content">
		<view class="forget-bg">
			<view class="forget-card">
				<view class="forget-input forget-margin-b">
					<uni-easyinput type="text" prefixIcon="contact" v-model="username" placeholder="请输入您的账号" @blur="test1()"/>
				</view>
				<view class="forget-input forget-margin-b">
					<!-- <input placeholder="请输入您的昵称" /> -->
					<uni-easyinput type="text" prefixIcon="contact-filled" v-model="realname" placeholder="请输入您的昵称"/>
				</view>
				<view class="forget-input forget-margin-b">
					<!-- <input placeholder="请输入您的个性签名" /> -->
					<uni-easyinput type="text" prefixIcon="sound" v-model="desc" placeholder="请输入您的个性签名"/>
				</view>
				<view class="forget-input forget-margin-b">
					<uni-easyinput  type="text" prefixIcon="phone" v-model="telephone" placeholder="请输入您的手机号" @blur="test2()"/>
					<!-- <input type="number" placeholder="请输入您的手机号" /> -->
				</view>
				<view class="forget-input forget-margin-b">
					<view class="verify-left">
						<input type="number" placeholder="请输入验证码" v-model="code"/>
					</view>
					<view class="verify-right">
						<button class="verify-btn" type="primary" @click="getcode">{{send?'发送验证码':second+'s重新发送'}}</button>
					</view>
				</view>
				<view class="forget-input">
					<uni-easyinput  type="password" prefixIcon="locked" v-model="password" placeholder="请输入密码(8-16位)" />
					<!-- <input placeholder="请输入密码(8-16位)" /> -->
				</view>
			</view>
		</view>
		<view class="forget-btn">
			<button class="landing" type="primary" @click="register">提交</button>
		</view>
	</view>
</template>

<script>
	import { ajax } from "../../js_sdk/lzh-promise1/request.js"
	export default {
		data() {
			return {
				s: 60,	//默认倒计时
				second: 0,
				send: true, //按钮可以点击
				username: '',
				telephone: '',
				password: '',
				realname: '',
				desc: '',
				code: '',
				urlip: 'https://samle.top:8065',
				// urlip: 'https://www.eatqionline.top:8066',
				// urlip: 'http://192.168.3.9:8000',
			}
		},
		onLoad() {

		},
		created() {
			this.urlip = uni.getStorageSync('urlip')
		},
		methods: {
			async getcode () {
				// 防止多次重复点击
				if(!this.send){
					return false;
				}
				const { data: res } = await ajax(this.urlip + '/rc/',{telephone: this.telephone},'post')
				// console.log(res)
				this.send = false
				if (res.code !== 201) {
					return uni.showModal({
						title: '通知',
						content: '服务器链接异常！',
						showCancel: false,
					})
				} else {
					uni.showToast({
						title:'发送成功',
						icon:'none',
						success: () => {
							this.time();	// 倒计时
						}
					})
				}
				// if (res.data.length !== 0) {
				// 	return uni.showModal({
				// 		title: '通知',
				// 		content: '账号已存在,请重新输入！',
				// 		showCancel: false
				// 	})
				// }
			},
			time(){
				let that = this;
				that.second = that.s;
				let interval = setInterval(function(){
					if(that.second == 1){
						that.send = true;
						that.second = that.s;
						clearInterval(interval);
					}else {
					// console.log(that.second)
						that.second--;
					}
				},1000)
			},
			async register () {
				const { data: res } = await ajax(this.urlip + '/register/',{
					telephone: this.telephone,
					code: this.code,
					username: this.username,
					password: this.password,
					realname: this.realname,
					desc: this.desc,
				},'post')
				uni.showToast({
					title:this.urlip,
					icon:'none',
				})
				console.log(res)
				if (res.code === 401) {
					return uni.showModal({
						title: '通知',
						content: res.msg,
						showCancel: false
					})
				} else if (res.code !== 201) {
					return uni.showModal({
						title: '通知',
						content: '服务器链接异常！',
						showCancel: false
					})
				} else if (res.code === 201) {
				uni.navigateTo({
				    url: '/pages/Login/Login'
				})
				}
			},
			async test1 () {
				const { data: res } = await ajax(this.urlip + '/register/',{username: this.username},'get')
				console.log(res)
				if (res.code !== 200) {
					return uni.showModal({
						title: '通知',
						content: '服务器链接异常！',
						showCancel: false
					})
				}
				if (res.data.length !== 0) {
					return uni.showModal({
						title: '通知',
						content: '账号已存在,请重新输入！',
						showCancel: false
					})
				}
			},
			async test2 () {
				// const { data: res } = await ajax(this.urlip + '/register/',{telephone: this.telephone},'get')
				// if (res.code !== 200) {
				// 	return uni.showModal({
				// 		title: '通知',
				// 		content: '服务器链接异常！',
				// 		showCancel: false
				// 	})
				// }
				// if (res.data.length !== 0) {
				// 	return uni.showModal({
				// 		title: '通知',
				// 		content: '手机号已存在,请重新输入！',
				// 		showCancel: false
				// 	})
				// }
				if (!(/^1(3|4|5|6|7|8|9)\d{9}$/.test(this.telephone))) {
					return uni.showModal({
						title: '通知',
						content: '手机号格式不正确,请重新输入！',
						showCancel: false
					})
				}
			}
		}
	}
</script>

<style>
	.verify-left{
		width: calc(100% - 260upx);
	}
	.verify-right{
		padding-left: 20upx;
	}
	.verify-btn{
		height: 80upx;
		line-height: 80upx;
		font-size: 28upx;
		width: 240upx;
		border-radius: 8upx;
		background: linear-gradient(#b3ccd0, #bedb74);
	}
	.verify-left,.verify-right{
		float: left;
	}
	.landing{
		height: 84upx;
		line-height: 84upx;
		border-radius: 44upx;
		font-size: 32upx;
		background: linear-gradient(#b3ccd0, #bedb74);
	}
	.forget-btn{
		padding: 10upx 20upx;
		margin-top: 730upx;
	}

	.forget-input input{
		background: #F2F5F6;
		font-size: 28upx;
		padding: 10upx 25upx;
		height: 62upx;
		line-height: 62upx;
		border-radius: 8upx;
	}
	.forget-margin-b{
		margin-bottom: 25upx;
	}
	.forget-input{
		padding: 10upx 20upx;
		overflow: auto;
	}
	.forget-card{
		background: #fff;
		border-radius: 12upx;
		padding: 60upx 25upx;
		box-shadow: 0 6upx 18upx rgba(0,0,0,0.12);
		position: relative;
		margin-top: 120upx;
	}
	.forget-bg {
		height: 260upx;
		padding: 25upx;
		background: linear-gradient(#b3ccd0, #bedb74);
	}
</style>

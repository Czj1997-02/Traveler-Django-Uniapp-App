<template>
	<view class="content">
		<!-- <view class="user-data-box" @click="goToPage('/pages/User/User')"> -->
		<view class="user-data-box" @click="NoPageTip()">
		<uni-row>
			<uni-col :span="6">
				<cmd-avatar :src="UserData.portrait_src" size="lg" shape="square"></cmd-avatar>
			</uni-col>
			<uni-col :span="16">
				<!-- <view ><text class="name-box">昵称： </text> <text class="value-box">{{UserData.realname}}</text></view> -->
				<!-- <view ><text class="name-box">账号： </text> <text class="value-box">{{UserData.username}}</text></view> -->
				<!-- <view ><text class="name-box">城市： </text> <text class="value-box">{{UserData.cityname}}</text></view> -->
				<view ><text class="name-box">{{UserData.realname}}</text></view>
				<view ><text class="value-box">{{UserData.desc}}</text></view>
			</uni-col>
			<uni-col :span="2" style="margin-top: 20px;">
				<uni-icons type="forward" size="20" style="color: #b3ccd0;margin-left: 12px;"></uni-icons>
			</uni-col>
		</uni-row>
		</view>
		<uni-list class="list-box">
			<uni-list-item :show-extra-icon="true" showArrow v-for="(item, index) in list1" :key="index" :title="item.name" link :to="item.url":extra-icon="item.icon" />
		</uni-list>
		<uni-list class="list-box">
			<uni-list-item :show-extra-icon="true" showArrow v-for="(item, index) in list2" :key="index" :title="item.name" link :to="item.url":extra-icon="item.icon" />
		</uni-list>
		<uni-list class="list-box">
			<!-- <uni-list-item :show-extra-icon="true" showArrow v-for="(item, index) in list3" :key="index" :title="item.name" link :to="item.url":extra-icon="item.icon" /> -->
			<uni-list-item :show-extra-icon="true" showArrow title="退出" link to="/pages/Login/Login" :extra-icon="outicon" @click="outlogin()"/>
		</uni-list>
	</view>
</template>

<script>
	// import '../../../common/iconfont/iconfont.css'
	export default {
		data() {
			return {
				outicon: {
					color: '#333333',
					size: '20',
					type: 'redo'
				},
				UserData: {},
				list1: [
					{
						name:'我的博文',
						url: '/pages/User/MyBlog',
						icon: {
							color: '#05d2bc',
							size: '20',
							type: 'compose'
						},
					},
					{
						name:'我的行程',
						url: '/pages/User/MyTrip',
						icon: {
							color: '#00a0e9',
							size: '20',
							type: 'map'
						},
					},
					{
						name:'我的词条',
						url: '/pages/User/MyPlace',
						icon: {
							color: '#b6d148',
							size: '20',
							type: 'map-pin-ellipse'
						},
					},
				],
				list2: [
					// {
					// 	name:'收藏列表',
					// 	url: '/pages/User/Collect',
					// 	icon: {
					// 		color: '#e8c50a',
					// 		size: '20',
					// 		type: 'star'
					// 	},
					// },
					// {
					// 	name:'点赞列表',
					// 	url: '/pages/User/Praise',
					// 	icon: {
					// 		color: '#ec7171',
					// 		size: '20',
					// 		type: 'heart'
					// 	},
					// },
					{
						name:'关注列表',
						url: '/pages/User/Follow',
						icon: {
							color: '#d597dc',
							size: '20',
							type: 'eye'
						},
					},
				],
				list3: [
					// {
					// 	name:'设置',
					// 	url: '/pages/User/Sys',
					// 	icon: {
					// 		color: '#bd3d3d',
					// 		size: '20',
					// 		type: 'gear'
					// 	},
					// },
					// {
					// 	name:'公告',
					// 	url: '/pages/User/Notice',
					// 	icon: {
					// 		color: '#e9761a',
					// 		size: '20',
					// 		type: 'sound'
					// 	},
					// },
					// {
					// 	name:'退出',
					// 	url: '/pages/Login/Login',
					// 	icon: {
					// 		color: '#333333',
					// 		size: '20',
					// 		type: 'redo'
					// 	},
					// },
				],
			}
		},
		onLoad() {

		},
		created() {
			this.getUserData()
			// uni.reLaunch({
			// 	url:'/pages/Login/Login'
			// })
		},
		methods: {
			outlogin(){
				console.log('退出登录同步清除数据')
				return uni.clearStorageSync();
			},
			getUserData () {
				this.$http.get('myself/').then(res=> {
				if (res.data.code === 200) {
					this.UserData = res.data.data[0]
				}
				})
			},
			goToPage(url) {
				if (!url) return;
				uni.navigateTo({
					url
				});
			},
			NoPageTip(){
				uni.showToast({title:'页面暂未完成，不予显示',icon:'none'})
			}
		}
	}
</script>

<style>
.content{
	background-color: #b3ccd0;
	min-height: 100vh-40px;
}
.user-data-box {
	padding: 10px 10px;
	/* background-color: #b3ccd0; */
	background-color: #ffffff;
}
.name-box {
	font-weight: 600;
	font-size: 15px;
}
.value-box {
	/* font-weight: 600; */
	font-size: 12px;
}
.group-box {
	margin: 0px !important;
}
.
/deep/.uni-group__content {
	padding: 0px !important;
}
.list-box {
	margin-top: 18rpx;
}
</style>

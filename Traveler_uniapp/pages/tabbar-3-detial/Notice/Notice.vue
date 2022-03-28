<template>
	<view>
		<uni-group title="公告标题" class="group-box">
			<uni-easyinput class="name-box" :inputBorder="false"  v-model="name" placeholder="公告标题" clearable ></uni-easyinput>
		</uni-group>
		<uni-group title="公告内容" class="group-box">
			<uni-easyinput class="content-box" type="textarea"  v-model="text" placeholder="公告内容" clearable ></uni-easyinput>
		</uni-group>
		<button @click="postNotice" style="color:red;background-color: #b3ccd0">发布</button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				name: '',
				text: ''
			}
		},
		methods: {
			postNotice(){
				this.$http.post('notice/', {
					name: this.name,
					text: this.text
				}).then(res=> {
					console.log(res.data)
					// 避免还没上传完就跳转回首页
					setTimeout(()=>{
						uni.reLaunch({
							url: '/pages/tabbar/tabbar-1/tabbar-1'
						})
					},1000)
				})
			}
		}
	}
</script>

<style>
.group-box {
	margin: 0px !important;
}
/deep/.name-box .uni-easyinput__content-input {
	border-bottom: 1px solid #e5e5e5 !important;
}
/deep/.content-box .uni-easyinput__content .uni-easyinput__content-textarea {
	min-height: 150px !important;
	height: 150px !important;
}
</style>

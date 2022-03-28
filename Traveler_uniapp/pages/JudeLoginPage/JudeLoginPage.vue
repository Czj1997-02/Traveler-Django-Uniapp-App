<template>
	<view>
		
	</view>
</template>

<script>
	export default {
		data() {
			return {
				type: '',
				code: ''
			};
		},
		created() {
			this.$http.get('blog-tags/').then(res=> {
			console.log(res)
			if (res) {
				this.code = res.data.code
				if ( this.code === 200 ) {
					// console.log('有token且有效')
					uni.reLaunch({
						// url: '/pages/tabbar/tabbar-1/tabbar-1?blogtype='+ encodeURIComponent(JSON.stringify(res.data.data))
						url: '/pages/tabbar/tabbar-1/tabbar-1'
					})
				} else {
					// console.log('没有token或者jwt-token已经失效')
					uni.reLaunch({
						url:'/pages/Login/Login'
					})
				}
			} else {
				// console.log('没有token或者jwt-token已经失效')
				uni.reLaunch({
					url:'/pages/Login/Login'
				})
			}
			}) 
		}
	}
</script>

<style lang="scss">

</style>

<template>
	<view>
	<view>
		<uni-data-picker :localdata="this.cityData"  v-model="city" popup-title="请选择所在城市以便于提供服务" @change="onchange" @nodeclick="onnodeclick"></uni-data-picker>
	</view>
	<button @click="changecity" style="background-color: #b3ccd0">确认</button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				city: '',
				userID: null,
				cityData: []
			}
		},
		created() {
			this.getCityData()
			this.getUserSelf()
		},
		methods: {
			getCityData () {
				this.$http.get('city-tree/').then(res=> {
					this.cityData = res.data.data
					// console.log(this.cityData)
				})
			},
			onchange(e) {
				const value = e.detail.value
				// console.log(e.detail.value, e.detail.text)
			},
			onnodeclick(node) {
				// console.log(node.text)
				// uni.setStorageSync('city', node.text)
			},
			getUserSelf () {
				this.$http.get('myself/').then(res=> {
				// console.log(res.data)
				if (res.data.code === 200) {
					this.userID = res.data.data[0].id
				}
				// console.log('用户id',this.userID)
				})
			},
			changecity () {
				// console.log(this.city)
				this.$http.put('myself/' + this.userID + '/', {user: this.userID,city: this.city}).then(res=> {
				// console.log(res.data)
				if (res.data.code === 200) {
					uni.setStorageSync('city', res.data.data.cityname)
					uni.reLaunch({
						url: '/pages/tabbar/tabbar-1/tabbar-1',
					})
				}
				})
			}
		},
		onLoad(option) {
			this.city = JSON.parse(decodeURIComponent(option.oldcity));
			// this.city = decodeURIComponent(option.oldcity)
		}
	}
</script>

<style>

</style>

<template>
	<view>
<!-- 		<web-view></web-view> -->
		<web-view :src="this.url"></web-view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				url: ''
			}
		},
		methods: {
			
		}
	}
</script>

<style>

</style>

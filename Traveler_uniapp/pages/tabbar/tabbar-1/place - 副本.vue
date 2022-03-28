<template>
	<view>
		<!-- <uni-icons type="trash-filled" size="20" class="delicon"></uni-icons> -->
		<!-- 封面 -->
		<!-- <view class="image-box"><image :src="data.image" class="face-image"></image></view> -->
		
		<!-- <uni-group title="摘要" class="blog-content-box" v-if="this.data.content"> -->
			<!-- <uni-easyinput class="content-box" type="textarea"  v-model="this.data.content" disabled ></uni-easyinput> -->
		<!-- </uni-group> -->
		
		<!-- this.$refs.amapbox.dataIndex 可以拿到是第几个数据 -->
		<amap :markerList="markerList" :zoom="zoom" ref='amapbox'></amap>
		<!-- <amap :markerList="markerList" :zoom="zoom" ref='amapbox'></amap> -->
		
		<uni-group title="内容" class="blog-content-box">
		<!-- 内容-换服务器影响图片显示，图片尺寸过大显示不完整 -->
		<view auto-height v-html="data.desc" class="blog-desc"></view>
		</uni-group>
		<!-- <button @click="print">打印</button> -->
		
	</view>
</template>

<script>
	const start = 'static/ITkoala-amap/start.png'
	import amap from '@/components/ITkoala-amap/show.vue'
	export default {
		components: {
			amap,
		},
		data() {
			return {
				data: {},
				markerList: [],
				zoom: 16,
				// map: null,
				// ownerInstanceObj: null ,//service层对象
				// dataIndex: ''
			}
		},
		methods: {
			print() {
				console.log(this.markerList,this.$refs.amapbox.dataIndex)
			}
		},
		created() {
			console.log(this.markerList)
		},
		onLoad(option) {
			const id = JSON.parse(decodeURIComponent(option.id))
			this.$http.get('place/' + id + '/').then(res=> {
			console.log(res.data)
			if (res.data.code === 200) {
				this.data = res.data.data
				this.markerList = [{lat:this.data.lat,lng:this.data.lng,icon: start}]
				this.firstmark = [this.data.lng,this.data.lat]
				console.log(this.data)
				uni.setNavigationBarTitle({
					title: this.data.name
				})
			}
			this.$forceUpdate()
			})
		},
		onPullDownRefresh() {
			this.$forceUpdate()
			setTimeout(()=>{
				uni.stopPullDownRefresh()
				uni.showToast({title:'刷新成功',icon:'none'})
			},800)
		}
	}
</script>

<style>
.html{
	width: 100%;
	word-break: break-all;
}
.image-box {
	width: 100%;
	padding: 0px;
	margin: 0px !important;
}
.face-image {
	width: 100%;
	padding: 0px;
	margin: 0px !important;
}
.blog-content-box {
	margin-top: 0px;
	margin: 0px !important;
}
/deep/.content-box .uni-easyinput__content .uni-easyinput__content-textarea {
	min-height: 50px !important;
	height: 50px !important;
}
.blog-desc-box {
	margin-top: 20px ;
	margin: 0px !important;
}
.blog-desc {
	width: 100%;
	word-break: break-all;
}
</style>

<template>
	<view class="amap-container">
		<view :prop="markerList" :change:prop="amap.updateEcharts" id="amap"></view>
		<!-- <view class="">当前点击的对象的index值为：{{ dataIndex }}</view> -->
	</view>
</template>


<script module="amap" lang="renderjs">
const start = 'static/ITkoala-amap/start.png'
import config from './config.js'

const selectedStart = 'static/ITkoala-amap/selectedStart.png' //选中的图片

export default {
	props: {
		markerList: {
			type: Array,
			// default: []
			default: () => [
				// {
				// 	lat: 23.00465240242822062555,
				// 	lng: 114.48473408818247776253,
				// 	icon: start
				// }
			]
		},
		zoom: {
			type: Number,
			default: 10
		},
		// dataIndex: {
		// 	type: Number,
		// 	default: null
		// },
		// ownerInstanceObj: {
		// 	type: Object,
		// 	default: null
		// },
		// map: {
		// 	type: Object,
		// 	default: null
		// }
	},
			  
	data() {
		return {
			map: null,
			ownerInstanceObj: null ,//service层对象
			// markerList: [],
			dataIndex: 0
		}
	},
	mounted() {
		// this.$nextTick(() => {
		// 	this.getMapData()
		// })
		if (typeof window.AMap === 'function') {
			this.initAmap()
		} else {
			// 动态引入较大类库避免影响页面展示
			const script = document.createElement('script')
			script.src = 'https://webapi.amap.com/maps?v=1.4.15&key=' + config.WEBAK
			script.onload = this.initAmap.bind(this)
			document.head.appendChild(script)
		}
	},
	methods: {
		// getMapData() {
		// 	this.markerList = [
		// 		{
		// 			lat: 23.00465240242822062555,
		// 			lng: 114.48473408818247776253,
		// 			icon: start
		// 		},
		// 		// {
		// 		// 	lat: 39.973253,
		// 		// 	lng: 116.473195,
		// 		// 	icon: start
		// 		// },
		// 		// {
		// 		// 	lat: 39.953253,
		// 		// 	lng: 116.453195,
		// 		// 	icon: start
		// 		// }
		// 	]
		// },
		initAmap() {
			this.map = new AMap.Map('amap', {
				resizeEnable: true,
				center: [this.markerList[0].lng, this.markerList[0].lat],
				layers: [ //使用多个图层
					// new AMap.TileLayer.Satellite() //使用卫星图
				],
				zooms: [4, 18], //设置地图级别范围
				zoom: this.zoom
			})

			this.initMarkers()
		},
		//初始化标记点
		initMarkers() {
			let prevMarker = null
			let prevIcon = null
			this.markerList.forEach((item, index) => {

				if(!!item.icon){
					//添加点标记
					let marker = new AMap.Marker({
						position: new AMap.LngLat(item.lng, item.lat),
						offset: new AMap.Pixel(-16, -30),
						icon: item.icon
					})

					marker.on('click', (e) => {
						if(!!prevMarker){
							prevMarker.setIcon(prevIcon)
						}
						prevIcon = item.icon
						prevMarker = marker
						marker.setIcon(selectedStart)
						this.dataIndex = index
						this.onClick(null,this.ownerInstanceObj)
					})

					this.map.add(marker)
				}

			})
		},
		//地图点击回调事件
		onViewClick(params) {
			this.dataIndex = params.dataIndex
		},
		updateEcharts(newValue, oldValue, ownerInstance, instance) {
			// 监听 service 层数据变更
			this.ownerInstanceObj = ownerInstance
		},
		onClick(event, ownerInstance) {
			// 调用 service 层的方法
			ownerInstance.callMethod('onViewClick', {
				dataIndex: this.dataIndex
			})
		}
	}
}
</script>

<style lang="scss" scoped>
#amap {
	width: 100%;
	height: 480rpx;
}

.infoWindow-wrap{
	  margin-left: 50px;
		color: #f00;
	}
</style>

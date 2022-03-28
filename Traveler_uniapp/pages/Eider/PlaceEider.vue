<template>
	<view class="amap-container">
		<!-- 之前if有问题，如果页面报错尝试注释if -->
		<view :prop="markerList" :change:prop="amap.updateEcharts" id="amap" v-if="data.lat"></view>
		<!-- <view class="">当前点击的对象的index值为：{{ dataIndex }}</view> -->
		<view>
		
		<uni-group :title="data.name" class="content-box">
		<!-- 内容-换服务器影响图片显示，图片尺寸过大显示不完整 -->
		<view >
			<view style="height: 1rpx;"></view>
			<uni-row >
			<uni-col :span="3" >
				<cmd-avatar :src="data.created_by_portrait" size="sm" @click="ToUser(data.created_by,data.created_by_name)"></cmd-avatar>
			</uni-col>
			<uni-col :span="9" style="margin-top: 5px;">
				<text style="font-weight: 600;font-size 28rpx;padding 4rpx;">{{data.created_by_name}}</text>
			</uni-col>
			
			<uni-col :span="10" style="margin-top: 8px;">
				<uni-tag :text="typchiose[data.typ]" class="my-tag" :circle="true" size="small" style="float: right;"></uni-tag>
				<text style="font-size: 10px;color: #222222;float: right;margin-top: 2px;" v-if="data.typ !== 'other'">{{data.city_name}}</text>
			</uni-col>
			
			<uni-col :span="2" style="margin-top: 10px;">
				<uni-icons type="more-filled" size="18"  @click="openpop()" style="float: right;"></uni-icons>
			</uni-col>
			
			</uni-row>
			
			<!-- <uni-tag :text="data.id" class="my-tag" :circle="true" size="small"></uni-tag> -->
					
		</view>
		<view style="height: 2px; margin-top: 5px; margin-bottom: 5px; border-bottom-style: inset;"></view>
		
		<view class="imgs" v-if="data.images">
			<block v-for="(img, index) in data.images" :key="index">
				<!-- <view class="imgs-box"><image :src="img" mode="aspectFill" style="width: 100%;height:110px"  @click="previewImg(img,data.images)"></image></view> -->
				<view class="imgs-box"><image :src="img" mode="aspectFill" class="img-style"  @click="previewImg(img,data.images)"></image></view>
			</block>
		</view>
		
		<!-- </uni-group>	 -->
		
		<!-- <uni-group title="内容" class="content-box"> -->
		<!-- 内容-换服务器影响图片显示，图片尺寸过大显示不完整 -->
		<view auto-height v-html="data.desc" class="blog-desc"></view>
		<!-- <view style="height: 2px; margin-top: 5px; margin-bottom: 5px; border-bottom-style: inset;"></view> -->
		<uni-row style="margin-top: 5px;" v-if="data.typ !== 'other'">
			<uni-col :span="9" style="margin-top: 10px;">
				<text style="font-size: 10px;color: #222222;float: left;">{{data.created_date}}</text>
			</uni-col>
			
			<!-- <uni-col :span="9" style="margin-top: 10px;">
				<text style="font-size: 10px;color: #222222;float: left;">{{data.created_date}}</text>
			</uni-col> -->
			
			<uni-col :span="5" style="margin-top: 5px;">
				
				<uni-icons type="heart" size="15" style="color:#ec7171;float: left;margin-top: 5px;" v-if="! data.is_praise" @click="dianzan()"></uni-icons>
				<uni-icons type="heart-filled" size="15" style="color:#ec7171;float: left;margin-top: 5px;" v-if="data.is_praise" @click="quxiaozan()"></uni-icons>
				<text style="font-size:15px;color:#545d61;float: left;margin-top: 3px;">{{data.praise}}</text>
			</uni-col>
			
			<uni-col :span="5" style="margin-top: 5px;">
				<uni-icons type="star" size="15" style="color:#e8c50a;float: left;margin-top: 5px;" v-if="! data.is_collect" @click="shoucang()"></uni-icons>
				<uni-icons type="star-filled" size="15" style="color:#e8c50a;float: left;margin-top: 5px;" v-if="data.is_collect" @click="quxiaocang()"></uni-icons>
				<text style="font-size:15px;color:#545d61;float: left;margin-top: 3px;">{{data.collect}}</text>
			</uni-col>
			
			<uni-col :span="5" style="margin-top: 5px;">
				<uni-icons type="chat" size="15" style="color:#4a4a4a;float: left;margin-top: 5px;"></uni-icons>
				<text style="font-size:15px;color:#545d61;float: left;margin-top: 2px;">{{data.talk}}</text>
			</uni-col>
		</uni-row>	
		
		<!-- 评论区 -->
		<view style="height: 2px; margin-top: 5px; margin-bottom: 5px; border-bottom-style: inset;"></view>
		
		<view class="talks-box">
			<view class="talks-box-list" v-for="(item,index) in talkData" style="margin-top: 3px;background-color: #f4f5f5;">
				<uni-row style="padding: 5px;">
					<uni-col :span="3">
						<cmd-avatar :src="item.portrait" size="sm" @click="ToUser(item.created_by,item.created_by_name)"></cmd-avatar>
					</uni-col>
					<uni-col :span="21">
						<uni-row>
							<uni-col :span="10"><text style="color: #0077AA;font-size: 10px;">{{item.created_by_name}}</text></uni-col>
							<uni-col :span="12"><text style="font-size: 10px;">{{item.created_date}}</text></uni-col>
							<uni-col :span="2" ><uni-icons type="trash-filled" size="18"  @click="deltalk(item.id)" style="float: right;"></uni-icons></uni-col>
						</uni-row>
						<view>{{item.desc}}</view>
					</uni-col>
				</uni-row>
			</view>
		</view>
		<view v-if="showadd" style="font-size: 15px;color: #b3ccd0;font-weight: 600;text-align: center;margin-top: 5px;" @click="ShowMoreTalk"><text >加载更多</text></view>
		</uni-group>
		
		<!-- 避免置底遮挡 -->
		<view style="height: 50px;"></view>
		<view class="talk-box">
			
		<uni-row style="margin-top: 5px;">
			<uni-col :span="18" >
				<uni-easyinput  v-model="talk" placeholder="评论:"  clearable style="margin-left:4%"></uni-easyinput>
			</uni-col>
			<uni-col :span="6" >
				<button size="mini" style="background-color: #b3ccd0;margin-left: 18%;margin-top: 3px;" @click="posttalk()">评论</button>
			</uni-col>
		</uni-row>
		
		</view>
		<!-- <uni-group title="图片展示" class="content-box">
		<view class="imgs" v-if="data.images">
			<block v-for="(img, index) in data.images" :key="index">
				<view class="imgs-box"><image :src="img" mode="aspectFill" style="width: 100%;height:100px;" @click="previewImg(img,data.images)"></image></view>
			</block>
		</view>
		</uni-group> -->

		</view>
		
		<uni-popup ref="openpopup">
		    <uni-list style="text-align: center;">
		        <uni-list-item title="设为己见" v-if="data.show" @click="changeShow()" clickable :show-extra-icon="true" :extra-icon="iconeyeslash"></uni-list-item>
		        <uni-list-item title="设为公开" v-if="!data.show" @click="changeShow()" clickable :show-extra-icon="true" :extra-icon="iconeye"></uni-list-item>
		        <uni-list-item title="删除数据" @click="delCheck()" clickable :show-extra-icon="true" :extra-icon="icondel"></uni-list-item>
		    </uni-list>
		</uni-popup>
		<uni-popup ref="popup">
			<uni-popup-dialog mode="base" title="确认删除"  :duration="0" :before-close="true" @close="delclose" @confirm="delconfirm"></uni-popup-dialog>
		</uni-popup>
		
	</view>
</template>

<script>
import cmdAvatar from "@/components/cmd-avatar/cmd-avatar.vue"
const start = 'static/ITkoala-amap/start.png'
export default {
	components: {cmdAvatar},
	data() {
		return {
			user: uni.getStorageSync('user'),
			page: 1,
			showadd: true,
			talk: '',
			iconeye: {
				color: '#6bcbda',
				size: '20',
				type: 'eye-filled'
			},
			iconeyeslash: {
				color: '#6bcbda',
				size: '20',
				type: 'eye-slash-filled'
			},
			icondel: {
				color: '#ce4d4d',
				size: '20',
				type: 'trash-filled'
			},
			// WinWidth: '375',
			data: {},
			talkData: [],
			markerList: [],
			dataIndex: '',
			dataID: null,
			dataname: '',
			typchiose: {
				play: '景玩',
				eat: '餐食',
				hotel: '住宿',
				go: '出行',
				other: '其他'
			}
		}
	},
	onLoad(option) {
		this.dataID = JSON.parse(decodeURIComponent(option.id))
		this.dataname = decodeURIComponent(option.name)
		// this.getwindowWidth()
		uni.setNavigationBarTitle({
			title: decodeURIComponent(option.name)
		})
		// this.getMapData()
	},
	mounted() {
		this.getMapData()
		this.getTalkData()
		// this.$nextTick(() => {
		// 	this.getMapData()
		// })
		// setTimeout(()=>{
		//     // this.list = list;
		//     this.getMapData()
		// },800)
	},
	methods: {
		dianzan(){
			console.log('dianzan')
			this.$http.post('place-praise/', {
				place: this.dataID,
				created_by: this.user
			}).then(res=> {
				setTimeout(()=>{
					this.$http.get('place/' + this.dataID + '/').then(res=> {
					if (res.data.code === 200) {
						this.data = res.data.data
					}
					})
				},300)
			})
		},
		quxiaozan(){
			console.log('quxiaozan')
			this.$http.del('place-praise/' + this.data.praise_id + '/').then(res=> {
				setTimeout(()=>{
					this.$http.get('place/' + this.dataID + '/').then(res=> {
					if (res.data.code === 200) {
						this.data = res.data.data
					}
					})
				},300)
			})
		},
		shoucang(){
			console.log('shoucang')
			this.$http.post('place-collect/', {
				place: this.dataID,
				created_by: this.user
			}).then(res=> {
				setTimeout(()=>{
					this.$http.get('place/' + this.dataID + '/').then(res=> {
					if (res.data.code === 200) {
						this.data = res.data.data
					}
					})
				},300)
			})
		},
		quxiaocang(){
			console.log('quxiaozan')
			this.$http.del('place-collect/' + this.data.collect_id + '/').then(res=> {
				setTimeout(()=>{
					this.$http.get('place/' + this.dataID + '/').then(res=> {
					if (res.data.code === 200) {
						this.data = res.data.data
					}
					})
				},300)
			})
		},
		posttalk(){
			if (this.talk !== '') {
				this.$http.post('place-talk/', {
					place: this.dataID,
					desc: this.talk,
				}).then(res=> {
					console.log(res.data)
					// 通过返回上级再回来刷新页面数据
					setTimeout(()=>{
						this.talk = ''
						// 通过重新请求数据来加载,而不是退回再进
						this.getTalkData()
					},500)
				})
			}
		},
		ToUser(id,name){
			console.log('userid', id)
			uni.navigateTo({
				url: '/pages/User/UserSelf' +'?id='+ encodeURIComponent(id) + '&name=' + encodeURIComponent(name)
			});
		},
		// 加载更多评论
		ShowMoreTalk(){
			this.page = this.page + 1
			this.$http.get('place-talk/?place=' + this.dataID + '&page=' + this.page).then(res=> {
			// console.log('talk', res.data)
			if (res.data.results.code === 200) {
				const nextTalkData = res.data.results.data
				this.talkData.push(...nextTalkData)
				if (this.talkData.length === res.data.count) {
					this.showadd = false
				}
			}
			})
		},
		// 删除评论
		deltalk(id){
			this.$http.del('place-talk/' + id + '/').then(res=> {
				console.log(res.data)
				// 通过返回上级再回来刷新页面数据
				setTimeout(()=>{
					this.getTalkData()
				},500)
			})
		},
		// 首次获取评论数据
		getTalkData(){
			this.$http.get('place-talk/?place=' + this.dataID + '&page=' + this.page).then(res=> {
			console.log(res.data)
			if (res.data.results.code === 200) {
				this.talkData = res.data.results.data
				if (this.talkData.length === res.data.count) {
					this.showadd = false
				}
			}
			})
		},
		// 获取屏幕宽度
		// getwindowWidth() {
		// 	uni.getSystemInfo({
		// 	    success: function (res) {
		// 	        console.log('1/3屏幕宽度', res.windowWidth / 3);
		// 			this.WinWidth = res.windowWidth
		// 	    }
		// 	});
		// },
		// 模拟从后台获取地图数据
		getMapData() {
			this.$http.get('place/' + this.dataID + '/').then(res=> {
			console.log(res.data)
			if (res.data.code === 200) {
				this.data = res.data.data
				this.markerList = [{lat:res.data.data.lat,lng:res.data.data.lng,icon: start}]
				}
			})
		},
		//地图点击回调事件
		onViewClick(params) {
			this.dataIndex = params.dataIndex
		},
		// 图片点击打开
		previewImg(src,urls){
			uni.previewImage({
				current:src,
				urls
			})
		},
		changeShow(){
			this.$http.put('place/' + this.dataID + '/', {name: this.data.name, show: ! this.data.show}).then(res=> {
			console.log(res.data)
			if (res.data.code === 200) {
				// 通过返回上级再回来刷新页面数据
				setTimeout(()=>{
					// h5
					// this.$router.go(0)
				
					// app
					uni.navigateBack({
						success: () => {
							uni.navigateTo({
								url: '/pages/Eider/PlaceEider' +'?id='+ encodeURIComponent(this.dataID) + '&name=' + encodeURIComponent(this.dataname)
							});
						}
					})
				},500)
			}
			})
		},
		openpop(){
			this.$refs.openpopup.open('center')
		},
		
		// 删除确认
		delCheck(){
			this.$refs.popup.open('center')
		},
		// 对话框关闭
		delclose() {
			// TODO 做一些其他的事情，before-close 为true的情况下，手动执行 close 才会关闭对话框
			// ...
			this.$refs.popup.close()
		},
		// 对话框确认
		delconfirm(value) {
			console.log('确认删除')
			// 输入框的值
			// console.log(value)
			
			// TODO 做一些其他的事情，手动执行 close 才会关闭对话框
			this.$http.del('place/' + this.dataID + '/').then(res=> {
				console.log(res.data)
				setTimeout(()=>{
					// h5
					// this.$router.go(-1)
					// setTimeout(()=>{
					// 	this.$router.go(0)
					// },500)

					// app 删除后回退到列表页，列表页没刷新，再次回退后重新进入列表
					uni.navigateBack({
						success: () => {
							uni.navigateBack({
								success: () => {
									uni.navigateTo({
										url: '/pages/User/MyPlace'
									});
								}
							})
						}
					})
				},500)
			})
			
			this.$refs.popup.close()
		}
	}
}
</script>

<script module="amap" lang="renderjs">
import config from '@/components/ITkoala-amap/config.js'

const selectedStart = 'static/ITkoala-amap/selectedStart.png' //选中的图片

export default {
	data() {
		return {
			map: null,
			ownerInstanceObj: null //service层对象
		}
	},
	mounted() {
		setTimeout(()=>{
		    // this.list = list;
		    if (typeof window.AMap === 'function') {
		    	this.initAmap()
		    } else {
		    	// 动态引入较大类库避免影响页面展示
		    	const script = document.createElement('script')
		    	script.src = 'https://webapi.amap.com/maps?v=1.4.15&key=' + config.WEBAK
		    	script.onload = this.initAmap.bind(this)
		    	document.head.appendChild(script)
		    }
		},800)
		
		// if (typeof window.AMap === 'function') {
		// 	this.initAmap()
		// } else {
		// 	// 动态引入较大类库避免影响页面展示
		// 	const script = document.createElement('script')
		// 	script.src = 'https://webapi.amap.com/maps?v=1.4.15&key=' + config.WEBAK
		// 	script.onload = this.initAmap.bind(this)
		// 	document.head.appendChild(script)
		// }
	},
	methods: {
		initAmap() {
			this.map = new AMap.Map('amap', {
				resizeEnable: true,
				center: [this.markerList[0].lng, this.markerList[0].lat],
				layers: [ //使用多个图层
					// new AMap.TileLayer.Satellite() //使用卫星图
				],
				zooms: [4, 18], //设置地图级别范围
				zoom: 16
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
						offset: new AMap.Pixel(-16, -33),
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
	height: 380rpx;
}
.amap-container {
	background-color: #ffffff;
}
.content-box {
	margin-top: 0px !important;
	min-height: 30px !important;
}
.my-tag {
	background-color: #b3ccd0 !important;
}
.imgs {
	// width: 94%;
	// margin-left: 3%;
	display: flex;
	flex-wrap: wrap;
	padding-top: 6upx;
	background-color: #ffffff;
	// box-shadow: 0px 2px 5px 2px red;
	// border: #b3ccd0;
	// border-style: double;
}
.imgs .imgs-box {
	width: 32%;
	margin-left: 1%;
	// height:32%;
	// padding-bottom:32%;
	// padding-right: 10upx;
	box-sizing: border-box;
}
.img-style {
	width: 100%;
	height: 110px;
}
.infoWindow-wrap{
	  margin-left: 50px;
		color: #f00;
	}
.talk-box {
	position: fixed;
	background-color: #FFFFFF;
	/* display: flex; */
	bottom: 0;
	left: 0;
	border-top: 1upx solid #b3ccd0;
	width: 100%;
	height: 100upx;
	z-index: 99;
}
</style>

<template>
	<view class="trip-eider">
		<view :prop="markerList" :change:prop="amap.updateEcharts" id="amap" v-if="markerList.length > 0"></view>
		<!-- <view class="">当前点击的对象的index值为：{{ dataIndex }}</view> -->
		
		<uni-card style="margin-top: 2px;margin-bottom: 10px;" v-if="markData && markerList.length > 0">
		<uni-list>
		    <uni-list-item
				:title="markData.place_name" 
				:thumb="markData.place_image"
				:note="markData.place_created_by_name + ' - ' + markData.place_created_date"
				thumb-size="lg"
				clickable
				@click="goToPage(markData.place_pagetyp,markData.place,markData.place_name)"
			></uni-list-item>
		</uni-list>
		</uni-card>
		
		<!-- <uni-icons type="trash-filled" size="20" class="delicon"></uni-icons> -->
		<!-- 封面 -->
		<!-- <view class="image-box"><image :src="data.image" class="face-image"></image></view> -->
		<uni-group title="摘要" class="trip-content-box" v-if="this.data.content">
				<uni-easyinput class="content-box" type="textarea"  v-model="this.data.content" disabled ></uni-easyinput>
		</uni-group>
		<uni-group :title="data.name" class="trip-desc-box">
			<view style="height: 1rpx;"></view>
			<uni-row >
			<uni-col :span="3" >
				<cmd-avatar :src="data.created_by_portrait" size="sm" @click="ToUser(data.created_by,data.created_by_name)"></cmd-avatar>
			</uni-col>
			<uni-col :span="19" style="margin-top: 5px;">
				<text style="font-weight: 600;font-size 28rpx;padding 4rpx;">{{data.created_by_name}}</text>
			</uni-col>
			<uni-col :span="2" style="margin-top: 10px;">
				<uni-icons type="more-filled" size="18"  @click="openpop()" style="float: right;"></uni-icons>
			</uni-col>
			</uni-row >
			
			<view style="height: 2px; margin-top: 5px; margin-bottom: 5px; border-bottom-style: inset;"></view>
			
			<!-- 内容-换服务器影响图片显示，图片尺寸过大显示不完整 -->
			<view auto-height v-html="data.desc" class="trip-desc"></view>
			
			<!-- <view style="height: 2px; margin-top: 5px; margin-bottom: 5px; border-bottom-style: inset;"></view> -->
			<uni-row style="margin-top: 5px;">
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
			
		</uni-group>
		<!-- <uni-card title="标题文字" thumbnail="https://vkceyugu.cdn.bspapp.com/VKCEYUGU-dc-site/460d46d0-4fcc-11eb-8ff1-d5dcf8779628.png" extra="额外信息" note="Tips">
		    内容主体，可自定义内容及样式
		</uni-card> -->
		<uni-group title="词条" class="trip-place-box" v-if="list.length > 0">
		<HM-dragSorts :list="list" :isLongTouch="true" :rowHeight="60" @change="change" @confirm="confirm" @onclick="onclick">
			<template slot="rowContent" slot-scope="{ row }">
				<view class="row" style="width: 95%;">
					<!-- 时间轴 -->
					<view style="width: 78px;float: left;font-size: 5px;color: #2C405A;" v-if="row.theDate || row.theBegin">
						<view style="height: 15px;"></view>
						<view v-if="row.theDate"><text class="text">{{row.theDate}}</text></view>
						<view v-if="row.theBegin"><text class="text">{{row.theBegin}}</text></view>
						<!-- <view v-if="row.theTime"><text class="text">H:{{row.theTime}}</text></view> -->
					</view>
					<view style="width: 55px;float: left;">
						<image v-if="row.icon" class="icon" :src="row.icon" style="width: 54px;height: 54px;margin-top: 4px;"></image>
					</view>
					
					<view style="float: left;">
					<view style="height: 45px;">
					<text class="text" style="font-size: 8px;font-weight: 600;">{{row.name}}</text>
					<view v-if="row.desc && row.desc.length < 20" style="font-size: 5px;color: #5f5f5f;"><text class="text">{{row.desc}}</text></view>
					<view v-if="row.desc && row.desc.length > 19" style="font-size: 5px;color: #5f5f5f;"><text class="text">{{row.desc.substring(0, 18) + '…'}}</text></view>
					</view>
					
					<view style="font-size: 5px;">
						<text class="text" v-if="row.theTime && row.theTime !== '0.0'" style="margin-left: 5px;">
							<!-- <uni-icons type="paperplane" size="5" style="margin-right: 2px;color: #00d8bb"></uni-icons> -->
							<image src="../../static/img/usetime.png" style="margin-right: 2px;width: 15px;height: 15px;"></image>
							{{row.theTime + ' h'}}
						</text>
						<text class="text" v-if="row.thePay && row.thePay !== '0.0'" style="margin-left: 5px;">
							<!-- <uni-icons type="spinner-cycle" size="5" style="margin-right: 2px;color: #eac500"></uni-icons> -->
							<image src="../../static/img/pay.png" style="margin-right: 2px;width: 15px;height: 15px;"></image>
							{{row.thePay + ' 元'}}
							</text>
					</view>
					</view>
					
				</view>
			</template>
		</HM-dragSorts>
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
		<button class="add-button" @click="addplace()">增加行程</button>
		
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
	const start = 'static/ITkoala-amap/start.png'
	export default {
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
				tripID: null,
				tripname: '',
				data: {},
				talkData: [],
				markerList: [],
				dataIndex: '',
				list: [],
				markData: {}
				// title: this.list[this.dataIndex].place_name
			}
		},
		mounted() {
			this.getMapData()
			this.getTalkData()
		},
		created() {
			// uni.setNavigationBarTitle({
			// 	title: this.tripname
			// })
		},
		methods: {
			dianzan(){
				console.log('dianzan')
				this.$http.post('trip-praise/', {
					trip: this.tripID,
					created_by: this.user
				}).then(res=> {
					setTimeout(()=>{
						this.$http.get('trip/' + this.tripID + '/').then(res=> {
						if (res.data.code === 200) {
							this.data = res.data.data
						}
						})
					},300)
				})
			},
			quxiaozan(){
				console.log('quxiaozan')
				this.$http.del('trip-praise/' + this.data.praise_id + '/').then(res=> {
					setTimeout(()=>{
						this.$http.get('trip/' + this.tripID + '/').then(res=> {
						if (res.data.code === 200) {
							this.data = res.data.data
						}
						})
					},300)
				})
			},
			shoucang(){
				console.log('shoucang')
				this.$http.post('trip-collect/', {
					trip: this.tripID,
					created_by: this.user
				}).then(res=> {
					setTimeout(()=>{
						this.$http.get('trip/' + this.tripID + '/').then(res=> {
						if (res.data.code === 200) {
							this.data = res.data.data
						}
						})
					},300)
				})
			},
			quxiaocang(){
				console.log('quxiaozan')
				this.$http.del('trip-collect/' + this.data.collect_id + '/').then(res=> {
					setTimeout(()=>{
						this.$http.get('trip/' + this.tripID + '/').then(res=> {
						if (res.data.code === 200) {
							this.data = res.data.data
						}
						})
					},300)
				})
			},
			posttalk(){
				if (this.talk !== '') {
					this.$http.post('trip-talk/', {
						trip: this.tripID,
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
				this.$http.get('trip-talk/?trip=' + this.tripID + '&page=' + this.page).then(res=> {
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
				this.$http.del('trip-talk/' + id + '/').then(res=> {
					console.log(res.data)
					// 通过返回上级再回来刷新页面数据
					setTimeout(()=>{
						this.getTalkData()
					},500)
				})
			},
			// 首次获取评论数据
			getTalkData(){
				this.$http.get('trip-talk/?trip=' + this.tripID + '&page=' + this.page).then(res=> {
				console.log(res.data)
				if (res.data.results.code === 200) {
					this.talkData = res.data.results.data
					if (this.talkData.length === res.data.count) {
						this.showadd = false
					}
				}
				})
			},
			goToPage(typ,id,name) {
				if (!id) return;
				uni.navigateTo({
					url: '/pages/tabbar/tabbar-1/'+ typ +'?id='+ encodeURIComponent(id) + '&name=' + encodeURIComponent(name)
				});
			},
			getMapData:function() {
				// 获取数据
				this.$http.get('trip/' + this.tripID + '/').then(res=> {
				console.log(res.data)
				if (res.data.code === 200) {
					this.data = res.data.data
					console.log('所有数据',this.data)
					this.list = res.data.data.places
					console.log('places',this.list)
					for (var i = 0; i < this.list.length; i++) {
						if ( this.list[i].lat && this.list[i].lng) {
							const marker = {lat:this.list[i].lat,lng:this.list[i].lng,icon: start}
							this.markerList.push(marker)
						}
					}
					console.log('列表',this.markerList)
					this.markData = this.list[0]
				}
				})
				
				
				
				// this.$http.get('place/' + this.tripID + '/').then(res=> {
				// console.log(res.data)
				// if (res.data.code === 200) {
				// 	this.data = res.data.data
				// 	this.markerList = [{lat:res.data.data.lat,lng:res.data.data.lng,icon: start}]
				// 	}
				// })
			},
			//地图点击回调事件
			onViewClick(params) {
				this.dataIndex = params.dataIndex - this.list.length
				this.markData = this.list[params.dataIndex - this.list.length]
				console.log('数据',this.markData)
			},
			addplace(id,name) {
				console.log('去搜索添加行程，提供地点和是否自己创建和时间筛选，类似购物点外卖筛选')
				// console.log(this.data.id,this.data.name)
				uni.navigateTo({
					url: '/pages/tabbar/tabbar-1/addtrip' +'?id='+ encodeURIComponent(this.data.id) + '&name=' + encodeURIComponent(this.data.name)
				});
				// pages/tabbar/tabbar-1/addtrip
			},
			onclick(e){
				console.log('=== onclick start 点击行，触发onclick事件 跳转页面进行编辑===');
				console.log("被点击行: " + JSON.stringify(e.value));
				console.log("被点击下标: " + JSON.stringify(e.index));
				uni.navigateTo({
					url: '/pages/Eider/PlaceInTrip' +'?id='+ encodeURIComponent(e.value.id) + '&name=' + encodeURIComponent(e.value.trip_name)
				});
				
				console.log('=== onclick end ===');
			},
			change(e){
				console.log('=== change start 拖拽过程中，行位置发生交换时，触发change事件 ===');
				// console.log("被拖动行: " + JSON.stringify(e.moveRow));
				// console.log("被拖动行id: ", e.moveRow.id);
				// console.log("被拖动行数据库顺序: ", e.moveRow.index);
				
				// console.log('原始下标：',e.index);
				// console.log('移动到：',e.moveTo);
				// console.log('=== change end ===');
			},
			changeIndex(id,index){
				this.$http.put('place-in-trip/' + id + '/', {index: index}).then(res=> {
				console.log(res.data)
				// if (res.data.code === 200) {
				// 	uni.showToast({title:'修改成功',icon:'none'})
				// }
				})
			},
			confirm(e){
				console.log('=== confirm start 拖拽结束且行位置发生了改变，触发confirm事件 ===');
				console.log("被拖动行: " + JSON.stringify(e.moveRow));
				console.log("被拖动行id: ", e.moveRow.id);
				console.log("被拖动行数据库顺序: ", e.moveRow.index);
				
				if (Number(e.moveTo) > Number(e.index)) {
					// 向后移
					for (var i = Number(e.index )+ 1; i < Number(e.moveTo) + 1 ; i++) {
						console.log("被拖动行id: ",this.list[i].id,'原始下标',this.list[i].index,'传入修改',i-1)
						this.changeIndex(this.list[i].id,i-1)
					}
				} else {
					// 向前移
					for (var i = Number(e.index )- 1; i > Number(e.moveTo) -1; i--) {
						console.log("被拖动行id: ",this.list[i].id,'原始下标',this.list[i].index,'传入修改',i+1)
						this.changeIndex(this.list[i].id,i+1)
					}
				}
				
				console.log("被拖动行id: ", Number(e.moveRow.id),'原始下标：',Number(e.index),'移动到：',Number(e.moveTo));
				this.changeIndex(Number(e.moveRow.id),Number(e.moveTo))
				
				uni.showToast({title:'修改成功',icon:'none'})
				console.log('=== confirm end ===');
				setTimeout(()=>{
					// h5
					// this.$router.go(0)
					this.getMapData()
					// app
					// uni.navigateBack({
					// 	success: () => {
					// 		// 因为直接跳转影响返回,所以到tab页面后再跳转
					// 		uni.navigateTo({
					// 			url: '/pages/Eider/TripEider' +'?id='+ encodeURIComponent(this.tripID) + '&name=' + encodeURIComponent(this.tripname)
					// 		});
					// 	}
					// })

				},500)
			},
			
			changeShow(){
				this.$http.put('trip/' + this.tripID + '/', {name: this.data.name, show: ! this.data.show}).then(res=> {
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
									url: '/pages/Eider/TripEider' +'?id='+ encodeURIComponent(this.tripID) + '&name=' + encodeURIComponent(this.tripname)
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
				this.$http.del('trip/' + this.tripID + '/').then(res=> {
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
											url: '/pages/User/MyTrip'
										});
									}
								})
							}
						})
					},500)
				})
				
				this.$refs.popup.close()
			}
		},
		onLoad(option) {
			this.tripID = JSON.parse(decodeURIComponent(option.id));
			uni.setNavigationBarTitle({
				title: decodeURIComponent(option.name)
			});
			// this.$http.get('trip/' + this.tripID + '/').then(res=> {
			// console.log(res.data)
			// if (res.data.code === 200) {
			// 	this.data = res.data.data
			// 	this.list = res.data.data.places
			// 	console.log(this.data)
			// 	uni.setNavigationBarTitle({
			// 		title: this.data.name
			// 	})
			// }
			// })
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
		this.getMapData()
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
				zoom: 11
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
    //scoped css只在当前页生效 不影响子组件
    page {background-color: #efeff4;}
    @media (prefers-color-scheme: dark){page {background-color: #000000;} }
    .content {.row{display: flex;flex-direction: row;align-items: center;.icon{width: 30px;border-radius: 6px;margin-right: 13px;}.text{font-size: 13px;}}}
</style>

<style lang="scss" scoped>
#amap {
	width: 100%;
	height: 380rpx;
}

.infoWindow-wrap{
	  margin-left: 50px;
		color: #f00;
	}
</style>

<style>
.trip-eider {
	min-height: 100vh;
}
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
.trip-content-box {
	margin-top: 0px;
	margin: 0px !important;
}
/deep/.trip-place-box .uni-group__content{
	padding: 0px !important;
}
/deep/.content-box .uni-easyinput__content .uni-easyinput__content-textarea {
	min-height: 50px !important;
	height: 50px !important;
}
.trip-desc-box {
	margin: 0px !important;
}
.trip-desc {
	width: 100%;
	word-break: break-all;
}
.add-button {
	margin-top: 10px;
	color: #b3ccd0;
}
/* .add-button:after {
	border: 1px solid rgba(0,0,0,.2);
	border-style: dashed;
} */
/deep/.uni-list--border-top {
	height: 0px !important;
}
/deep/.uni-list--border-bottom {
	height: 0px !important;
}
/deep/.uni-card {
	padding: 0px !important;
	margin: 5px 0px !important;
}
/deep/.uni-card__content {
	padding: 2px !important;
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

<template>
	<view>
		<uni-nav-bar class="nav-box" backgroundColor="#b3ccd0" fixed>
			<view solt="default" style="margin-left: -65px;">
				<uni-easyinput class="search-box" :inputBorder="false" prefixIcon="search"  v-model="searchData" placeholder="请输入内容" @iconClick="onClick" clearable ></uni-easyinput>
			</view>
		</uni-nav-bar>
		<HM-filterDropdown 
			:menuTop="90" 
			:filterData="filterData" 
			:defaultSelected="defaultSelected"
			:updateMenuName="true" 
			@confirm="confirm"
			color="red"
			dataFormat="Object">
		</HM-filterDropdown>
		<view style="margin-top: 80rpx;">
			<me-select 
			ref="meSelect" 
			@change="change" 
			@finish="finish" 
			@itemClick="itemClick" 
			:datalist="placeData"
			:options="options"
			>
				<view slot-scope="slot" class="item">
					<uni-card>
					<uni-list>
					    <uni-list-item
							:title="slot.slotScope.item.name" 
							:thumb="slot.slotScope.item.image"
							:note="slot.slotScope.item.created_by_name + ' - ' + slot.slotScope.item.created_date"
							thumb-size="lg"
							clickable
							@click="goToPage(slot.slotScope.item.pagetyp,slot.slotScope.item.id,slot.slotScope.item.name)"
						></uni-list-item>
					</uni-list>
					</uni-card>
				   <!-- 这里可以写自己的模板 -->
					<!-- <uni-card 
					@click="goToPage(slot.slotScope.item.pagetyp,slot.slotScope.item.id,slot.slotScope.item.name)"
					>
					<view>{{slot.slotScope.item.id}}</view>
					</uni-card> -->
				</view>
			</me-select>
			<!-- <button @click="changeModel">编辑/取消</button> -->
			<!-- <button @click="getSelectAll">获取所有选中的列表</button> -->
			<!-- <choiselist :data="placeData"></choiselist> -->
		</view>
		<view style="height: 60px;"></view>
		<!-- <button style="margin-top: 120px;" @click="getSearch">查询增加地点</button> -->
	</view>
</template>

<script>
	// import choiselist from '@/components/ChoiseList/ChoiseList.vue'
	import meSelect from '@/components/me-select/tripinblog-select.vue'
	export default {
		components: {
			meSelect
		},
		data() {
			return {
				headerTop: null,
				dataID: null,
				dataname:'',
				page: 1,
				isNewRenderDone:true,//锁的作用
				searchData: '',
				options: {
					flags: ['id','name','typ'], //设置需要返回的参数这个参数必须在 dataList 中的item中存在（不配置默认全部返回）
					itemCanSelect: true //是否开启点击列表页选择配置
				},
				data: {},
				indexArr: '',
				valueArr: '',
				filterData: [
					// {
					// 	name: '所在城市',
					// 	type: 'hierarchy-column',
					// 	submenu: []
					// },
					{
						name: '类型',
						type: 'radio',
						submenu: [{
							name: '词条分类',
							submenu: [
								{
									name: '餐食',
									value: 'eat'
								},
								{
									name: '住宿',
									value: 'hotel'
								},
								{
									name: '出行',
									value: 'go'
								},
								{
									name: '景玩',
									value: 'play'
								}
							]
						}]
					},
					{
						name: '归属',
						type: 'radio',
						submenu: [{
							name: '词条归属',
							submenu: [
								{
									name: '全部',
									value: 'all'
								},
								{
									name: '公开',
									value: 'show'
								},
								{
									name: '私有',
									value: 'my'
								}
							]
						}]
					},
					{
						name: '状态',
						type: 'radio',
						submenu: [{
							name: '状态类型',
							submenu: [
								{
									name: '赞过',
									value: 'praise'
								},
								{
									name: '收藏',
									value: 'collect'
								},
								{
									name: '关注',
									value: 'follow'
								}
							]
						}]
					},
					
				],
				defaultSelected: [],
				placeData: [],
				typChoise: {
					play: '观赏游玩',
					eat: '用餐',
					hotel: '休憩',
					go: '搭乘出行'
				}
			}
		},
		created() {
			this.getSearch()
		},
		mounted() {
			// setTimeout(() => {
			// 	this.getCitySearch()
			// 	console.log(this.filterData)
			// }, 100);
		},
		methods: {
			getLoadNum(num){
				console.log('共加载了:'+num);
				!this.isNewRenderDone&&uni.hideLoading()
				this.isNewRenderDone = true
			},
			goToPage(typ,id,name) {
				if (!id) return;
				uni.navigateTo({
					url: '/pages/tabbar/tabbar-1/'+ typ +'?id='+ encodeURIComponent(id) + '&name=' + encodeURIComponent(name)
				});
			},
			// getCitySearch(){
			// 	this.$http.get('city-search/').then(res=> {
			// 	if (res.data.code === 200) {
			// 		for (let i = 0; i < res.data.data.length; i++) {
			// 		this.filterData[0].submenu.push(res.data.data[i])
			// 		}
			// 	}
			// 	})
			// 	console.log('last', this.filterData)
			// },
			//接收菜单结果
			confirm(e) {
				this.indexArr = e.index;
				this.valueArr = e.value;
			
			},
			getSearch(){
				// 497 'eat' 'show' 'collect'
				this.page = 1
				if (this.valueArr === '') {
					if ( this.searchData !== '') {
						this.$http.get('trip/?page='+this.page + '&search=' + this.searchData).then(res=> {
						if (res.data.results.code === 200) {
							console.log(res.data.results.data)
							this.placeData = res.data.results.data
						}
						})
					} else {
						this.$http.get('trip/?page='+this.page).then(res=> {
						if (res.data.results.code === 200) {
							console.log(res.data.results.data)
							this.placeData = res.data.results.data
						}
						})
					}
					
				} else {
					const search =  '?typ=' + this.valueArr[1][0][0] + '&belong='+ this.valueArr[2][0][0] + '&show=' + this.valueArr[3][0][0]
					console.log(search)
					if (this.searchData !== '') {
						this.$http.get('trip/'+ search + '&page='+this.page + '&search=' + this.searchData).then(res=> {
						if (res.data.results.code === 200) {
							console.log(res.data.results.data)
							this.placeData = res.data.results.data
						}
						})
					} else {
						this.$http.get('trip/'+ search + '&page='+this.page).then(res=> {
						if (res.data.results.code === 200) {
							console.log(res.data.results.data)
							this.placeData = res.data.results.data
						}
						})
					}
					
				}
			},
			changeModel() {
				this.$refs.meSelect.changeModel()
			},
			getSelectAll() {
				var result = this.$refs.meSelect.getSelectAll()
				console.log('当前全选：', result)
			},
			itemClick(e) {
				console.log('列表点击了：', e)
			},
			finish(e) {
				console.log('所有的选择：', e)
				this.$http.put('blog/' + this.dataID + '/', {
					name: this.dataname,
					trip: e[0].id,
				}).then(res=> {
					console.log(res.data)
				})
					
				setTimeout(()=>{
					// app 返回上一页
					uni.navigateBack({
						success: () => {
							uni.navigateBack({
								success: () => {
									// 因为直接跳转影响返回,所以到tab页面后再跳转
									uni.navigateTo({
										url: '/pages/Eider/BlogEider' +'?id='+ encodeURIComponent(this.dataID) + '&name=' + encodeURIComponent(this.dataname)
									});
								}
							})
						}
					})
				},600)

			},
			change(e) {
				console.log('发生改变了：', e)
			}
		},
		watch: {
			valueArr(){
				this.getSearch()
			},
			searchData(){
				this.getSearch()
			}
		},
		onLoad(option) {
			this.dataID = JSON.parse(decodeURIComponent(option.id))
			this.dataname = decodeURIComponent(option.name)
			uni.setNavigationBarTitle({
				title: decodeURIComponent(option.name)
			})
		},
		onReachBottom() {
			console.log('onReachBottom');
			// 加锁，避免在加载更多时用户频繁下拉导致的重复触发而渲染异常
			// if(!this.isNewRenderDone) return;   
			// this.isNewRenderDone = false
			// uni.showLoading({title:'正在加载更多'})
			// 模拟分页请求 (加载更多)
			// setTimeout(()=>{
			this.page = this.page + 1
			// this.nextData = []
			if (this.valueArr === '') {
				if ( this.searchData !== '') {
					this.$http.get('trip/?page='+this.page + '&search=' + this.searchData).then(res=> {
					if (res) {
						if (res.data.results.code === 200) {
							console.log(res.data.results.data)
							this.nextData = res.data.results.data
						}
					}  else {
						uni.showToast({title:'总该有个结尾吧~',icon:'none'})
					}
					
					})
				} else {
					this.$http.get('trip/?page='+this.page).then(res=> {
					if (res) {
						if (res.data.results.code === 200) {
							console.log(res.data.results.data)
							this.nextData = res.data.results.data
						}
					}  else {
						uni.showToast({title:'总该有个结尾吧~',icon:'none'})
					}
					
					})
				}
				
			} else {
				const search =  '?city=' + this.valueArr[0][2] + '&typ=' + this.valueArr[1][0][0] + '&belong='+ this.valueArr[2][0][0] + '&show=' + this.valueArr[3][0][0]
				console.log(search)
				if (this.searchData !== '') {
					this.$http.get('trip/'+ search + '&page='+this.page + '&search=' + this.searchData).then(res=> {
					if (res) {
						if (res.data.results.code === 200) {
							console.log(res.data.results.data)
							this.nextData = res.data.results.data
						}
					}  else {
						uni.showToast({title:'总该有个结尾吧~',icon:'none'})
					}
					
					})
				} else {
					this.$http.get('trip/'+ search + '&page='+this.page).then(res=> {
					if (res) {
						if (res.data.results.code === 200) {
							console.log(res.data.results.data)
							this.nextData = res.data.results.data
						}
					}  else {
						uni.showToast({title:'总该有个结尾吧~',icon:'none'})
					}
					
					})
				}
				
			}
			
			// const nextData = JSON.parse(JSON.stringify(this.list.slice(0,10)))
			this.placeData.push(...this.nextData)
			this.nextData = []
			console.log('残余数据', this.nextData)
			// this.$nextTick(()=>{
			//     this.$refs.wfalls.handleViewRender();
			// })
			// APP上触发不了还是setTimeout万能
			setTimeout(()=>{
				// this.isNewRenderDone = true
				this.nextData = []
			},0)
			// },800)
		},
		onPullDownRefresh() {
			// 模拟更新新数据
			// const newData = JSON.parse(JSON.stringify(this.list.slice(0,10)))
			setTimeout(()=>{
				this.page = 1
				this.getSearch()
				// this.$refs.wfalls.init()
				uni.stopPullDownRefresh()
				uni.showToast({title:'刷新成功',icon:'none'})
			},800)
		}
	}
</script>

<style>
.search-box {
	background-color: #ffffff;
	border-radius:100px;
	height: 35px;
	line-height: 35px;
	width: -webkit-calc(100% + 130px) !important;;
}
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
</style>

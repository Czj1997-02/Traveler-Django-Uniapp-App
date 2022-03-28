<template>
	<view class="content">
		<uni-nav-bar class="nav-box" backgroundColor="#b3ccd0" fixed>
			<view solt="default" style="margin-left: -65px;">
				<uni-easyinput class="search-box" :inputBorder="false" prefixIcon="search"  v-model="searchData" placeholder="请输入内容" @iconClick="onClick" clearable ></uni-easyinput>
			</view>
		    <view slot="right" class="city-box" @click="goCityChoice"><uni-icons type="location-filled" size="25" color="#494e75"></uni-icons>{{this.city}}</view>
		</uni-nav-bar>
		<view>
			<wfalls-flow :list="blogData" ref="wfalls" @finishLoad="getLoadNum"></wfalls-flow>
		</view>
		<image src="../../static/logo.png" style="width: 100%;" v-if="blogData.length===0"></image>
		<view style="height: 20upx;"></view>
	</view>
</template>

<script>
// import wfallsFlow from '../../components/wfalls-flow/wfalls-flow-place.vue'
import wfallsFlow from '@/components/wfalls-flow/wfalls-flow'
// const list = require('@/static/wfalls-flow/data.json').list
export default {
	// components: {
	// 	wfallsFlow
	// },
	data() {
		return {
			defaultIndex: 0,
			city: '',
			cityid: '',
			searchData: '',
			current: 0,
			list:[],
			isNewRenderDone:false,//锁的作用
			blogData: [],
			nextData: [],
			tags: 1,
			page: 1,
			noticeData: null
		}
	},
	created() {
		this.getUserData()//获得用户所在城市方便推送信息
		this.getBlogData()
	},
	methods: {
		goToPage(url) {
			if (!url) return;
			uni.navigateTo({
				url
			});
		},
		getUserData () {
			// this.city = uni.getStorageSync('city')
			this.$http.get('myself/').then(res=> {
			// console.log(res.data)
			if (res.data.code === 200) {
				this.cityid = res.data.data[0].city
				this.city = res.data.data[0].cityname
			}
			console.log('城市id',this.cityid,this.city)
			})
		},
		goCityChoice () {
			console.log(this.city)
			// uni.navigateTo({
			// 	url: '/pages/tabbar/tabbar-1/CityChoice?oldcity='+ encodeURIComponent(this.cityid)
			// })
		},
		onClick () {
			console.log(this.searchData)
			setTimeout(()=>{
			    // this.list = list;
			    this.getBlogData()
				console.log('切换加载', this.blogData)
			    this.$refs.wfalls.init()
				setTimeout(()=>{
					this.$refs.wfalls.init()
					console.log('此时数据：',this.blogData)
				},500)
				// this.$forceUpdate();
			},500)
		},
		changecurrent(e) {
			this.current = e.detail.current
			console.log(this.current)
		},
		getLoadNum(num){
			console.log('共加载了:'+num);
			!this.isNewRenderDone&&uni.hideLoading()
			this.isNewRenderDone = true
		},
		getBlogData(){
			this.nextData = []
			this.page = 1
			if ( this.searchData !== '') {
				this.$http.get('place/?typ=go' + '&page=' + this.page + '&search=' + this.searchData).then(res=> {
				if (res) {
					// console.log(res.data)
					if (res.data.results.code === 200) {
						this.blogData = res.data.results.data
						// console.log(this.blogData)
					} else {
						this.blogData = []
					}
				} else {
					this.blogData = []
				}
				})
			} else {
				this.$http.get('place/?typ=go' + '&page=' + this.page).then(res=> {
				if (res) {
					// console.log(res.data)
					if (res.data.results.code === 200) {
						this.blogData = res.data.results.data
						// console.log(this.blogData)
					} else {
						this.blogData = []
					}
				} else {
					this.blogData = []
				}
				})
			}
			
		},
		tabClick(index) {
			// 获取点击的数据
			console.log(this.blogtype[index].id)
			this.page = 1
			this.tags = this.blogtype[index].id
			// 修改tags
			setTimeout(()=>{
			    // this.list = list;
			    this.getBlogData()
				console.log('切换加载', this.blogData)
			    this.$refs.wfalls.init()
				setTimeout(()=>{
					this.$refs.wfalls.init()
					console.log('此时数据：',this.blogData)
				},500)
				// this.$forceUpdate();
			},500)
			// this.$forceUpdate();
		}
	},
	watch: {
		// tags(newVal,oldVal){
		// 	this.tabClick(index)
		// }
		searchData(){
			this.onClick()
		}
	},
	onLoad(option) {
		// const blogtype = JSON.parse(decodeURIComponent(option.blogtype));
		// console.log(blogtype)
		// 模拟首次加载列表数据
		setTimeout(()=>{
		    // this.list = list;
		    this.getBlogData()
			console.log('首次加载', this.blogData)
		    this.$refs.wfalls.init();
		},1000)
	},
	onReachBottom() {
		console.log('onReachBottom');
		// 加锁，避免在加载更多时用户频繁下拉导致的重复触发而渲染异常
		if(!this.isNewRenderDone) return;   
		this.isNewRenderDone = false
		uni.showLoading({title:'正在加载更多'})
		// 模拟分页请求 (加载更多)
		setTimeout(()=>{
			this.page = this.page + 1
			// this.nextData = []
			if (this.searchData !== '') {
				this.$http.get('place/?typ=go' + '&page=' + this.page + '&search=' + this.searchData).then(res=> {
				if (res) {
					console.log(res)
					if (res.data.results.code === 200) {
						this.nextData = res.data.results.data
					}
				} else {
					uni.showToast({title:'总该有个结尾吧~',icon:'none'})
				}
				// if (res.data.results.code !== 200) {
				// 	uni.showToast({title:'已经到底了',icon:'none'})
				// }
				})
			} else {
				this.$http.get('place/?typ=go' + '&page=' + this.page).then(res=> {
				if (res) {
					console.log(res)
					if (res.data.results.code === 200) {
						this.nextData = res.data.results.data
					}
				} else {
					uni.showToast({title:'总该有个结尾吧~',icon:'none'})
				}
				// if (res.data.results.code !== 200) {
				// 	uni.showToast({title:'已经到底了',icon:'none'})
				// }
				})
			}
			
			// const nextData = JSON.parse(JSON.stringify(this.list.slice(0,10)))
			this.blogData.push(...this.nextData)
			this.nextData = []
			console.log('残余数据', this.nextData)
			// this.$nextTick(()=>{
			//     this.$refs.wfalls.handleViewRender();
			// })
			// APP上触发不了还是setTimeout万能
			setTimeout(()=>{
				this.$refs.wfalls.handleViewRender();
				this.nextData = []
			},0)
		},800)
	},
	onPullDownRefresh() {
		// 模拟更新新数据
		// const newData = JSON.parse(JSON.stringify(this.list.slice(0,10)))
		setTimeout(()=>{
			this.page = 1
			this.getBlogData()
			this.$refs.wfalls.init()
			uni.stopPullDownRefresh()
			uni.showToast({title:'刷新成功',icon:'none'})
		},800)
	}
};
</script>

<style>
.content {
	min-height: 100vh;
	/* background-color: #b3ccd0 !important; */
}
/* .nav-box {
	border: 0px;
} */
/deep/.uni-navbar--border {
    border: 0px !important;
}
.search-box {
	background-color: #ffffff;
	border-radius:100px;
	height: 35px;
	line-height: 35px;
	width: -webkit-calc(100% + 60px) !important;;
}
.city-box {
	margin-left: -30px;
	color: #494e75;
	font-weight: 600;
	max-height: 45px;
	overflow: hidden;
	/* word-break: break-all; */  /* break-all(允许在单词内换行。) */
	text-overflow: ellipsis;  /* 超出部分省略号 */
	display: -webkit-box; /** 对象作为伸缩盒子模型显示 **/
	-webkit-box-orient: vertical; /** 设置或检索伸缩盒对象的子元素的排列方式 **/
	-webkit-line-clamp: 3; /** 显示的行数 **/
}
.home-page-box {
	position: relative;
	display: flex;
	width: 90%;
	margin-top: 15upx;
	margin-left: 5%;
	background: #fff;
	border-radius: 20upx;
	padding: 20upx 20upx;
	box-sizing: border-box;
	z-index: 2;
	box-shadow: 0px 2px 5px 2px rgba(0, 0, 0, 0.1);
}
.home-page-box-item {
	width: 50px;
	height: 70px;
	margin-left: -webkit-calc((100% - 250px) / 6) !important;;
	text-align: center;
	position: relative;
}
.box-image {
	width: 50px;
	height: 50px;
	/* display:flex; */
	/* flex-direction:row; */
	/* align-items:center; */
}
.explain {
	/* display:flex; */
	/* flex-direction:row; */
	/* align-items:center; */
}
.home-data-box {
	position: relative;
	display: flex;
	width: 90%;
	margin-top: 20upx;
	margin-left: 5%;
	/* margin-bottom: 20upx; */
	background: #fff;
	border-radius: 20upx;
	padding: 20upx 20upx;
	box-sizing: border-box;
	z-index: 2;
	box-shadow: 0px 2px 5px 2px rgba(0, 0, 0, 0.1);
}

/* /deep/.uni-noticebar__content-text */
/deep/.uni-noticebar__content-text--scrollable {
	animation-delay: -10.32s !important;
	animation-duration: 10.32s !important;
}
</style>

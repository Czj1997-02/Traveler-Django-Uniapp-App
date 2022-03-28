<template>
	<view>
		<view style="background-color: #b3ccd0;height: 90px;">
			<view class="portrait-box" style="text-align: center;"><image :src="userdata.portrait_src" mode="aspectFill" class="img-style"  @click="previewImg(userdata.portrait_src,[userdata.portrait_src])"></image></view>
			<!-- 操作组 -->
		</view>
		
		<view style="text-align: center;background-color: #b3ccd0;height: 30px;" >
			关注:{{userdata.guanzhu}}&nbsp;&nbsp;&nbsp;&nbsp;粉丝:{{userdata.fensi}}
			<text style="font-weight: 600;margin-left: 20px;border-bottom-style: inset;" v-if="!userdata.is_follow && userid !== user" @click="follow">关注</text>
			<text style="font-weight: 600;margin-left: 20px;border-bottom-style: inset;" v-if="userdata.is_follow && userid !== user" @click="unfollow">取消关注</text>
		</view>
		
		<view style="margin-top: 10upx;">
			<liuyuno-tabs :tabData="blogtype" :defaultIndex="defaultIndex" @tabClick='tabClick' />
		</view>
		<view>
			<wfalls-flow :list="blogData" ref="wfalls" @finishLoad="getLoadNum"></wfalls-flow>
		</view>
		<image src="../../static/logo.png" style="width: 100%;" v-if="blogData.length===0"></image>
		<view style="height: 20upx;"></view>
		
	</view>
</template>

<script>
	import wfallsFlow from '@/components/wfalls-flow/wfalls-flow'
	export default {
		data() {
			return {
				user: uni.getStorageSync('user'),
				userdata: {},
				userid: null,
				realname: '',
				blogtype: [
					{
						id: 1,
						typ: 'blog',
						name: '图文'
					},
					{
						id: 2,
						typ: 'place',
						name: '地点'
					},
					{
						id: 3,
						typ: 'trip',
						name: '行程'
					},
				],
				blogData: [],
				nextData: [],
				defaultIndex: 0,
				isNewRenderDone:false,//锁的作用
				tags: 1,
				typ: 'blog',
				page: 1,
				noticeData: null
			}
		},
		mounted() {
			setTimeout(()=>{
			    // this.list = list;
			    this.getBlogData()
				console.log('首次加载', this.blogData)
			    this.$refs.wfalls.init();
			},1000)
		},
		methods: {
			getLoadNum(num){
				console.log('共加载了:'+num);
				!this.isNewRenderDone&&uni.hideLoading()
				this.isNewRenderDone = true
			},
			follow(){
				this.$http.post('follow/', {
					created_by: this.user,
					follow: this.userid,
				}).then(res=> {
					console.log(res.data)
					// 通过返回上级再回来刷新页面数据
					setTimeout(()=>{
						// h5
						// this.$router.go(0)
						// app
						uni.navigateBack({
							success: () => {
								uni.navigateTo({
									url: '/pages/User/UserSelf' +'?id='+ encodeURIComponent(this.userid) + '&name=' + encodeURIComponent(this.realname)
								});
							}
						})
					},500)
				})
			},
			unfollow(){
				this.$http.del('follow/' + this.userdata.follow_id + '/').then(res=> {
					console.log(res.data)
						// 通过返回上级再回来刷新页面数据
						setTimeout(()=>{
							// h5
							// this.$router.go(0)
							// app
							uni.navigateBack({
								success: () => {
									uni.navigateTo({
										url: '/pages/User/UserSelf' +'?id='+ encodeURIComponent(this.userid) + '&name=' + encodeURIComponent(this.realname)
									});
								}
							})
						},500)
					})
			},
			// 图片点击打开
			previewImg(src,urls){
				uni.previewImage({
					current:src,
					urls
				})
			},
			tabClick(index) {
				// 获取点击的数据
				console.log(this.blogtype[index])
				this.page = 1
				this.typ = this.blogtype[index].typ
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
				this.$forceUpdate();
			},
			getBlogData(){
				this.nextData = []
				this.page = 1

				this.$http.get(this.typ+'/?follower=' + this.userid + '&page=' + this.page).then(res=> {
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
				
			},
		},
		onLoad(option) {
			const id = JSON.parse(decodeURIComponent(option.id))
			
			this.userid = JSON.parse(decodeURIComponent(option.id))
			this.realname = decodeURIComponent(option.name)
			
			this.$http.get('user-extension/' + id + '/').then(res=> {
			console.log(res.data)
			if (res.data.code === 200) {
				this.userdata = res.data.data
				console.log(this.userdata)
				uni.setNavigationBarTitle({
					title: this.userdata.realname
				})
			}
			})
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

				this.$http.get(this.typ+'/?follower=' + this.userid + '&page=' + this.page).then(res=> {
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
	}
</script>

<style>
.img-style {
	width: 80px;
	height: 80px;
}
</style>

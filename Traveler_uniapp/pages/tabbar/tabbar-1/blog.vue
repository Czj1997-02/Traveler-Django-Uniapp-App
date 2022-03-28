<template>
	<view>
		<!-- <uni-icons type="trash-filled" size="20" class="delicon"></uni-icons> -->
		<!-- 封面 -->
		<!-- <view class="image-box"><image :src="data.image" class="face-image"></image></view> -->
		<uni-group title="摘要" class="blog-content-box" v-if="this.data.content">
				<uni-easyinput class="content-box" type="textarea"  v-model="this.data.content" disabled ></uni-easyinput>
		</uni-group>
		<uni-group title="关联行程" class="blog-content-box" v-if="this.data.trip">
			<!-- <view>{{this.data.trip}}</view> -->
			<uni-card style="margin-top: 2px;margin-bottom: 10px;" v-if="this.data.trip">
			<uni-list>
				<uni-list-item
					:title="this.data.trip_name" 
					:thumb="this.data.trip_image"
					:note="this.data.trip_created_by + ' - ' + this.data.trip_created_date"
					thumb-size="lg"
					clickable
					@click="goToPage(data.trip,data.trip_name)"
				></uni-list-item>
			</uni-list>
			</uni-card>
		</uni-group>
		<uni-group :title="data.name" class="blog-desc-box">
			
			<view style="height: 1rpx;"></view>
			<uni-row >
			<uni-col :span="3" >
				<cmd-avatar :src="data.created_by_portrait" size="sm" @click="ToUser(data.created_by,data.created_by_name)"></cmd-avatar>
			</uni-col>
			<uni-col :span="21" style="margin-top: 5px;">
				<text style="font-weight: 600;font-size 28rpx;padding 4rpx;">{{data.created_by_name}}</text>
			</uni-col>
			<!-- <uni-col :span="2" style="margin-top: 10px;"> -->
				<!-- <uni-icons type="more-filled" size="18"  @click="openpop()" style="float: right;"></uni-icons> -->
			<!-- </uni-col> -->
			</uni-row >
			
			<view style="height: 2px; margin-top: 5px; margin-bottom: 5px; border-bottom-style: inset;"></view>
			
			<!-- 内容-换服务器影响图片显示，图片尺寸过大显示不完整 -->
			<view auto-height v-html="data.desc" class="blog-desc"></view>
			
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
								<uni-col :span="2" v-if="item.created_by == user || data.created_by == user"><uni-icons type="trash-filled" size="18"  @click="deltalk(item.id)" style="float: right;"></uni-icons></uni-col>
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
	export default {
		data() {
			return {
				page: 1,
				showadd: true,
				talk: '',
				data: {},
				talkData: [],
				user: uni.getStorageSync('user'),
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
				dataID: null,
				dataname: ''
			}
		},
		mounted() {
			this.getTalkData()
		},
		methods: {
			dianzan(){
				console.log('dianzan')
				this.$http.post('blog-praise/', {
					blog: this.dataID,
					created_by: this.user
				}).then(res=> {
					setTimeout(()=>{
						this.$http.get('blog/' + this.dataID + '/').then(res=> {
						if (res.data.code === 200) {
							this.data = res.data.data
						}
						})
					},300)
				})
			},
			quxiaozan(){
				console.log('quxiaozan')
				this.$http.del('blog-praise/' + this.data.praise_id + '/').then(res=> {
					setTimeout(()=>{
						this.$http.get('blog/' + this.dataID + '/').then(res=> {
						if (res.data.code === 200) {
							this.data = res.data.data
						}
						})
					},300)
				})
			},
			shoucang(){
				console.log('shoucang')
				this.$http.post('blog-collect/', {
					blog: this.dataID,
					created_by: this.user
				}).then(res=> {
					setTimeout(()=>{
						this.$http.get('blog/' + this.dataID + '/').then(res=> {
						if (res.data.code === 200) {
							this.data = res.data.data
						}
						})
					},300)
				})
			},
			quxiaocang(){
				console.log('quxiaozan')
				this.$http.del('blog-collect/' + this.data.collect_id + '/').then(res=> {
					setTimeout(()=>{
						this.$http.get('blog/' + this.dataID + '/').then(res=> {
						if (res.data.code === 200) {
							this.data = res.data.data
						}
						})
					},300)
				})
			},
			goToPage(id,name) {
				if (!id) return;
				uni.navigateTo({
					url: '/pages/tabbar/tabbar-1/trip' +'?id='+ encodeURIComponent(id) + '&name=' + encodeURIComponent(name)
				});
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
				this.$http.get('blog-talk/?blog=' + this.dataID + '&page=' + this.page).then(res=> {
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
			// 发布评论
			posttalk(){
				if (this.talk !== '') {
					this.$http.post('blog-talk/', {
						blog: this.dataID,
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
			// 删除评论
			deltalk(id){
				this.$http.del('blog-talk/' + id + '/').then(res=> {
					console.log(res.data)
					// 通过返回上级再回来刷新页面数据
					setTimeout(()=>{
						this.getTalkData()
					},500)
				})
			},
			// 首次获取评论数据
			getTalkData(){
				this.$http.get('blog-talk/?blog=' + this.dataID + '&page=' + this.page).then(res=> {
				console.log('talk', res.data)
				if (res.data.results.code === 200) {
					this.talkData = res.data.results.data
					if (this.talkData.length === res.data.count) {
						this.showadd = false
					}
				}
				})
			},
			changeShow(){
				this.$http.put('blog/' + this.dataID + '/', {name: this.data.name, show: ! this.data.show}).then(res=> {
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
									url: '/pages/Eider/BlogEider' +'?id='+ encodeURIComponent(this.dataID) + '&name=' + encodeURIComponent(this.dataname)
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
				this.$http.del('blog/' + this.dataID + '/').then(res=> {
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
											url: '/pages/User/MyBlog'
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
			const id = JSON.parse(decodeURIComponent(option.id))
			this.dataID = JSON.parse(decodeURIComponent(option.id))
			this.dataname = decodeURIComponent(option.name)
			this.$http.get('blog/' + id + '/').then(res=> {
			console.log(res.data)
			if (res.data.code === 200) {
				this.data = res.data.data
				console.log(this.data)
				uni.setNavigationBarTitle({
					title: this.data.name
				})
			}
			})
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
	margin: 0px !important;
}
.blog-desc {
	width: 100%;
	word-break: break-all;
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
.uni-comment {
        padding: 5rpx 0;
        display: flex;
        flex-grow: 1;
        flex-direction: column;
    }

    .uni-comment-list {
        flex-wrap: nowrap;
        padding: 10rpx 0;
        margin: 10rpx 0;
        width: 100%;
        display: flex;
    }

    .uni-comment-face {
        width: 70upx;
        height: 70upx;
        border-radius: 100%;
        margin-right: 20upx;
        flex-shrink: 0;
        overflow: hidden;
    }

    .uni-comment-face image {
        width: 100%;
        border-radius: 100%;
    }

    .uni-comment-body {
        width: 100%;
    }

    .uni-comment-top {
        line-height: 1.5em;
        justify-content: space-between;
    }

    .uni-comment-top text {
        color: #0A98D5;
        font-size: 24upx;
    }

    .uni-comment-date {
        line-height: 38upx;
        flex-direction: row;
        justify-content: space-between;
        display: flex !important;
        flex-grow: 1;
    }

    .uni-comment-date view {
        color: #666666;
        font-size: 24upx;
        line-height: 38upx;
    }

    .uni-comment-content {
        line-height: 1.6em;
        font-size: 28upx;
        padding: 8rpx 0;
    }

    .uni-comment-replay-btn {
        background: #FFF;
        font-size: 24upx;
        line-height: 28upx;
        padding: 5rpx 20upx;
        border-radius: 30upx;
        color: #333 !important;
        margin: 0 10upx;
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

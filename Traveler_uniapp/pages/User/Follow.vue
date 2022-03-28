<template>
	<view>
		<view class="list-box">
			<view class="list-box-list" v-for="(item,index) in listData" style="margin-top: 3px;background-color: #f4f5f5;">
				
				<uni-row style="padding: 5px;">
					<uni-col :span="3">
						<cmd-avatar :src="item.follow_portrait" size="sm" @click="ToUser(item.follow,item.follow_name)"></cmd-avatar>
					</uni-col>
					<uni-col :span="21">
						<uni-row>
							<uni-col :span="21"><text style="color: #0077AA;font-size: 15px;" @click="ToUser(item.follow,item.follow_name)">{{item.follow_name}}</text></uni-col>
							<!-- <uni-col :span="2" v-if="item.created_by == user || data.created_by == user"><uni-icons type="trash-filled" size="18"  @click="deltalk(item.id)" style="float: right;"></uni-icons></uni-col> -->
						</uni-row>
						<view><text style="font-size: 10px;">关注：{{item.guanzhu}} 粉丝：{{item.fensi}}</text></view>
					</uni-col>
				</uni-row>
				
			</view>
		</view>
		<view v-if="showadd" style="font-size: 15px;color: #b3ccd0;font-weight: 600;text-align: center;margin-top: 5px;" @click="ShowMore"><text >加载更多</text></view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				page: 1,
				showadd: true,
				listData: []
			}
		},
		mounted() {
			this.getlistData()
		},
		methods: {
			ToUser(id,name){
				console.log('userid', id)
				uni.navigateTo({
					url: '/pages/User/UserSelf' +'?id='+ encodeURIComponent(id) + '&name=' + encodeURIComponent(name)
				});
			},
			// 首次获取数据
			getlistData(){
				this.$http.get('follow/?page=' + this.page).then(res=> {
				console.log('follow', res.data)
				if (res.data.results.code === 200) {
					this.listData = res.data.results.data
					if (this.listData.length === res.data.count) {
						this.showadd = false
					}
				}
				})
			},
			// 加载更多数据
			ShowMore(){
				this.page = this.page + 1
				this.$http.get('follow/?page=' + this.page).then(res=> {
				if (res.data.results.code === 200) {
					const nextData = res.data.results.data
					this.listData.push(...nextData)
					if (this.listData.length === res.data.count) {
						this.showadd = false
					}
				}
				})
			},
		}
	}
</script>

<style>

</style>

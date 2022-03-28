<template>
	<view>
		<view class="fanku_con">
			<view class="img_z">
				<view class="imgadf center" @click="ongetimg()">
					<image style="width: 58rpx;height: 58rpx;" src="./tupianadd.png" mode=""></image>
					<text style="margin-top: 5rpx;">上传图片</text>
				</view>
				<view style="position: relative;" v-for="(item,index) in img_list" :key="index">
					<image @click="preview(index,img_list)" style="width: 120rpx;height: 120rpx;margin-left: 20rpx;margin-bottom: 20rpx;background-color:rgba(0,0,0,0.1);border-radius: 10rpx;"
					 :src="item"></image>
					<image class="shancs" src="./shanchus2.png" mode="" @click="selec(index)"></image>
				</view>
			</view>
		</view>

	</view>
</template>

<script>
	export default {
		data() {
			return {
				img_list: []
			}
		},
		props: {
			// 最多上数量 1-9
			count: {
				type: Number,
				default: false
			},
			//图片上传地址
			url: {
				type: String,
				default: ''
			},
			//文件对应的 key 
			name: {
				type: String,
				default: ''
			},
			//请求头
			header: {
				type: Object,
				default: {}
			}
		},
		computed: {},
		methods: {
			ongetimg() { //上传图片方法
				var that = this
				if (!that.url) {
					return uni.showToast({
						title: '请填写上传地址',
						icon: 'none',
						position: 'bottom'
					});
				}
				uni.chooseImage({ //选中本地图片
					count: that.count,
					sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
					sourceType: ['album'], //从相册选择
					success: res => {
						uni.showLoading({ //加载框
							title: '加载中...'
						})
						const tempFilePaths = res.tempFilePaths;
						res.tempFilePaths.forEach((item, index) => { //本地选中的图片组
							console.log(that.url)
							let yy = new Date().getFullYear();
						　　let mm = new Date().getMonth()+1;
						　　let dd = new Date().getDate();
						　　let hh = new Date().getHours();
						　　let mf = new Date().getMinutes()<10 ? '0'+new Date().getMinutes() : new Date().getMinutes();
						　　let ss = new Date().getSeconds()<10 ? '0'+new Date().getSeconds() : new Date().getSeconds();
						　　const gettime = yy+'_'+mm+'_'+dd+'_'+hh+'_'+mf+'_'+ss;
							uni.uploadFile({ //上传图片
								url: that.url, //上传接口地址
								filePath: item, //一张图
								name: that.name,
								formData: {
								    'name': gettime
								},
								header: that.header,
								success: res => {
									if (that.img_list.length >= that.count) //限制
										return uni.showToast({
											title: '最多上传' + that.count + '张图片',
											icon: 'none',
											position: 'bottom'
										});
									that.img_list.push(JSON.parse(res.data).data.url); //plus数组
									that.$emit('obtain_img', that.img_list)
								}
							});
							uni.hideLoading() //关闭加载框
						});
					}
				});
			},
			//删除
			selec(index) {
				this.img_list.splice(index, 1)
				this.$emit('obtain_img', this.img_list)
			},
			//预览
			preview(index, urls) {
				console.log(index)
				console.log(urls)
				uni.previewImage({
					urls: urls,
					current: index,
					longPressActions: {
						itemList: ['发送给朋友', '保存图片', '收藏'],
						success: function(data) {
							console.log('选中了第' + (data.tapIndex + 1) + '个按钮,第' + (data.index + 1) + '张图片');
						},
						fail: function(err) {
							console.log(err.errMsg);
						}
					}
				});
			}
		}
	}
</script>

<style>
	page {
		background-color: #181E38;
		padding-top: 66rpx;
		box-sizing: border-box;
	}

	.fanku_con {
		width: 690rpx;
		background: rgba(0, 0, 0, 0.1);
		border-radius: 10rpx;
		margin-left: 30rpx;
		padding-top: 20rpx;
		padding-bottom: 70rpx;
		box-sizing: border-box;
	}

	.imgadf {
		width: 120rpx;
		height: 120rpx;
		background-color: rgba(255, 255, 255, 0.5);
		/* margin-left: 29rpx; */
		margin-left: 20rpx;
		border-radius: 10rpx;
		margin-bottom: 20rpx;
		font-size: 20rpx;
		color: #666666;
		flex-direction: column;
	}

	.img_z {
		display: flex;
		flex-wrap: wrap;
		margin-top: 90rpx;
		padding-right: 10rpx;
		box-sizing: border-box;
	}

	.shancs {
		width: 35rpx;
		height: 35rpx;
		position: absolute;
		top: -10rpx;
		right: -10rpx;
		background-color: #FFFFFF;
		border-radius: 100%;
	}

	.dianhua_on {
		width: 364rpx;
		height: 74rpx;
		background: linear-gradient(to right, #F55C63, #F78361);
		border-radius: 38rpx;
		font-size: 28rpx;
		color: #FFFFFF;
		margin-top: 130rpx;
		margin-left: 192rpx;
	}

	.center {
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>

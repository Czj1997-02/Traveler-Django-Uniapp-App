<!-- components/evaluate-components/index.wxml -->
<template>
	<view class="evaluateBox">
		<view class="evaluate-header">
			<view class="title">
				<text v-if="isShowIcon" class="iconfont" style="color:#999">&#xe640;</text>
				<text v-if="isShowTotal" style="margin-left: 10upx;">评价 ({{ listData.length }})</text>
			</view>
			<view class="total">
				<view class="stars">
					<view class="stars-normal">
						<view class="box">
							<block v-for="i in 5" :key="i"><text class="iconfont">&#xe870;</text></block>
						</view>
					</view>
					<view class="stars-selected" :style="{ width: (rate / 5) * 100 + '%' }">
						<view class="box">
							<block v-for="j in 5" :key="j"><text class="iconfont">&#xe870;</text></block>
						</view>
					</view>
				</view>
				<text>{{ rate }}{{ (rate * 10) % 10 == 0 ? '.0' : '' }}</text>
			</view>
		</view>

		<view class="lists" v-if="listData.length > 0">
			<block v-for="(item, index_) in listData" :key="index_">
				<view class="item">
					<view class="icon"><image :src="item.header_img" mode="widthFix" style="width:100%" /></view>
					<view class="info">
						<view class="name-time">
							<text class="name">{{ item.user_name }}</text>
							<text class="time">{{ item.create_time }}</text>
						</view>
						<view class="stars">
							<view class="stars-normal">
								<view class="box">
									<block v-for="i_ in 5" :key="i_"><text class="iconfont">&#xe870;</text></block>
								</view>
							</view>
							<view class="stars-selected" :style="{ width: (item.rate / 5) * 100 + '%' }">
								<view class="box">
									<block v-for="j_ in 5" :key="j_"><text class="iconfont">&#xe870;</text></block>
								</view>
							</view>
						</view>
						<view class="evaluate-content">
							<text>{{ item.content || '用户暂未评价' }}</text>
							<view class="imgs" v-if="item.imgs">
								<block v-for="(imgurl, index) in item.imgs" :key="index">
									<view class="imgs-box"><image :src="imgurl" mode="widthFix" style="width: 100%;" @click="previewImg(imgurl,item.imgs)"></image></view>
								</block>
							</view>
						</view>
					</view>
				</view>
			</block>
		</view>
		<view class="no-lists" v-else>暂无评论</view>
	</view>
</template>

<script>
//数据模拟
import data from './list.js';
export default {
	props: {
		//评价列表数据
		listData: {
			type: Array,
			default: data
		},
		//是否显示总评价数量
		isShowTotal: {
			type: Boolean,
			default: true
		},
		//是否显示评价前面的图标
		isShowIcon: {
			type: Boolean,
			default: true
		},
		//总评分
		rate: {
			type: Number,
			default: 4.6
		}
	},
	data() {
		return {}
	},
	methods: {
		previewImg(src,urls){
			uni.previewImage({
				current:src,
				urls
			})
		}
	}
};
</script>
<style scoped>
@import './iconfont.css';
.evaluateBox {
	width: 100%;
	margin-bottom: 120upx;
}

.evaluate-header {
	width: 100%;
	height: 80upx;
	display: flex;
	justify-content: space-between;
	padding: 20upx;
	align-items: center;
	margin-bottom: 12upx;
	box-sizing: border-box;
	border-bottom: 1upx solid #e5e5e5;
}

.evaluateBox .title {
	display: flex;
	align-items: center;
	color: #000000;
	font-size: 30upx;
}

.total {
	/* flex: 1; */
	height: 100%;
	font-size: 30upx;
	color: #d76d9d;
	display: flex;
	align-items: center;
	justify-content: flex-end;
}

.stars {
	width: 180upx;
	height: 36upx;
	position: relative;
}
.stars .box {
	width: 180upx;
}
.stars-normal {
	width: 100%;
	position: absolute;
	left: 0;
	top: 0;
	color: #ccc;
}
.stars-selected {
	position: absolute;
	left: 0;
	top: 0;
	z-index: 1;
	color: #fde16d;
	overflow: hidden;
}
.stars-selected .iconfont,
.stars-normal .iconfont {
	font-size: 36upx;
}

.lists .item {
	padding: 20upx;
	display: flex;
	/* height: auto; */
	/* align-items: center; */
	font-size: 22upx;
	color: #999;
}

.lists .item .icon {
	width: 60upx;
	height: 60upx;
	border-radius: 50%;
	overflow: hidden;
	margin-right: 26upx;
	/* align-self: flex-start; */
}

.lists .item .info {
	flex: 1;
	font-size: 26upx;
	color: #666;
}

.info .name-time {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding-bottom: 6upx;
}
.lists .info .stars {
	width: 140upx;
}

.info .stars-normal .iconfont,
.info .stars-selected .iconfont {
	font-size: 28upx;
}

.info .stars .box {
	width: 140upx;
}
.lists .info .evaluate-content {
	color: #000;
	font-size: 28upx;
	text-align: left;
	padding-top: 6upx;
}
.info .evaluate-content .imgs {
	display: flex;
	flex-wrap: wrap;
	padding-top: 6upx;
}
.evaluate-content .imgs .imgs-box {
	width: 25%;
	padding-right: 10upx;
	box-sizing: border-box;
}
/* .evaluate-content .imgs .imgs-box:nth-child(4n+1){
	padding-left: 0;
}
.evaluate-content .imgs .imgs-box:nth-child(4n){
	padding-right: 0;
} */
.no-lists {
	padding: 20upx 0;
	text-align: center;
	font-size: 24upx;
	color: #666;
}
</style>

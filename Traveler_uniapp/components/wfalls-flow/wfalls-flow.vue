<template>
	<view class="list-container">
		<view id="wf-list" class="list" v-for="(list,listIndex) of viewList" :key="listIndex">
            <view class="item" v-for="(item,index) of list.list" :key="index" @click="goToPage(item.pagetyp,item.id,item.name)">
                <image @load="handleViewRender(listIndex,index)" @error="handleViewRender(listIndex,index)" :src="item.image" mode="widthFix" v-if="item.image"></image>
				
				<uni-row>
					<uni-col :span="6">
						<cmd-avatar :src="item.created_by_portrait" size="sm"></cmd-avatar>
					</uni-col>
					<uni-col :span="18">
						<view class="desc" style="font-weight: 600;margin-top: 10rpx;" v-if="item.name">{{item.name}}</view>
					</uni-col>
				</uni-row>

                <view class="desc" v-if="item.content">{{item.content}}</view>
				
				<uni-row>
					<uni-col :span="12">
						<uni-icons type="heart" size="15" style="color:#ec7171" v-if="! item.is_praise"></uni-icons>
						<uni-icons type="heart-filled" size="15" style="color:#ec7171" v-if="item.is_praise"></uni-icons>
						<text style="font-size:15px;color:#545d61">{{item.praise}}</text>
					</uni-col>
					<uni-col :span="12">
						<uni-icons type="star" size="15" style="color:#e8c50a" v-if="! item.is_collect"></uni-icons>
						<uni-icons type="star-filled" size="15" style="color:#e8c50a" v-if="item.is_collect"></uni-icons>
						<text style="font-size:15px;color:#545d61">{{item.collect}}</text>
					</uni-col>
				</uni-row>
				
            </view>
        </view>
	</view>
</template>

<script>
	import cmdAvatar from "@/components/cmd-avatar/cmd-avatar.vue"
	export default {
		components: {cmdAvatar},
        props:{
            list:{
                type:Array, //实际请求获取的列表数据
            }
        },
		data() {
			return {
                viewList:[{list:[]},{list:[]}],  //展示到视图的列表数据
                everyNum:2
			}
		},
		methods: {
			goToPage(typ,id,name) {
				if (!id) return;
				uni.navigateTo({
					url: '/pages/tabbar/tabbar-1/'+ typ +'?id='+ encodeURIComponent(id) + '&name=' + encodeURIComponent(name)
				});
			},
            init(){
                this.viewList = [{list:[]},{list:[]}];
                setTimeout(()=>{
                    this.handleViewRender(0,0)
                },0)
            },
			handleViewRender(x,y){
                // console.log(x,y);
                // const num = (x+1)*(y+1);
                // console.log(num%(this.everyNum));
                // console.log(num);
                // if((num%(this.everyNum))!==0&&num!==1)return;
                // console.log(num,'----');
                const index = this.viewList.reduce((total,current)=>total + current.list.length,0)
                if(index>this.list.length-1) {
                    // 加载完成触发事件并返回加载过的图片数
                    this.$emit('finishLoad',index)
                    return
                };
                const query = uni.createSelectorQuery().in(this);
                let listFlag = 0;
                query.selectAll('#wf-list').boundingClientRect(data => {
                    listFlag = data[0].bottom - data[1].bottom<=0?0:1;
                    this.viewList[listFlag].list.push(this.list[index])
                    // this.list.slice(index,index+this.everyNum).forEach((item,index)=>{
                    //     const flag = listFlag===0?index&1:Number(!(index&1))
                    //     this.viewList[flag].list.push(item)
                    // })
                }).exec()
            },
		},
        mounted() {
            if(this.list.length){
                this.init()
            }
        }
	}
</script>

<style lang="stylus" scoped>
    .list-container
        display flex
        justify-content space-between
        align-items:flex-start
        padding 0 24rpx
        padding-top 30rpx
        .list
            width calc(50% - 8rpx)
            display flex
            flex-direction column
            .item
                margin-bottom 18rpx
                border 1px solid #b3ccd0
                image
                    width 100%
                .desc
                    padding 4rpx
                    font-size 28rpx
</style>
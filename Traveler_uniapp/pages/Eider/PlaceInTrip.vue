<template>
	<view>
		<!-- <uni-group title="地点" class="desc-box"> -->
			
			<uni-card>
			<uni-list>
			    <uni-list-item
					:title="place.name" 
					:thumb="place.image"
					:note="place.created_by_name + ' - ' + place.created_date"
					thumb-size="lg"
					clickable
					@click="goToPage(place.pagetyp,place.id,place.name)"
				></uni-list-item>
			</uni-list>
			</uni-card>
			
			<!-- {{this.place.name}} -->
		<!-- </uni-group> -->
		
		<uni-group title="信息" class="desc-box">
			
			<template>
			    <view class="">
			        <uni-forms :modelValue="data" label-position="top">
			            <uni-forms-item label="主要事项" name="name" label-width="100">
			                <uni-easyinput type="text" v-model="data.name" placeholder="主要事项" />
			            </uni-forms-item>
						<uni-forms-item label="备忘说明" name="desc" label-width="100">
						    <uni-easyinput type="text" v-model="data.desc" placeholder="备忘说明" />
						</uni-forms-item>
						
						<uni-forms-item label="预计耗时(h)" name="theTime" label-width="100">
						    <uni-number-box v-model="data.theTime" :min="0" :max="9999999999" :step="0.1"></uni-number-box>
						</uni-forms-item>
						<uni-forms-item label="预算金额(元)" name="thePay" label-width="100">
						    <uni-number-box v-model="data.thePay" :min="0" :max="9999999999" :step="0.1"></uni-number-box>
						</uni-forms-item>
						
						<uni-forms-item label="预计开始日期" name="theDate" label-width="100">
						    <uni-datetime-picker type="date" v-model="data.theDate" start="2000-1-1" end="2200-1-1" />
						</uni-forms-item>
						
						<uni-forms-item label="预计开始时间" name="theBegin" label-width="100">
							<uni-card @click="DatePicker('time')">
								
							<view v-if="!data.theBegin">
								<image src="../../static/img/time.png" style="width: 16px;height: 16px;"></image>
								<text style="margin-left: 5px;color: #808080;">选择时间</text>
							</view>
							
							<view v-if="data.theBegin">
							<text style="color: #808080;">{{data.theBegin}}</text>
							<image src="../../static/img/close.png" style="width: 12px;height: 12px;float: right;margin-top: 3px;" @click="clean()"></image>
							</view>
							</uni-card>
							 <mx-date-picker :show="showPicker" :type="type" :value="data.theBegin" :show-tips="true"  :show-seconds="true" @confirm="ed" @cancel="ed" />
						</uni-forms-item>
			        </uni-forms>
			    </view>
			</template>
			<button @click="changedata" style="background-color: #b3ccd0;margin-top: 20px;">保存</button>
			<button @click="deldata" style="background-color: #b3ccd0;margin-top: 10px;color: red;">删除</button>
		</uni-group>

	</view>
</template>

<script>
	import MxDatePicker from "@/components/mx-datepicker/mx-datepicker.vue";
	export default {
		components: {
			MxDatePicker
		},
		data() {
			return {
				tripID: null,
				tripname: '',
				showPicker: false,
				value: '',
				type: 'time',
				url: '',
				data: {},
				place: {}
			}
		},
		methods: {
			goToPage(typ,id,name) {
				if (!id) return;
				uni.navigateTo({
					url: '/pages/tabbar/tabbar-1/'+ typ +'?id='+ encodeURIComponent(id) + '&name=' + encodeURIComponent(name)
				});
			},
			getPlaceInTrip(id){
				console.log('11111111111111111111',id)
				
				
				
				this.$http.get('place-in-trip/' + id + '/').then(res=> {
				
				if (res.data.code === 200) {
					this.data = res.data.data
					this.tripname = this.data.trip_name
					this.tripID = this.data.trip
					console.log('place-in-trip',this.data)
					// 获取地点信息
					this.$http.get('place/' + this.data.place + '/').then(res2=> {
					
					if (res2.data.code === 200) {
						this.place = res2.data.data
						console.log('place',this.place)
					}
					})
				}
				})
			},
			DatePicker(type){//显示
				this.type = type;
				this.showPicker = true;
				this.value = this[type];
			},
			ed(e) {//选择
				this.showPicker = false;
				if(e) {
					this[this.type] = e.value;
					this.data.theBegin = e.value;
					//选择的值
					console.log('value => '+ e.value);
					//原始的Date对象
					console.log('date => ' + e.date);
				}
			},
			clean(){
				this.data.theBegin = null
				this.showPicker = false
			},
			changedata () {
				const putData = {}
				
				// 处理数据
				if (this.data.name) {
					putData['name'] = this.data.name
				} else {
					putData['name'] = ''
				}
				
				if (this.data.desc) {
					putData['desc'] = this.data.desc
				} else {
					putData['desc'] = ''
				}
				
				if (this.data.theDate) {
					putData['theDate'] = this.data.theDate
				} else {
					putData['theDate'] = ''
				}
				
				if (this.data.theBegin) {
					putData['theBegin'] = this.data.theBegin
				// }
				} else {
					putData['theBegin'] = ''
				}
				
				if (this.data.theTime) {
					if (this.data.theTime === "0") {
						putData['theTime'] = 0
					} else {
						putData['theTime'] = this.data.theTime
					}
				} else {
					putData['theTime'] = 0
				}
				
				if (this.data.thePay) {
					if (this.data.thePay === "0") {
						putData['thePay'] = 0
					} else {
						putData['thePay'] = this.data.thePay
					}
				} else {
					putData['thePay'] = 0
				}
				
				console.log(putData)
				this.$http.put('place-in-trip/' + this.data.id + '/', putData,).then(res=> {
				if (res.data.code === 200) {
					uni.showToast({title:'修改成功',icon:'none'})
					// uni.reLaunch({
					// 	url: '/pages/tabbar/tabbar-1/tabbar-1',
					// })
					setTimeout(()=>{
						// H5
						// this.$router.go(-1)
						// setTimeout(()=>{
						// 	this.$router.go(0)
						// },500)

						// app
						uni.navigateBack({
							success: () => {
								uni.navigateBack({
									success: () => {
										// 因为直接跳转影响返回,所以到tab页面后再跳转
										uni.navigateTo({
											url: '/pages/Eider/TripEider' +'?id='+ encodeURIComponent(this.tripID) + '&name=' + encodeURIComponent(this.tripname)
										});
									}
								})
							}
						})
					},500)
				}
				})
			},
			deldata() {
				this.$http.del('place-in-trip/' + this.data.id + '/').then(res=> {
					console.log(res.data)
					setTimeout(()=>{
						// h5
						// this.$router.go(-1)
						// setTimeout(()=>{
						// 	this.$router.go(0)
						// },500)

						// app
						uni.navigateBack({
							success: () => {
								uni.navigateBack({
									success: () => {
										console.log(this.tripID,this.tripname)
										// 因为直接跳转影响返回,所以到tab页面后再跳转
										uni.navigateTo({
											url: '/pages/Eider/TripEider' +'?id='+ encodeURIComponent(this.tripID) + '&name=' + encodeURIComponent(this.tripname)
										});
									}
								})
							}
						})
					},500)
				})
			}
		},
		onLoad(option) {
			const id = JSON.parse(decodeURIComponent(option.id))
			uni.setNavigationBarTitle({
				title: decodeURIComponent(option.name)
			})
			console.log(JSON.parse(decodeURIComponent(option.id)))
			this.getPlaceInTrip(id)
		}
	}
</script>

<style>
.desc-box {
	margin: 0px !important;
}
/deep/.uni-forms-item__inner {
	padding-bottom: 2px !important;
}
/deep/.uni-numbox {
	width: 100% !important;
}
/deep/.uni-numbox__value {
	width: -webkit-calc(100% - 70px) !important;
}
/deep/.uni-card {
    margin: 0px !important;
}
/deep/.uni-list--border-top {
	height: 0px !important;
}
/deep/.uni-list--border-bottom {
	height: 0px !important;
}
/* /deep/.uni-card {
	padding: 0px;
	margin: 5px 0px;
} */
/* /deep/.uni-card__content {
	padding: 2px;
} */
</style>

<template>
	<view class="me-select-item-wrap-box">
		<view class="me-select-item-wrap" v-for="(item, index) in data__list" :key="index">
			<view class="me-select-item-left" :class="{'scan': editModel}">
				<view @tap="itemTap(item, index)">
					<slot :slot-scope="{item: item, index:index}"></slot>
				</view>
				<image @tap="tap(index, false)" :class="{'up': editModel}" v-show="editModel && item.select" class="select-icon"
				 src="../../static/unselect.png" mode=""></image>
				<image @tap="tap(index, true)" :class="{'up': editModel}" v-show="editModel && !item.select" class="select-icon"
				 src="../../static/select.png" mode=""></image>
			</view>
		</view>
		<view class="bot-fixed-wrap" v-if="editModel && data__list.length > 0">
			<view v-if="selectArr.length < data__list.length" class="but" @tap="selectAll">全选</view>
			<view v-else class="but" @tap="unSelectAll">取消全选</view>
			<view @tap="finish" class="but" :class="{'danger': selectArr.length > 0, 'un':selectArr.length<=0 }">{{selectArr.length > 0 ? `确认(${selectArr.length})` : '确认'}}</view>
		</view>
	</view>
</template>

<script>
	import meSelect from '@/components/me-select/me-select.vue'
	export default {
		components: {
			meSelect
		},
		data() {
			return {
				data__list: [],
				editModel: true,
				selectNum: 0,
				selectArr: [],
			}
		},
		props: {
			datalist: {
				type: Array,
				require: true
			},
			options: {
				type: Object,
				require: true
			},
		},
		watch: {
			datalist: {
				handler(n, o) {
					this.data__list = n
				},
				deep: true
			},
			data__list: {
				handler(n, o) {
					var selectNum = 0
					var tem = []
					if (this.data__list.length > 0) {
						this.data__list.forEach((item, index) => {
							item.select && selectNum++
							if (this.options.flags.length <= 0) {
								item.select && tem.push(item)
							} else {
								var tItem = {}
								this.options.flags.forEach((item2) => {
									tItem[item2] = item[item2]
								})
								tItem['index'] = index
								item.select && tem.push(tItem)
							}
						})
					}
					this.selectArr = tem
					this.selectNum = selectNum
					this.$emit('change', this.selectArr)
				},
				deep: true
			}
		},
		created() {
			this.data__list = this.datalist
		},
		methods: {
			itemTap(item, index) {
				if (this.options.itemCanSelect && this.editModel) {
					this.data__list[index].select = !this.data__list[index].select
				}
				if (!this.editModel) {
					this.$emit('itemClick', item)
				}
			},
			changeModel() {
				this.editModel = !this.editModel
			},
			getSelectAll() {
				return this.selectArr
			},
			selectAll() {
				this.data__list.forEach((item, index) => {
					item.select = true
				})
			},
			unSelectAll() {
				this.data__list.forEach((item, index) => {
					item.select = false
				})
			},
			tap(index, value) {
				this.data__list[index].select = value
			},
			finish() {
				if (this.selectArr.length <= 0) return
				this.$emit('finish', this.selectArr)
			}
		}

	}
</script>

<style scoped>
	.me-select-item-wrap-box {
		padding: 20upx;
		box-sizing: border-box;
	}

	.me-select-item-wrap {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		margin: 0upx 0;
	}


	.me-select-item-left {
		min-height: 40upx;
		width: 100%;
		transition: width .1s linear;
	}

	.me-select-item-left .select-icon {
		height: 40upx;
		width: 40upx;
	}

	.me-select-item-left.scan {
		width: 80%;
	}

	.me-select-item-left .select-icon {
		position: absolute;
		left: 40upx;
		top: 50%;
		transform: translateY(-50%);
		z-index: -1;


	}

	.me-select-item-left .select-icon.up {
		z-index: 1;
	}

	.bot-fixed-wrap {
		position: fixed;
		background-color: #FFFFFF;
		display: flex;
		bottom: 0;
		left: 0;
		border-top: 1upx solid #b3ccd0;
		width: 100%;
		height: 100upx;
		z-index: 99;
	}

	.but {
		line-height: 100upx;
		text-align: center;
		height: 100upx;
		width: 50%;
	}

	.but.un {
		color: #999999;
	}

	.but:first-child {
		border-right: 1upx solid #b3ccd0;
	}

	.but.danger {
		background-color: #b3ccd0;
		color: #ffffff;
		font-weight: 500;
	}
</style>

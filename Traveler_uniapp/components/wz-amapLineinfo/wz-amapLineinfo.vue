<template>
	<view class="xlxx_box">

		<view class="mapInfo_box">
			<view id="map_box"></view>
			<view class="input_box">
				<picker @change="lineChange" :value="lineIndex" :range-key="'LINE_NAME'" :range="lineList">
					<view class="uni-input-wrapper">
						<input class="uni-input" placeholder="请选择行驶路线" :value="lineName" disabled="true" />
						<view class="xiala_icon"></view>
					</view>
				</picker>

			</view>
		</view>
		<view class="btn_box">
			<view class="btn" @click="saveLineInfo">
				确定线路
			</view>
		</view>
	</view>

</template>

<script>
	import amap from '../../static/AMap.js';

	export default {
		data() {
			return {
				map: '',
				lineName:'',
				lineList: [{
						ID: 143,
						LINE_NAME: "模拟线路",
						ROADLIST: [{
								LON: "116.7829494443813",
								ID: 54,
								LAT: "33.963703521394905",
								DLMC: "濉溪北路与海宫路",
							},
							{

								LON: "116.77759485681538",
								ID: 60,
								LAT: "33.95421870052367",
								DLMC: "人民中路与濉溪北路"
							},
							{

								LON: "116.78970490291029",
								ID: 57,

								LAT: "33.95441083194905",
								DLMC: "人民中路与鹰山路"
							},
							
						],


					}


				],
				lineIndex: '',
				polyline: [],
				overlayGroups: '', //线组
				markXlArr: [], //线路mark
				markLineArr: [],
				hsArr: [], //记录点下标
				allMarkPoint: [ //所有路口经纬度

					{

						LON: "116.77759485681538",
						ID: 60,
						LAT: "33.95421870052367",
						DLMC: "人民中路与濉溪北路"
					},
					{

						LON: "116.78970490291029",
						ID: 57,
						LAT: "33.95441083194905",
						DLMC: "人民中路与鹰山路"
					},
					{

						LON: "116.79445036079697",
						ID: 55,
						LAT: "33.95445714453656",
						DLMC: "人民中路与孟山中路",
					},
					{

						LON: "116.79978820819366",
						ID: 63,
						LAT: "33.95454633145508",
						DLMC: "人民中路与相山中路"
					},
					{

						LON: "116.77125131114326",
						ID: 69,
						LAT: "33.95437875211084",
						DLMC: "人民路五中路段"
					},

					{

						LON: "116.7829494443813",
						ID: 54,
						LAT: "33.963703521394905",
						DLMC: "濉溪北路与海宫路",

					}
				]
			}
		},
		onLoad() {


			amap().then(res => {
				this.map = new AMap.Map('map_box', {
					zoom: 14, //级别
					resizeEnable: true
				});
				this.addAllMarker(this.allMarkPoint)
			});


		},
		methods: {


			saveLineInfo() {
				// this.markXlArr             线路mark点集合
				// this.markXlArr._originOpts 线路每一个mark点（路口名称、路ID、经纬度）

			},
			lineChange(e) { //路线下拉选择框
				this.markLineArr = []
				this.hsArr = []
				this.markXlArr = []
				this.lineIndex = e.detail.value
				this.lineName = this.lineList[this.lineIndex]['LINE_NAME']

				var laysArr = this.map.getAllOverlays()

				for (var i = 0; i < laysArr.length; i++) {
					if (laysArr[i]['type'] == 'AMap.Overlay') {
						this.map.remove(laysArr[i])
					} else {
						laysArr[i].setLabel({
							offset: new AMap.Pixel(0, -5),
							content: "",
							direction: 'center'
						});
					}

				}

				for (var k = 0; k < this.lineList[this.lineIndex]['ROADLIST'].length; k++) {
					this.markLineArr.push([Number(this.lineList[this.lineIndex]['ROADLIST'][k]['LON']), Number(this
						.lineList[this.lineIndex]['ROADLIST'][k]['LAT'])])
					this.hsArr.push(this.lineList[this.lineIndex]['ROADLIST'][k]['ID'])
				}

				this.addMarker(this.lineList[this.lineIndex]['ROADLIST'])
			},

			addLine(lineArr) { //连线
				var that = this
				this.polyline = []
				var lineEach = new AMap.Polyline({
					map: that.map,
					path: lineArr,
					strokeColor: "#FF2222", //线颜色
					strokeOpacity: 1, //线透明度
					strokeWeight: 5, //线宽
					strokeStyle: "solid", //线样式
					showDir: true
				});
				this.polyline.push(lineEach)
				this.overlayGroups = new AMap.OverlayGroup(this.polyline);
				this.map.add(this.overlayGroups);
			},
			addMarker(jwdArr) { //改变点并连线

				this.map.setCenter([Number(jwdArr[0]['LON']), Number(jwdArr[0]['LAT'])])
				var lineArr = []
				var allMarkArr = this.map.getAllOverlays()
				for (var i = 0; i < jwdArr.length; i++) { //添加线经纬度集合
					lineArr.push([Number(jwdArr[i]['LON']), Number(jwdArr[i]['LAT'])])
					for (var k = 0; k < allMarkArr.length; k++) {
						//判断所有mark里和所选线路相同的mark
						if (jwdArr[i]['ID'] == allMarkArr[k]['_originOpts']['id']) {
							this.markXlArr.push(allMarkArr[k])
							allMarkArr[k]['_originOpts']['state'] = true
							allMarkArr[k].setLabel({
								offset: new AMap.Pixel(0, -5),
								content: "<div style='color:#fff'>" + (i + 1) + "</div>",
								direction: 'center'
							});
						}
					}
				}
				this.addLine(lineArr)
			},
			addAllMarker(jwdArr) { //添加所有点
				var that = this
				this.map.setCenter([Number(jwdArr[0]['LON']), Number(jwdArr[0]['LAT'])])
				var lineArr = []
				var markIndex = []
				var indexArr = []
				for (var i = 0; i < jwdArr.length; i++) {
					var marker = new AMap.Marker({
						position: new AMap.LngLat(Number(jwdArr[i]['LON']), Number(jwdArr[i]['LAT'])),
						id: jwdArr[i]['ID'],
						state: false,
						dlmc: jwdArr[i]['DLMC']
					});
					marker.on('click', function(e) {

						if (this._originOpts.state) {
							this._originOpts.state = false
							var clearIndex = that.hsArr.indexOf(this._originOpts.id)

							that.hsArr.splice(clearIndex, 1)
							that.markXlArr.splice(clearIndex, 1)

							that.markLineArr.splice(clearIndex, 1)
							var laysArr = that.map.getAllOverlays()
							for (var i = 0; i < laysArr.length; i++) {
								if (laysArr[i]['type'] == 'AMap.Marker') {
									laysArr[i].setLabel({
										offset: new AMap.Pixel(0, -5),
										content: "",
										direction: 'center'
									});

								}
							}

							for (var i = 0; i < laysArr.length; i++) {
								if (laysArr[i]['type'] == 'AMap.Overlay') {
									that.map.remove(laysArr[i])
								}

							}
							for (var i = 0; i < that.markXlArr.length; i++) {
								that.markXlArr[i].setLabel({
									offset: new AMap.Pixel(0, -5),
									content: "<div style='color:#fff'>" + (i + 1) + "</div>",
									direction: 'center'
								});
							}

							that.addLine(that.markLineArr)

						} else {

							this._originOpts.state = true
							that.markXlArr.push(this)
							that.hsArr.push(this._originOpts.id)
							that.markLineArr.push([Number(this['_originOpts']['position']['lng']), Number(this[
								'_originOpts']['position']['lat'])])
							for (var i = 0; i < that.markXlArr.length; i++) {
								this.setLabel({
									offset: new AMap.Pixel(0, -5),
									content: "<div style='color:#fff'>" + that.markXlArr.length + "</div>",
									direction: 'center'
								});

							}

							that.addLine(that.markLineArr)
						}
					})
					this.map.add(marker)

				}

			},


		}
	}
</script>

<style lang="scss">
	.xlxx_box {
		.btn_box {
			position: fixed;
			bottom: 13.88rpx;
			left: 0;
			width: 100%;

			height: 87.5rpx;
			display: flex;
			justify-content: center;

			.btn {
				width: 80%;
				height: 87.5rpx;
				line-height: 87.5rpx;
				color: #fff;
				font-size: 29.16rpx;
				background: #1777FF;
				text-align: center;
				border-radius: 8.33rpx;
			}
		}

		.mapInfo_box {
			width: 100%;
			height: 100%;
			position: fixed;

			.input_box {
				width: 100%;
				padding: 11.11rpx 19.44rpx;
				position: absolute;
				left: 0;
				top: 0;
				z-index: 100;
				box-sizing: border-box;

				input {

					height: 68.05rpx;
					background: #fff;
					border: 0.69rpx solid #E3E3E3;
					border-radius: 8.33rpx;
					font-size: 29.16rpx;
				}

				.xiala_icon {
					width: 50rpx;
					height: 50rpx;
					position: absolute;
					right: 0;
					top: 50%;
					margin-top: -25rpx;
					background: url(../../static/img/play.png)no-repeat;
					background-size: 100% 100%;
				}
			}

			#map_box {
				width: 100%;
				height: 100%;
				position: absolute;
				left: 0;
				top: 0;

			}
		}
	}
</style>

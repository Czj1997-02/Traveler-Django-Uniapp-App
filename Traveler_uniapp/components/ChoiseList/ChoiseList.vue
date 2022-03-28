<template>
	<view>
		<uni-list>
				<!-- @click="goToPage(item.pagetyp,item.id,item.name)" -->
				<!-- @switchChange="choise(item.id)" -->
				<!-- :switchChecked="! item.id in choiseitems" -->
		    <uni-list-item v-for="(item,index) of data" :key="index"
				:title="item.name" 
				:thumb="item.image"
				:note="item.created_by_name + ' - ' + item.created_date"
				thumb-size="lg"
				clickable
				:showSwitch="true"
				:switchChecked="false"
				@switchChange="choise(item.id)"
			></uni-list-item>
		</uni-list>
	</view>
</template>

<script>
	export default {
		name:"ChoiseList",
		props: {
			data: {
				type: Array,
				default: () => [
				{
					"id": 3,
					"images": [
						{
							"id": 5,
							"content": "惠州学院[图1]",
							"img": "127.0.0.1:8000/media/imgs/2021_09/tanxian.jpg"
						}
					],
					"pagetyp": "place",
					"image": "http://127.0.0.1:8000/media/imgs/2021_09/tanxian.jpg",
					"created_by_portrait": "http://127.0.0.1:8000/media/img/portraits/Samle.jpg",
					"created_by_name": "Samle",
					"created_date": "2021-09-29 19:56:13",
					"last_edited_by_name": "Samle",
					"last_edited_date": "2021-09-29 19:56:13",
					"is_praise": false,
					"is_collect": false,
					"praise": 0,
					"collect": 0,
					"gaode": "https://surl.amap.com/3sJbsEx118b5",
					"lng": "114.41850230097772112003",
					"lat": "23.03724660226005482855",
					"name": "惠州学院",
					"desc": "<p>测试</p>",
					"typ": "play",
					"show": true,
					"editedDay": "2021-09-29",
					"deleted": "0",
					"img1": 5,
					"img2": null,
					"img3": null,
					"img4": null,
					"img5": null,
					"img6": null,
					"img7": null,
					"img8": null,
					"img9": null,
					"city": 58,
					"created_by": 1,
					"last_edited_by": 1
				},
				{
					"id": 2,
					"images": [
						{
							"id": 2,
							"content": "康冠科技[图1]",
							"img": "127.0.0.1:8000/media/imgs/2021_09/1632903224932_IMG_20210916_140224.jpg"
						}
					],
					"pagetyp": "place",
					"image": "http://127.0.0.1:8000/media/imgs/2021_09/tanxian.jpg",
					"created_by_portrait": "http://127.0.0.1:8000/media/img/portraits/Samle.jpg",
					"created_by_name": "Samle",
					"created_date": "2021-09-29 16:15:06",
					"last_edited_by_name": "Samle",
					"last_edited_date": "2021-09-29 16:15:06",
					"is_praise": false,
					"is_collect": false,
					"praise": 0,
					"collect": 0,
					"gaode": "https://surl.amap.com/2sLfal3s2Aj",
					"lng": "114.48351636528970232121",
					"lat": "22.99202461600761182581",
					"name": "康冠科技",
					"desc": "<p>测试多个地点</p>",
					"typ": "go",
					"show": true,
					"editedDay": "2021-09-29",
					"deleted": "0",
					"img1": 2,
					"img2": null,
					"img3": null,
					"img4": null,
					"img5": null,
					"img6": null,
					"img7": null,
					"img8": null,
					"img9": null,
					"city": 58,
					"created_by": 1,
					"last_edited_by": 1
				},
				{
					"id": 3,
					"images": [
						{
							"id": 1,
							"content": "凤翔花园[图1]",
							"img": "127.0.0.1:8000/media/imgs/2021_09/1632903010223_IMG_20210926_233337.jpg"
						}
					],
					"pagetyp": "place",
					"image": "http://127.0.0.1:8000/media/imgs/2021_09/tanxian.jpg",
					"created_by_portrait": "http://127.0.0.1:8000/media/img/portraits/Samle.jpg",
					"created_by_name": "Samle",
					"created_date": "2021-09-29 16:11:27",
					"last_edited_by_name": "Samle",
					"last_edited_date": "2021-09-29 16:11:27",
					"is_praise": false,
					"is_collect": false,
					"praise": 0,
					"collect": 0,
					"gaode": "https://surl.amap.com/2rxHHJf186xO",
					"lng": "114.48473408818247776253",
					"lat": "23.00465240242822062555",
					"name": "凤翔花园",
					"desc": "<p>测试高德定位数据录入</p>",
					"typ": "hotel",
					"show": true,
					"editedDay": "2021-09-29",
					"deleted": "0",
					"img1": 1,
					"img2": null,
					"img3": null,
					"img4": null,
					"img5": null,
					"img6": null,
					"img7": null,
					"img8": null,
					"img9": null,
					"city": 58,
					"created_by": 1,
					"last_edited_by": 1
				}
				]
			},
			// choiseitems: {
			// 	type: Array,
			// 	default: () => [
					
			// 	]
			// },
		},
		data() {
			return {
				choiseitems: []
			};
		},
		watch: {
			// data(){
			// 	this.choiseitems = []
			// }
		},
		methods: {
			findindex(list,data){
				for (var i = 0; i < list.length; i++) {
					if ( list[i] === data ) return i
				}
				return -1
			},
			choise(id){
				// console.log(this.findindex(this.choiseitems,id))
				const inindex = this.findindex(this.choiseitems,id)
				if (inindex === -1) {
					this.choiseitems.push(id)
					console.log(this.choiseitems)
				} else {
					this.choiseitems.splice(inindex,1)
					console.log(this.choiseitems)
				}
			},
			goToPage(typ,id,name) {
				if (!id) return;
				uni.navigateTo({
					url: '/pages/tabbar/tabbar-1/'+ typ +'?id='+ encodeURIComponent(id) + '&name=' + encodeURIComponent(name)
				});
			},
		}
	}
</script>

<style>
/deep/.uni-list--lg {
    height: 60px !important;
    width: 60px !important;
}
/deep/.uni-switch-input{
    border-color: #b3ccd0 !important;
    background-color: #b3ccd0 !important;
}

</style>

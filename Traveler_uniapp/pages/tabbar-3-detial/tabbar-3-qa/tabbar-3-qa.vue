<template>
	<view class="content">
		<!-- <view style="height: 37px;"></view> -->
		<uni-group title="图片-最多上传9张" class="place-image-box">
			<uni-file-picker limit="9" v-model="image" class="place-image" @select="select"></uni-file-picker>
		</uni-group>
		<uni-group title="地点名称" class="place-content-box">
				<uni-easyinput class="name-box" :inputBorder="false"  v-model="name" placeholder="地点名称" clearable ></uni-easyinput>
		</uni-group>
		<uni-group title="地点定位" class="place-content-box">
		<uni-data-picker :localdata="this.cityData"  v-model="city" popup-title="地点定位" @change="onchange" @nodeclick="onnodeclick"></uni-data-picker>
		<uni-easyinput v-model="gaode" style="margin-top: 10px;" placeholder="高德地图APP分享定位链接"></uni-easyinput>
		</uni-group>
		<uni-group title="词条类型" class="place-content-box">
			<uni-data-checkbox v-model="tag" mode="tag" :localdata="tagsData" @change="changetag"></uni-data-checkbox>
		</uni-group>
		<uni-group title="地点介绍" class="place-desc-box">
			<robin-editor class="editor" 
			    @cancel="hideEditor" 
			    @save="saveEditor" 
			    v-model="desc"
				:tools="toollist"
			    :muiltImage="true">
			</robin-editor>
		</uni-group>
		<!-- <button @click="open">打开弹窗</button> -->
		<uni-popup ref="popup">
		    <uni-list>
		        <uni-list-item title="自己可见" @click="myself" clickable></uni-list-item>
		        <uni-list-item title="公开可见" @click="ourself" clickable></uni-list-item>
		        <uni-list-item title="保存退出" @click="goout" clickable></uni-list-item>
		    </uni-list>
		</uni-popup>
	</view>
</template>

<script>
	import imgUpload from '../../../components/linzq-imgUpload/linzq-imgUpload.vue'
	export default {
		data() {
			return {
				toollist: [
					'preview',//预览	
					'h1','h2','h3','h4','h5','h6',//标题	
					'font',//字体大小
					'bold',//加粗
					'italic',//斜体	
					'underline',//下划线	
					'strike',//删除线
					'align-left',//右对齐	
					'align-center',//居中	
					'align-right',//左对齐
					'indent',//缩进
					'outdent',//缩进	
					'rtl',//书写方向	
					// 'color',//字体颜色,有bug先关掉
					// 'backgroundColor',//背景色,有bug先关掉
					'image',//插入图片	
					'date',//插入日期	
					'list-ordered','list-bullet',//列表
					'list-check',//不显示但是是有东西的，可勾选方框
					'divider',//分割线
					'sub',//上下标	
					'super',//上下标
					'undo',//撤销
					'redo',//恢复撤销
					'remove',//清除格式
					'clear',//清空	
				],
				autoupload:false,
				gettime: '',
				image: [],
				name: '',
				desc: '',
				postimg: null,
				tagsData: [
					{
						'value': 'play',
						'text': '景玩'
					},
					{
						'value': 'eat',
						'text': '餐食'
					},
					{
						'value': 'hotel',
						'text': '住宿'
					},
					{
						'value': 'go',
						'text': '出行'
					},
					{
						'value': 'other',
						'text': '其他'
					},
				],
				tag: '',
				city: '',
				cityData: [],
				gaode: ''
			}
		},
		components:{
			imgUpload
		},
		onLoad() {

		},
		created() {
			this.getCityData()
			if (uni.getStorageSync('place-image')) { this.image = uni.getStorageSync('place-image') }
			if (uni.getStorageSync('place-name')) { this.name = uni.getStorageSync('place-name') }
			if (uni.getStorageSync('place-desc')) { this.desc = uni.getStorageSync('place-desc')}
			if (uni.getStorageSync('place-tag')) { this.tag = uni.getStorageSync('place-tag')}
			if (uni.getStorageSync('place-city')) { this.city = uni.getStorageSync('place-city')}
			if (uni.getStorageSync('place-gaode')) { this.gaode = uni.getStorageSync('place-gaode')}
		},
		methods: {
			getCityData () {
				this.$http.get('city-tree/').then(res=> {
					this.cityData = res.data.data
					// console.log(this.cityData)
				})
			},
			onnodeclick(node) {
				// console.log(node.text)
				// uni.setStorageSync('city', node.text)
			},
			onchange(e) {
				const value = e.detail.value
				// console.log(e.detail.value, e.detail.text)
			},
			changetag(e){
				console.log('e:',e);
			},
			// 上传图片
			select(e){
				console.log('选择文件：',e)
				const tempFilePaths = e.tempFilePaths;
				e.tempFilePaths.forEach((item, index) => { //本地选中的图片组
					let yy = new Date().getFullYear();
				　　let mm = new Date().getMonth()+1;
				　　let dd = new Date().getDate();
				　　let hh = new Date().getHours();
				　　let mf = new Date().getMinutes()<10 ? '0'+new Date().getMinutes() : new Date().getMinutes();
				　　let ss = new Date().getSeconds()<10 ? '0'+new Date().getSeconds() : new Date().getSeconds();
				　　const gettime = yy+'_'+mm+'_'+dd+'_'+hh+'_'+mf+'_'+ss;
					uni.uploadFile({ //上传图片
						url: uni.getStorageSync('urlip') + '/imgs/', //上传接口地址
						filePath: tempFilePaths[0],
						name: 'img',
						formData: {
						    'name': gettime
						},
						header: {
							// 'Content-Type': 'application/x-www-form-urlencoded',
							'Authorization': 'Bearer ' + uni.getStorageSync('token')
						},
						success: (uploadFileRes) => {
						    console.log(JSON.parse(uploadFileRes.data));
						    console.log(this.image);
							this.image.push(JSON.parse(uploadFileRes.data).data)
						}
					});

				})
			},
			// 取消并保存内容
			hideEditor: function() {
				// 保存当前数据
				// uni.setStorageSync('place-image', this.image)
				// uni.setStorageSync('place-name', this.name)
				// uni.setStorageSync('place-tag', this.tag)
			    // this.$router.go(-1)
				uni.navigateBack()
			},
			myself(){
				console.log('自己可见')
				const imgids = []
				for (let i = 0; i < this.image.length; i++) {
					console.log(this.image[i].id)
					imgids.push(this.image[i].id)
				}
				console.log(imgids)
				this.$http.post('place/', {
					imgs: imgids,
					name: this.name,
					desc: this.desc,
					typ: this.tag,
					city: this.city,
					gaode: this.gaode,
					show: false
				}).then(res=> {
					console.log(res.data)
					// 清空缓存
					uni.removeStorageSync('place-image')
					uni.removeStorageSync('place-name')
					uni.removeStorageSync('place-desc')
					uni.removeStorageSync('place-tag')
					uni.removeStorageSync('place-city')
					uni.removeStorageSync('place-gaode')
					// 避免还没上传完就跳转回首页
					setTimeout(()=>{
						uni.reLaunch({
							url: '/pages/tabbar/tabbar-1/tabbar-1'
						})
					},1000)
				})
			},
			ourself(){
				console.log('大家可见')
				const imgids = []
				for (let i = 0; i < this.image.length; i++) {
					console.log(this.image[i].id)
					imgids.push(this.image[i].id)
				}
				console.log(imgids)
				this.$http.post('place/', {
					imgs: imgids,
					name: this.name,
					desc: this.desc,
					typ: this.tag,
					city: this.city,
					gaode: this.gaode,
					show: true
				}).then(res=> {
					console.log(res.data)
					// 清空缓存
					uni.removeStorageSync('place-image')
					uni.removeStorageSync('place-name')
					uni.removeStorageSync('place-desc')
					uni.removeStorageSync('place-tag')
					uni.removeStorageSync('place-city')
					uni.removeStorageSync('place-gaode')
					// 避免还没上传完就跳转回首页
					setTimeout(()=>{
						uni.reLaunch({
							url: '/pages/tabbar/tabbar-1/tabbar-1'
						})
					},1000)
				})
			},
			goout(){
				uni.reLaunch({
					url: '/pages/tabbar/tabbar-1/tabbar-1'
				})
			},
			saveEditor: function(e) {
				// 保存当前数据
				uni.setStorageSync('place-image', this.image)
				uni.setStorageSync('place-name', this.name)
				uni.setStorageSync('place-desc', e.html)// 因为取不出来，直接在组件里面保存了
				uni.setStorageSync('place-tag', this.tag)
				uni.setStorageSync('place-city', this.city)
				uni.setStorageSync('place-gaode', this.gaode)
			    // 赋值
			    this.desc = e.html
				if (this.tag === '') {
					this.tag = 1
				}
				if (this.city === '') {
					this.city = 1
				}
				// 弹出层选择
				this.$refs.popup.open('center')
				// console.log(e.html)
				// console.log(this.desc )
				// this.$http.post('place/', {
				// 	img: this.image.id,
				// 	name: this.name,
				// 	content: this.content,
				// 	desc: e.html,
				// 	tags: this.tag
				// }).then(res=> {
				// 	console.log(res.data)
				// 	// 清空缓存
				// 	uni.removeStorageSync('place-image')
				// 	uni.removeStorageSync('place-name')
				// 	uni.removeStorageSync('place-desc')

				// 	// 避免还没上传完就跳转回首页
				// 	setTimeout(()=>{
				// 		uni.reLaunch({
				// 			url: '/pages/tabbar/tabbar-1/tabbar-1'
				// 		})
				// 	},1000)
				// })
				// console.log(res.data)
			    // 跳转回首页
				// uni.reLaunch({
				// 	url: '/pages/tabbar/tabbar-1/tabbar-1'
				// }).then(this.$router.go(0))
			}
		}
	}
</script>

<style>
.place-image-box {
	margin: 0px !important;
}
.place-content-box {
	margin: 0px !important;
}
.place-desc-box {
	margin: 0px !important;
}
/deep/.name-box .uni-easyinput__content-input {
	border-bottom: 1px solid #e5e5e5 !important;
}
/deep/.content-box .uni-easyinput__content .uni-easyinput__content-textarea {
	min-height: 50px !important;
	height: 50px !important;
}
.editor {
	padding: 0px;
	border: 1px solid #e5e5e5;
}
/deep/.container {
	margin-top: 0px !important;
}
/deep/.uni-data-checklist .checklist-group .checklist-box.is--tag {
    margin-right: 10px !important;
    padding: 5px 10px !important;
}
/deep/.uni-data-checklist .checklist-group .checklist-box.is--tag.is-checked {
	border-color: #b3ccd0 !important;
	background-color: #b3ccd0 !important;
}
.editor {
	min-height: 500px;
}
</style>

<template>
	<view class="content">
		<!-- <view style="height: 37px;"></view> -->
		<uni-group title="文章封面" class="blog-image-box">
			<uni-file-picker
			limit="1"
			v-model="image"
			class="blog-image"
			@select="select"
			></uni-file-picker>
		</uni-group>
		<uni-group title="文章摘要" class="blog-content-box">
				<uni-easyinput class="name-box" :inputBorder="false"  v-model="name" placeholder="标题" clearable ></uni-easyinput>
				<uni-easyinput class="content-box" type="textarea"  v-model="content" placeholder="摘要" clearable ></uni-easyinput>
				<!-- <uni-fav :checked="checked" class="favBtn" circle="true" bgColor="#dd524d" bgColorChecked="#007aff" @click="onClick"/> -->
		</uni-group>
		<uni-group title="文章类型" class="blog-content-box">
			<uni-data-checkbox v-model="tag" mode="tag" :localdata="tagsData" @change="changetag"></uni-data-checkbox>
		</uni-group>
		<uni-group title="文章内容" class="blog-desc-box">
			<robin-editor class="editor" 
			    @cancel="hideEditor" 
			    @save="saveEditor" 
			    v-model="desc"
			    :imageUploader="uploadImg"
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
				// count: 9,
				// name: 'img',   //必填
				// url: uni.getStorageSync('urlip') + '/imgs/',    //必填
				// header: {
				// 	// 'Content-Type': 'application/x-www-form-urlencoded',
				// 	'Authorization': 'Bearer ' + uni.getStorageSync('token')
				// },
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
				image: null,
				name: '',
				content: '',
				desc: '',
				tag: '',
				tagsData: [],//blog-tags-option
				postimg: null
			}
		},
		components:{
			imgUpload
		},
		onLoad() {

		},
		created() {
			this.getTagsData()
			if (uni.getStorageSync('blog-image')) { this.image = uni.getStorageSync('blog-image') }
			if (uni.getStorageSync('blog-name')) { this.name = uni.getStorageSync('blog-name') }
			if (uni.getStorageSync('blog-content')) { this.content = uni.getStorageSync('blog-content') }
			if (uni.getStorageSync('blog-desc')) { this.desc = uni.getStorageSync('blog-desc')}
			if (uni.getStorageSync('blog-tag')) { this.tag = uni.getStorageSync('blog-tag')}
		},
		methods: {
			getTagsData(){
				this.$http.get('blog-tags-option/').then(res=> {
					this.tagsData = res.data.data
				})
			},
			changetag(e){
				console.log('e:',e);
			},
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
							this.image = JSON.parse(uploadFileRes.data).data
						}
					});

				})
			},
			hideEditor: function() {
				// 保存当前数据
				// uni.setStorageSync('blog-image', this.image)
				// uni.setStorageSync('blog-name', this.name)
				// uni.setStorageSync('blog-content', this.content)
				// uni.setStorageSync('blog-desc', e.html)// 因为取不出来，直接在组件里面保存了
				// uni.setStorageSync('blog-tag', this.tag)
			    // this.$router.go(-1)
				uni.navigateBack()
			},
			myself(){
				console.log('自己可见')
				this.$http.post('blog/', {
					img: this.image.id,
					name: this.name,
					content: this.content,
					desc: this.desc,
					tags: this.tag,
					show: false
				}).then(res=> {
					console.log(res.data)
					// 清空缓存
					uni.removeStorageSync('blog-image')
					uni.removeStorageSync('blog-name')
					uni.removeStorageSync('blog-content')
					uni.removeStorageSync('blog-desc')
					uni.removeStorageSync('blog-tag')
				
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
				this.$http.post('blog/', {
					img: this.image.id,
					name: this.name,
					content: this.content,
					desc: this.desc,
					tags: this.tag,
					show: true
				}).then(res=> {
					console.log(res.data)
					// 清空缓存
					uni.removeStorageSync('blog-image')
					uni.removeStorageSync('blog-name')
					uni.removeStorageSync('blog-content')
					uni.removeStorageSync('blog-desc')
					uni.removeStorageSync('blog-tag')
				
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
				uni.setStorageSync('blog-image', this.image)
				uni.setStorageSync('blog-name', this.name)
				uni.setStorageSync('blog-content', this.content)
				uni.setStorageSync('blog-desc', e.html)// 因为取不出来，直接在组件里面保存了
				uni.setStorageSync('blog-tag', this.tag)
				
			    // 赋值
			    this.desc = e.html
				if (this.tag === '') {
					this.tag = 1
				}
				
				// 弹出层选择
				this.$refs.popup.open('center')
				// console.log(e.html)
				// console.log(this.desc )
				// this.$http.post('blog/', {
				// 	img: this.image.id,
				// 	name: this.name,
				// 	content: this.content,
				// 	desc: e.html,
				// 	tags: this.tag
				// }).then(res=> {
				// 	console.log(res.data)
				// 	// 清空缓存
				// 	uni.removeStorageSync('blog-image')
				// 	uni.removeStorageSync('blog-name')
				// 	uni.removeStorageSync('blog-content')
				// 	uni.removeStorageSync('blog-desc')
				// 	uni.removeStorageSync('blog-tag')

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
			},
			objectURLToBlob(blodurl) {
				// uni.showLoading({
				// 	title: '压缩中...'
				// });
				return new Promise((resolve, reject) => {
					var http = new XMLHttpRequest();
					http.open('GET', blodurl, true);
					http.responseType = 'blob';
					http.onload = function(e) {
					    if (this.status == 200 || this.status === 0) {
						console.log('blod数据',this.response);
						// 在将blod数据转为file
					　　let yy = new Date().getFullYear();
					　　let mm = new Date().getMonth()+1;
					　　let dd = new Date().getDate();
					　　let hh = new Date().getHours();
					　　let mf = new Date().getMinutes()<10 ? '0'+new Date().getMinutes() : new Date().getMinutes();
					　　let ss = new Date().getSeconds()<10 ? '0'+new Date().getSeconds() : new Date().getSeconds();
					　　const gettime = yy+'_'+mm+'_'+dd+'_'+hh+'_'+mf+'_'+ss;
						
						let files = new window.File([this.response], gettime, { type: 'image' });
						console.log('blod数据转换file',files);
						resolve(files);
						// uni.hideLoading();
				        }
					};
					http.send();
				});
			},
			uploadImg: function(img, callback) {
				console.log(img)
			    // 构造图片名字
				this.getCurrentTime()
				const image_name = this.name + '_' + this.gettime
				// 转化图片
				this.objectURLToBlob(img).then(res=>{
					console.log('file',res);
					this.postimg = res
				}).then(()=>{
					// 上传图片
					console.log('typ',typeof this.postimg)
					// this.$http.post('imgs/',{name:image_name,img:this.postimg}).then(res=> {
					// 	console.log('上传图片测试', res)
					// 	// if (res.data.code === 200) {
					// 	// }
					// })
					//将图片链接传给回调函数
					callback(img)
				})
			},
			getCurrentTime() {
				//获取当前时间并打印
			　　let yy = new Date().getFullYear();
			　　let mm = new Date().getMonth()+1;
			　　let dd = new Date().getDate();
			　　let hh = new Date().getHours();
			　　let mf = new Date().getMinutes()<10 ? '0'+new Date().getMinutes() : new Date().getMinutes();
			　　let ss = new Date().getSeconds()<10 ? '0'+new Date().getSeconds() : new Date().getSeconds();
			　　this.gettime = yy+'_'+mm+'_'+dd+'_'+hh+'_'+mf+'_'+ss;
			　　console.log(this.gettime)  
			}
		}
	}
</script>

<style>
.blog-image-box {
	margin: 0px !important;
}
.blog-content-box {
	margin: 0px !important;
}
.blog-desc-box {
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
    margin-right: 5px !important;
    padding: 5px 5px !important;
}
/deep/.uni-data-checklist .checklist-group .checklist-box.is--tag.is-checked {
	border-color: #b3ccd0 !important;
	background-color: #b3ccd0 !important;
}
</style>

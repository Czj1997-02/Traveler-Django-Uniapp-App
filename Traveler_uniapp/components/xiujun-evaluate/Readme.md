### 评价 列表

评价列表组件，组件名：``uni-evaluate``，可预览图片

**使用方式：**

下载组件，在 ``script`` 中引用组件 

```javascript
import uniEvaluate from '../../components/xiujun-evaluate/uni-evaluate.vue';
export default {
    components: {uniEvaluate}
}
```

用法

```html
<uni-evaluate :list-data="列表数据" :rate="总评分"/>
```

**组件属性说明：**	

|属性名|类型|默认值	|说明|
|---|----|---|---|
|listData|Array|-|评价列表数据|
|rate|Number|-|总评分|
|isShowTotal|Boolean|true|是否显示总评价数量|
|isShowIcon|Boolean|true|是否显示评价头图标|

**listData属性说明：**

|属性名|类型|默认值|说明|
|---|----|---|---|
|header_img|String|-|用户头像|
|user_name|String| -      |用户名|
|rate|Number|-|评分|
|create_time|String|-|发表评论时间|
|content|String|-|评价内容文本|
|imgs|Array|-|评价内容图片格式['图片地址1','图片地址2']|

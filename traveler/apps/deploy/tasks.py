# from __future__ import absolute_import, unicode_literals
# from celery import shared_task

# from .models import *
# from django.contrib.auth.models import User
# from django.utils.timezone import now

# # date = models.DateField(verbose_name='日期', help_text='日期（DateField）')
# # news = models.TextField(verbose_name='信息', help_text='信息（TextField）', blank=True)
# # latitude = models.CharField(max_length=255, verbose_name='纬度', help_text='纬度', default='', blank=True)
# # way = models.CharField(max_length=255, verbose_name='来源', help_text='来源', default='', blank=True)

# # created_by = models.ForeignKey(User,  verbose_name='创建人',help_text='创建人（ForeignKey）', null=True, blank=True, on_delete=models.SET_NULL, related_name='newsflash_cb')
# # created_date = models.DateTimeField(verbose_name='创建时间', help_text='创建时间（DateTimeField）', null=True, blank=True, auto_now_add=True)
# # last_edited_by = models.ForeignKey(User,  verbose_name='最后编辑人',help_text='最后编辑人（ForeignKey）', null=True, blank=True, on_delete=models.SET_NULL, related_name='newsflash_eb')
# # last_edited_date = models.DateTimeField(verbose_name='最后编辑时间', help_text='最后编辑时间（DateTimeField）', null=True, blank=True, auto_now=True)
# # deleted = models.CharField(max_length=1, verbose_name='是否删除', help_text='是否删除（CharField，可选值：0，1）', choices=del_choices, default='0')

# news_url1 = 'https://3g.163.com/touch/reconstruct/article/list/BBM54PGAwangning/0-6.html'
# news_url2 = 'https://3g.163.com/touch/reconstruct/article/list/BA8EE5GMwangning/0-6.html'
# news_url3 = 'https://3g.163.com/touch/reconstruct/article/list/BA8D4A3Rwangning/0-6.html'
# from getapi import getNews

# @shared_task
# def get_NewsFlash():

#     newsdata1 = getNews(news_url1)
#     for thisnews in newsdata1:
#         # print(thisnews)
#         new_news = NewsFlash()
#         new_news.date = now()
#         new_news.news = thisnews['title']
#         new_news.latitude = '新闻'
#         new_news.way = thisnews['source']
#         new_news.url = thisnews['url']
#         new_news.created_by = User.objects.get(id=1)
#         new_news.last_edited_by = User.objects.get(id=1)
#         new_news.created_date = now()
#         new_news.last_edited_date = now()
#         new_news.save()
    
#     newsdata2 = getNews(news_url2)
#     for thisnews in newsdata2:
#         # print(thisnews)
#         new_news = NewsFlash()
#         new_news.date = now()
#         new_news.news = thisnews['title']
#         new_news.latitude = '财经'
#         new_news.way = thisnews['source']
#         new_news.url = thisnews['url']
#         new_news.created_by = User.objects.get(id=1)
#         new_news.last_edited_by = User.objects.get(id=1)
#         new_news.created_date = now()
#         new_news.last_edited_date = now()
#         new_news.save()
    
#     newsdata3 = getNews(news_url3)
#     for thisnews in newsdata3:
#         # print(thisnews)
#         new_news = NewsFlash()
#         new_news.date = now()
#         new_news.news = thisnews['title']
#         new_news.latitude = '科技'
#         new_news.way = thisnews['source']
#         new_news.url = thisnews['url']
#         new_news.created_by = User.objects.get(id=1)
#         new_news.last_edited_by = User.objects.get(id=1)
#         new_news.created_date = now()
#         new_news.last_edited_date = now()
#         new_news.save()

#     return 'Reset Tasks Success!'


# @shared_task
# def get_DLTData():
#     from lxml import etree
#     from .getnum import getdata,geturl
#     # 获取数据
#     urldata = geturl()

#     #解析数据
#     alldata = etree.HTML(urldata)
#     # print(alldata)
#     nownum = LotteryData.objects.all().count()
#     # print(nownum)
#     beginNum = 20
#     if nownum < 1000:
#         beginNum = 1000

#     for i in range(beginNum,0,-1):
#         path1 = r'//*[@id="tdata"]/tr['+str(i)+']/td[1]'
#         path2 = r'//*[@id="tdata"]/tr['+str(i)+']/td[2]'
#         path3 = r'//*[@id="tdata"]/tr['+str(i)+']/td[3]'
#         path4 = r'//*[@id="tdata"]/tr['+str(i)+']/td[4]'
#         path5 = r'//*[@id="tdata"]/tr['+str(i)+']/td[5]'
#         path6 = r'//*[@id="tdata"]/tr['+str(i)+']/td[6]'
#         path7 = r'//*[@id="tdata"]/tr['+str(i)+']/td[7]'
#         path8 = r'//*[@id="tdata"]/tr['+str(i)+']/td[8]'
#         path9 = r'//*[@id="tdata"]/tr['+str(i)+']/td[15]'
#         ordernum=int('20'+str(alldata.xpath(path1)[0].text))

#         #查看是否存在这一期，如果不存在的话，创建这一期
#         # thisorder = LotteryData()
#         thisorder = LotteryData.objects.filter(order__exact=ordernum).first()
#         if thisorder == None:
#             thisorder = LotteryData()
#             #从前2001期到现在的每一期数据
#             thisorder.order = ordernum
#             thisorder.red1 =  int(alldata.xpath(path2)[0].text)
#             thisorder.red2 =  int(alldata.xpath(path3)[0].text)
#             thisorder.red3 =  int(alldata.xpath(path4)[0].text)
#             thisorder.red4 =  int(alldata.xpath(path5)[0].text)
#             thisorder.red5 =  int(alldata.xpath(path6)[0].text)
#             thisorder.blue1 =  int(alldata.xpath(path7)[0].text)
#             thisorder.blue2 =  int(alldata.xpath(path8)[0].text)
#             thisorder.date =  alldata.xpath(path9)[0].text
#             thisorder.save()
    
#     return 'get DLT Data Success!'

# @shared_task
# def get_GuessData():
#     from .guess import predict
#     maxnum = LotteryData.objects.all().order_by('-id') .first().pk
#     predict(maxnum)

#     return 'get Guess Data Success!'
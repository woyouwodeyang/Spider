import os
import time
import re
from bs4 import BeautifulSoup
import requests
import random
import shutil

class p():
	def __printVersion__(self):				#私有方法
		print('Author:Quchao')
		print('Version:V1.1.0')
		print('Copyright © 2017 Free Software Foundation, Inc.  License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.')
		print('This is free software: you are free to change and redistribute it.  There is NO WARRANTY, to the extent permitted by law.'+'\n')
	def printInfo(self,string):									#打印爬取状态
		sz = os.get_terminal_size()						#获取终端的长度和宽度
		columns = sz.columns
		#print('*'*columns+'\n')
		print('%s'%string+'\n')
		#print('*'*columns+'\n')

def getUrl():											#获得网页的有效url
	p().printInfo('请输入要爬取的网址,若要爬取多个网页，请将变化的数字(暂时只支持数字)用一队大括号代替,多个用多个大括号,目前只支持两个,没有大扩号默认代表爬取一个单个网页')
	originUrl = input('请输入网站:')
	if not originUrl.startswith('http'):	#避免输入的时候缺少http(s)而出错
		originUrl = 'http://'+originUrl
	Timex = originUrl.count('{}')				#统计{}的个数
	if Timex==0:
		url = [originUrl]				#单个网页
	elif Timex==1:
		try:
			start = int(input('请输入初始变化网页,避免以0开头:'))
			end = int(input('请输入结束爬取页:'))+1
			step = int(input('请输入每隔几页爬取一次:'))
		except:
			p().printInfo('输入有误,请重新输入!!!!!')
		url = [originUrl.format(str(i)) for i in range(start,end,step)] #是一个列表
	elif Timex==2:
		start = int(input('请输入初始变化网页,避免以0开头:'))
		end = int(input('请输入结束爬取页:'))+1
		step = int(input('请输入没隔几页爬取一次:')) #与第一次的意义有所不同
		start1 = int(input('请输入第二次变化的初始网页:'))
		end1 = int(input('请输入第二次变化的结束网页:'))
		step1 = int(input('请输入第二次变化的步长:'))
		#可以输入多个{}{}{}
		url = [originUrl.format(str(i),str(j)) for i in range(start,end,step) for j in range(start1,end1+1,step1)]
	return url

def Browse_Way():							#定义访问模式
	choice = input('请选择访问模式(1->电脑，2->安卓，3->苹果,4->ipad):')
	while not choice.isdigit() or not 1<=int(choice)<=4:    #判断输入是否合法并且是否在范围内,for i in range()  效率低
		choice = input('请选择访问模式(1->电脑，2->安卓，3->苹果,4->ipad):')
	headers = [{'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'},
	{'user-agent':'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36'},
	{'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'},
	{'User-Agent':'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}]
	headers = headers[int(choice)-1]
	return headers

class Dir():
	rootPath = ''							#在这个类中可以直接使用rootPath变量
	def deleteFiles(self,path):				#判断目录是否为空或者只有一张图片，然后删除
		number=os.walk(path,topdown=True,onerror=None,followlinks=False)
		for (root,dirs,files) in number:
			#print(root)			#返回文件夹下的文件下名称(路径)
			#print(files)		#返回文件里面的文件，不包括文件夹
			#print(dirs)			#返回文件夹里面的文件夹
			#print('当前文件夹中文件夹的数目%d'%len(dirs))
			if (len(dirs)==0) and (len(files)<1):			#如果当前目录下没有文件夹并且文件数目小于2个的时候删除文件夹
				shutil.rmtree(root)   						#print('已经删除删除%s'%root)

	def MakeDir(slef,*title):				#随时间创建文件夹,名字后面加入标题,title为可选参数
		realTime = time.strftime("%Y%m%d%I%M%S", time.localtime())
		operateSystem = os.name
		try:						#避免用户乱输入导致程序的结束
			if not len(Dir.rootPath) == 0:
				if operateSystem == 'posix' and not Dir.rootPath.startswith('/'):
					#判断操作系统并且判断用户输入的是绝对路径还是相对路径
					Dir.rootPath = os.getcwd()+'/'+Dir.rootPath
				elif operateSystem == 'nt' and Dir.rootPath.find(':') == -1:
					Dir.rootPath = os.getcwd()+'/'+Dir.rootPath
				rootPath = Dir.rootPath+'/'+realTime+'/'
				if not len(title) == 0:
					rootPath = Dir.rootPath+'/'+realTime+'/'+str(title[0])+'/'
				os.makedirs(rootPath)				#默认在当前文件夹下创建)
			else:
				os.mmm()							#随便产生一个错误
		except:
			p().printInfo('创建文件夹失败，将采用系统默认路径')
			if operateSystem == 'posix':								#判断操作系统
				rootPath = "/mnt/d/python/picture/"				#文件保存根目录
			elif operateSystem == 'nt':
				rootPath = "D:/python/picture/"			#文件保存根目录,/ \ 都可以
			rootPath = rootPath+realTime+'/'
			if not len(title) == 0:						#判断输入是否非空
				rootPath = rootPath+str(title[0])+'/'
			try:										#避免权限问题出现创建文件夹失败
				if not os.path.exists(rootPath):			#判断根目录是否存在
					os.makedirs(rootPath)						#比mkdir更强大，解决前一文件夹不存在的错误
			except:
				tmpDir = os.getcwd()+'/pictures/'+realTime+'/'		#在当前目录下建立文件夹
				if not len(title) == 0:
					tmpDir = os.getcwd()+'/pictures/'+realTime+'/'+str(title[0])+'/'
				os.makedirs(tmpDir)
				rootPath = tmpDir
		return rootPath										#函数返回值

class RetAllImageUrl:
	label = ''					#默认属性，可以修改
	def RetAllImageUrl(self,rtext):					#解析网页，返回所有图片的url
		soup = BeautifulSoup(rtext,'html.parser')
		p = []			#用来临时保存所有网址
		try:			#防止网址错误而导致程序结束
			#title = soup.select('div > strong.title')[0].text			#在此修改爬取的标题
			title = soup.select(RetAllImageUrl.label)[0].text
			title = title.strip()					#去除标题的空格
		except:
			title = ''
			pass					#有错时，继续后面程序的执行
		soup = soup.prettify()			#格式化解析网页,变成了字符型
		try:
			AllIamgeUrl = re.findall(r'.*="(.*\.(jpg|png|gif).*)"',soup)
			#在soup中搜索所有以什么="什么.jpg或png或gif"的东西,结果为括号里面的东西,二维列表
			#AllIamgeUrl中的第二个元素为图片类型,末尾加.*是为了找出经过修饰后的图片
			for i in AllIamgeUrl:					#判断类型,找出合法的图片地址
				if i[1] == 'jpg':
					f = (i[0].split('jpg'))[0]+'jpg'
				elif i[1] == 'png':
					f = (i[0].split('png'))[0]+'png'
				elif i[1] == 'gif':
					f = (i[0].split('gif'))[0]+'gif'
				p.append(f)
			AllIamgeUrl = p
			return (AllIamgeUrl,title)  #AllIamgeUrl为一维列表
		except:
			p().printInfo('当前网站没有图片或者解析不出图片')

########################################################################################################################################
#程序从下面开始正式开始
########################################################################################################################################

#添加代码信息，作者，版本号等
p().__printVersion__()

global j
j = 0								#统计爬取图片的张数
number = 0							#遍历网址的下标
failUrl = []						#统计爬取失败的url
url = getUrl()						#调用getUrl函数,获取需要爬取的网站，返回列表类型
size = len(url)						#取得网址的数量
headers = Browse_Way()				#调用Browse_Way函数，设置浏览方式
Dir.rootPath = input('请输入文件保存路径:')
RetAllImageUrl.label = input('请输入标题所对应的标签(默认为空):')

while number < size:				#爬取多个网页,外循环
	k = 0								#统计单网页爬取时的进度
	p().printInfo('与服务器通信中......')
	try:
		p().printInfo('即将爬取的网址为:'+str(url[number]))
		r = requests.get(url[number],headers = headers)				#linux下无网络会一直等下去
		if int(r.status_code) == 200:								#通信成功才会进行后面的操作
			p().printInfo('与服务器通信成功')
			#number += 1
			r.encoding = r.apparent_encoding					#让网页不出现乱码
			rtext = r.text
			(AllIamgeUrl,title) = RetAllImageUrl().RetAllImageUrl(rtext)			#返回所有图像网址
			#类后面的函数要加一个(),以区分
			print(title)
			rootPath = Dir().MakeDir(title)
#####################################################################
#以下为写入到文件的代码
#####################################################################
			for i in AllIamgeUrl:				#内循环，AllIamgeUrl为一个网页中的所有网页
				imageUrl = i
				if  not imageUrl.startswith('http'):					#查找图片网址是否缺省了http或这https
					imageUrl = 'http:' + imageUrl			#解析的网页没有http字段
				path = rootPath + imageUrl.split('/')[-1]		#创建路径
				if  not os.path.exists(path):						#判断文件是否存在,路径不存在执行下面的语句
					try:			#防止一些错误的网址导致程序的结束
						ri = requests.get(imageUrl)
						with open(path,'wb') as f:				#写到path路径里面，以二进制方式写
							p().printInfo('正在爬取第%d张图片,文件将保存到%s'%(j,path))
							f.write(ri.content)						#with会自动关闭文件
							j+=1
							#p().printInfo('爬取第%d张图片,文件已保存到%s'%(j,path))
					except:
						p().printInfo('爬取'+str(imageUrl)+'失败')
						failUrl.append(imageUrl)		#将错误的url加入到failUrl中
						#pass
					CP = (k+1)/len(AllIamgeUrl)*100
					TP = (number+1)/len(url)*100
					if CP > 100:
						CP = CP%100
					p().printInfo('当前网页爬取进度为:'+str(CP)+'%,'+'总的网页爬取进度为:'+str(TP)+'%.')
					k += 1
			#time.sleep(random.randint(1,5))	#随机1到5秒访问一次，防止网站封ip '''
			Dir().deleteFiles(rootPath)
			time.sleep(random.randint(1,10)/10)
			number += 1
		else:
			number += 1						#避免一直在错误网址循环
			p().printInfo('访问网站失败,错误代码:'+str(r.status_code))
	except:
		p().printInfo('响应超时,可能是无网络或者网址错误或者无法访问该网站') #如果有错不会执行后面的语句
		number += 1				#避免由于中途的一个错误而导致程序的结束
		continue
print('本次一共爬取%d张照片'%j)
if not len(failUrl) == 0:
	print('以下网址爬取失败')
	for i in failUrl:
		print('网址'+i+'爬取失败')
input('请按任意键结束')

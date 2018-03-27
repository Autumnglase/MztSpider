from bs4 import BeautifulSoup
import requests
import os
from tkinter import *
import threading
from tkinter.scrolledtext import ScrolledText
import time
url='http://www.mzitu.com/'
headers={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Host':'i.meizitu.net',
'Referer':'',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}
headers1={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'www.mzitu.com',
'Referer':'http://www.mzitu.com/110847',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}
path= '/spider/'
d={}
s=[]
root = Tk()
root.title("爬取妹子图（首页热门部分）")
root.geometry('500x500')
t = ScrolledText(root, width=20, height=20, background='#EECFA1')
t.pack(expand=1, fill="both")
localtime = time.asctime( time.localtime(time.time()) )
class thread1(threading.Thread):
    def run(self):
        def sendmsg(msg):
            t.insert(END, str(msg) + '\n')
            t.see(END)
        def pic_download(page,start,end,path1):#分别是：要爬的页面，开始的张数，结束张数,保存路径
            for i in range(start,end):
                end+=1
                adrs=page+str(i)
                try:
                    data = requests.get(adrs, headers=headers1, timeout=3).text
                    soup = BeautifulSoup(data, 'lxml')
                    images = soup.select('div.main-image')
                    image = re.search(r'src="(.*?)"/>', str(images))
                    z = image.group(1)
                    sendmsg('正在抓取:  ' + z)
                    headers['Referer'] = adrs
                    try:
                        r = requests.get(z, headers=headers, timeout=3)
                        sendmsg('正在下载:  ' + z[-9:])
                        with open(path1 + z[-9:], 'wb')as jpg:
                            jpg.write(r.content)
                    except requests.exceptions.ReadTimeout:
                        sendmsg('进入图片页面失败')
                        s.append(i)
                    except requests.exceptions.ConnectionError:
                        sendmsg('进入图片页面失败')
                        s.append(i)
                except requests.exceptions.ConnectionError:
                    sendmsg('下载图片失败')
                    s.append(i)
                except requests.exceptions.ReadTimeout:
                    sendmsg('下载图片失败')
                    s.append(i)
            d[z]=str(s)
            s.clear()
        def linkstart():
            def girlsilike(i,name):#name must be a str!
                if str(title).find(name) + 1:
                    path2 = path + name+'专辑/' + str(title) + '/'
                    isExists1 = os.path.exists(path2)
                    if not isExists1:
                        try:
                            os.makedirs(path2)
                            pic_download(i + '/', 1, int(end), path2)
                        except NotADirectoryError:
                            path2 = path + name+'专辑/' + i[-6:] + '/'
                            isExists1 = os.path.exists(path2)
                            if not isExists1:
                                os.makedirs(path2)
                                pic_download(i + '/', 1, int(end), path2)
                        except OSError:
                            path2 = path + name+'专辑/' + i[-6:] + '/'
                            isExists1 = os.path.exists(path2)
                            if not isExists1:
                                os.makedirs(path2)
                                pic_download(i + '/', 1, int(end), path2)
                    # pic_download(i + '/', 1, int(end), path2)
            try:
                data = requests.get(url, headers=headers1, timeout=3).text
                soup = BeautifulSoup(data, 'lxml')
                images = soup.select('ul#pins')
                image = re.findall('<span><a href="(.*?)" target="_blank"', str(images))
                for i in image:
                    # 获取图片张数
                    try:
                        data = requests.get(i, headers=headers1, timeout=3).text
                        soup = BeautifulSoup(data, 'lxml')
                        quantity = re.findall('<span>(.*?)</span></a>', str(soup))
                        title = re.findall('main-title">(.*?)</h2>', str(soup))
                        end = quantity[-2]
                        path1 = path + str(title) + '/'
                        isExists = os.path.exists(path1)

                        if not isExists:
                            try:
                                os.makedirs(path1)
                                pic_download(i + '/', 1, int(end), path1)
                            except NotADirectoryError:
                                path1 = path + i[-6:] + '/'
                                isExists = os.path.exists(path1)
                                if not isExists:
                                    os.makedirs(path1)
                                    pic_download(i + '/', 1, int(end), path1)
                            except OSError:
                                path1 = path + i[-6:] + '/'
                                isExists = os.path.exists(path1)
                                if not isExists:
                                    os.makedirs(path1)
                                    pic_download(i + '/', 1, int(end), path1)

                        girlsilike(i,'唐琪儿')#在这里添加喜欢的人
                    except requests.exceptions.ReadTimeout:
                        sendmsg('查找页数失败')
                        d[i]=0
                    except requests.exceptions.ConnectionError:
                        sendmsg('查找页数失败')
                        d[i] = 0
            except requests.exceptions.ReadTimeout:
                sendmsg('请求首页失败')
                d[url] = 0
            except requests.exceptions.ConnectionError:
                sendmsg('请求首页失败')
                d[url] = 0
            sendmsg('没有下载到的图片：')
            sendmsg(d)
            with open(path+'misspics.txt', 'a')as txt:
                txt.write(str(d)+localtime+'\n')
        linkstart()
t1=thread1()
t1.start()
root.mainloop()

sys.exit(0)
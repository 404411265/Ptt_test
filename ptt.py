# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
import demjson
payload={
    'from':'/bbs/Gossiping/M.1505346477.A.8F6.html' ,
    'yes':'yes'
}
address='https://www.ptt.cc/bbs/Gossiping/M.1505346477.A.8F6.html'
rs = requests.session()
res = rs.post('https://www.ptt.cc/ask/over18',data=payload)
res = rs.get(address)
soup=BeautifulSoup(res.text,"lxml")

pushdict={}
txt = soup.find('div',{"id":"main-content"})

h=soup.select('.article-metaline')
totaldict={
    'author' : h[0].contents[1].text  ,            ###  add 作者.文章.時間 看板
    'article' : h[1].contents[1].text  ,
    'time' : h[2].contents[1].text
}

for message in soup.select('#main-content')[0].contents[0:4]:       ###  del 作者.文章.時間 看板
    message.extract()

for frm in soup.select('.f2'):                                      ###  del 來自
    frm.extract()

num=1
for push in soup.find_all('div', {"class":"push"}):      ###  add 推文
    pre={
        'tag':push.contents[0].text ,                               ###  del 推文
        'userid':push.contents[1].text ,
        'content':push.contents[2].text 
    }
    pushdict[str(num)]=pre
    num+=1
    push.extract()

txt=txt.text.replace('\n',"")
totaldict['content']=txt
totaldict['push']=pushdict

totaldict=demjson.decode(str(totaldict))
f=open('1.json','w',encoding='utf-8')
json.dump(totaldict,f,indent=5, sort_keys=True,ensure_ascii=False)
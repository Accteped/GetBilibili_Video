
import requests
import json
import random
import time
import re
import os

file_ = open('Headers.txt')
str_ = file_.readlines()

str_[0] = re.sub(r"\n","",str_[0])

headers = {
    'User-Agent': '',
    'referer': ''
    }
headers['User-Agent'] = str_[0]
headers['referer'] = str_[1]

url1 = input('请输入bilibili视频地址:')
status_ = int(input('爬取视频是否为列表(1为是，0为否):'))
folder = re.sub(r"\/","//",input('请输入存储位置:'))
if folder[folder.__len__()-1] != '/':
    folder = folder + '\\'
print(folder)

if not os.path.exists(folder):
    os.makedirs(folder)
id = 1

res = requests.get(url=url1,headers=headers)
if res.status_code != 200:
    print('状态码异常，视频获取失败,Code:',res.status_code)
    print('请更新Headers')
    exit(0)

if status_ == 0:
    content = re.findall('<h1 data-title="(.*?)"',res.text)
    num = int(1)
    prime_num = int(-1)
else:
    content = re.findall('<div title="(.*?)"',res.text)
    prime_num = int(0)

    for i in range(len(content)):
        if '视频选集' == content[i]:
            prime_num = i
        if '点击打开迷你播放器' == content[i]:
            num = i - prime_num - 1

url = url1

for i in range(num):
    res = requests.get(url=url,headers=headers)

    obj = re.compile(r'window.__playinfo__=(.*?)</script>')
    
    title = content[prime_num+id]
    title = re.sub(r"[\/:?<>|']","",title)
    if res.status_code != 200:
        print('状态码异常，视频:',title,'Failed,Code:',res.status_code)
        id = id + 1
        continue
    print('正在下载第',id,'个视频:',title)
    html_data = obj.findall(res.text)[0]
    json_data = json.loads(html_data)

    videos = json_data['data']['dash']['video']
    video_url = videos[0]['baseUrl']

    audios = json_data['data']['dash']['audio']
    audio_url = audios[0]['baseUrl']

    #res1 = requests.get(url=video_url, headers=headers)

    #with open('test.mp4', mode = 'wb') as file:
    #    file.write(res1.content)

    res2 = requests.get(url=audio_url, headers=headers)

    with open(folder+title+'.mp3', mode = 'wb') as file:
        file.write(res2.content)

    print('Successful!成功下载第',id,'个视频:',title)
    id = id + 1
    time_div = [0.8,1.2,2.3,1.4,0.5]
    time_ = random.randint(0,4)
    time.sleep(time_div[time_])
    
    url = url1 + '&p=%d'%id

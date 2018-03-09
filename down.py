#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from syncart import  init
import os
import requests
import re
from pyquery import PyQuery as pyq
import shutil

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/34.0'
headers = {
    'Host': 'www.jianshu.com',
    'Referer': 'https://www.jianshu.com/',
    'User-Agent': agent,
    'Cookie': '"BAIDUID=0EF13E73AA44BEC88FEA2544E702DC33:FG=1; HMACCOUNT=774E92CFEC3ECFD8; BIDUPSID=0EF13E73AA44BEC88FEA2544E702DC33; PSTM=1520584656; BDRCVFR[gltLrB7qNCt]=mk3SLVN4HKm; PSINO=2; H_PS_PSSID=1454_19037_21113_20719; BDORZ=FFFB88E999055A3F8A630C64834BD6D0"'

}
headers_img = {
    'Host': 'upload-images.jianshu.io',
    'Referer': 'http://www.jianshu.com/',
    'User-Agent': agent
}




# title = ["068.与喵共舞35～春游故宫","067.友人录2~大媒婆关婧","066.朝花夕拾17~合唱队","065.看图说话1~麦霸","064.吃过什么5~乐观的一喜寿司","063.朝花夕拾16~跑步去打饭","062.与喵共舞34~春游菜地","061.与喵共舞33~春游动物园","060.与喵共舞32~爸爸还会再陪我会儿","059.人间3~西二旗的早上","058.与喵共舞31~0到1岁喵","057.朝花夕拾15——北京动物园","056.菜谱1——最偷懒的酱牛肉","055.朝花夕拾14~北京粮店","054.吃过什么4~还是牛腱子？","053.朝花夕拾13~记忆中的春游","052.与喵共舞30~发烧总是不期而遇","051.与喵共舞29~每天早上去幼儿园的一路","050.与喵共舞28~我当老师，你们当小兔子","049.吃过什么3~好吃又好看","048.人间2~急诊室的大夫","047.朝花夕拾12~还记得47年的事吗？","046.与喵共舞27~妈妈住院之后","045.人间1~急诊观察室的病人","044.人间1~急诊观察室的一周","043.与喵共舞25~翻脸不认人的胰液","042.与喵共舞24~狼、鳄鱼、金雕","041.吃过什么2~再来6个","040.与喵共舞23~这次该爸爸去小黑屋","039.与喵共舞22~2015年度总结","038.朝花夕拾11~爷爷奶奶家","037.与喵共舞21~摇滚？滚球球，哈哈哈哈哈哈...","036.与喵共舞20~“长大”这两个字看似简单","035.与喵共舞20~与绿色为友","034.与喵共舞19~两根秒针","033.与喵共舞16~熟悉的味道，新的","032.与喵共舞18~爸爸说话了","031.吃过什么1~来自花果山上的月亮饼","030.与喵共舞17~再玩儿十分钟","029.与喵共舞16~幼儿园之《人在旅途洒泪时》","028.朝花夕拾10~你也看过这本书啊？","027.与喵共舞15~喵的新生活","026.与喵共舞14~老奶奶出来啦","025.与喵共舞13~自己拉臭了","024.与喵共舞12~与喵的谈话录，那永恒的“排骨白菜”","023.朝花夕拾9~记忆中的第一个世界杯","022.与喵共舞11~自己尿尿了","021.与喵共舞10~钢琴可以弹一弹","020.朝花夕拾8~不想睡的午觉","019.与喵共舞9~小警犬","018.与喵共舞8~谁来捡？","017.朝花夕拾7~两代人相同的回答","016.与喵共舞7~喵的四大金刚","015.友人录1~云已散，龙行远","014.朝花夕拾6~亲密的“客气”","013.与喵共舞6~喵起床说明书","012.朝花夕拾5~记忆中和父母去过的电影院","011.与喵共舞5~喵的幼儿急疹护理问题总结","010.与喵共舞4~喵的幼儿急疹记录","009.看电影2~从课堂上开始了解《教父》","008.看电影1~和姐姐妹妹一起看指环王（魔戒）","007.与喵共舞3~喵与“你”的2013","006.朝花夕拾4~你要摆头","005.与喵共舞2~思无崖（喵的小屋）的变迁史","004.朝花夕拾3~午后的评书连播","003.与喵共舞1~遇见过去的自己","002.朝花夕拾2~父亲那难以望其项背的好胃口","001.朝花夕拾1~母亲那一如既往马虎的爱"]
title = ["760.朝花夕拾82~三源里"]

# url = ["https://www.jianshu.com/p/f060d8315c60","https://www.jianshu.com/p/f42c6c8e53ae","https://www.jianshu.com/p/908aa73919b9","https://www.jianshu.com/p/1da41c3e0e89","https://www.jianshu.com/p/212eb9ad84bf","https://www.jianshu.com/p/acb80937bc66","https://www.jianshu.com/p/5c5c7875d2d2","https://www.jianshu.com/p/bc5655005874","https://www.jianshu.com/p/0692bff353f6","https://www.jianshu.com/p/15d0c44406eb","https://www.jianshu.com/p/64a5e08f6dac","https://www.jianshu.com/p/2eba4c09a870","https://www.jianshu.com/p/10f1bd502009","https://www.jianshu.com/p/ae7b181744ee","https://www.jianshu.com/p/af8d422ea8e7","https://www.jianshu.com/p/432575502010","https://www.jianshu.com/p/6df8446a66f1","https://www.jianshu.com/p/d92ed4f15a2f","https://www.jianshu.com/p/0cd7d0807711","https://www.jianshu.com/p/87e0e0c8128c","https://www.jianshu.com/p/d688e92a9e06","https://www.jianshu.com/p/4a8000683611","https://www.jianshu.com/p/e1384252cb73","https://www.jianshu.com/p/5ec7c3022356","https://www.jianshu.com/p/4e97c7e07350","https://www.jianshu.com/p/60d16681cff4","https://www.jianshu.com/p/32c9f8840483","https://www.jianshu.com/p/22233afb176a","https://www.jianshu.com/p/d7057826cce3","https://www.jianshu.com/p/6720bc652bfd","https://www.jianshu.com/p/df543a678f78","https://www.jianshu.com/p/579bbb44ead9","https://www.jianshu.com/p/0fdbeacb6cd3","https://www.jianshu.com/p/01045b32e858","https://www.jianshu.com/p/c7ded455c32e","https://www.jianshu.com/p/f1297859b1e4","https://www.jianshu.com/p/dd35a56bbf82","https://www.jianshu.com/p/0c725853e7f4","https://www.jianshu.com/p/c422f02511e3","https://www.jianshu.com/p/c34591c95423","https://www.jianshu.com/p/1c8241994ed5","https://www.jianshu.com/p/f7c2c50ea015","https://www.jianshu.com/p/d7978e091f95","https://www.jianshu.com/p/a3de0bd2b5c4","https://www.jianshu.com/p/2ec8e52f46c8","https://www.jianshu.com/p/693d93337cb5","https://www.jianshu.com/p/cdd07b8237ab","https://www.jianshu.com/p/07c0ee434a8f","https://www.jianshu.com/p/3c63f6be8b7e","https://www.jianshu.com/p/489041e08471","https://www.jianshu.com/p/0e21da532163","https://www.jianshu.com/p/872620f626ad","https://www.jianshu.com/p/ea9c5e9d2750","https://www.jianshu.com/p/6c63c7f93bae","https://www.jianshu.com/p/0ee80a615ef4","https://www.jianshu.com/p/b11621eae0fd","https://www.jianshu.com/p/e1decaee76b6","https://www.jianshu.com/p/4912bfc039b5","https://www.jianshu.com/p/7b4d7b41536f","https://www.jianshu.com/p/19701ef68760","https://www.jianshu.com/p/465f7986b9a1","https://www.jianshu.com/p/51188489697e","https://www.jianshu.com/p/34f8758e188b","https://www.jianshu.com/p/cceb50106cd1","https://www.jianshu.com/p/372fb13a1656","https://www.jianshu.com/p/9b86c0b4926f","https://www.jianshu.com/p/24e23df3c17d","https://www.jianshu.com/p/cae99322ded1"]
url = ["https://www.jianshu.com/p/f060d8315c60"]

print(title)
print(url)

file_parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir) + os.path.sep)
file_parent_path = file_parent_path + os.path.sep + 'momiaojushi'

print(file_parent_path)

session = requests.session()

# print(len(title))
# print(len(url))

for i in range(0, len(url)):
   
    folder = init.fetch_url(file_parent_path, url[i])
    print(folder)













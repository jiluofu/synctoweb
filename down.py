#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from syncart import  init
import os
import requests
import re
from pyquery import PyQuery as pyq
import shutil

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'Host': 'www.jianshu.com',
    'Referer': 'https://www.jianshu.com/',
    'User-Agent': agent,
    'Cookie': 'UM_distinctid=15abf6020014ed-0cbf592aad2c5c-1d336f50-232800-15abf602002747; CNZZDATA1258679142=2085407508-1479623066-%7C1493240676; _gat=1; remember_user_token=W1s1MTAwMV0sIiQyYSQxMCRtc3JidDFZei90T2tvWWNkdXRNajV1IiwiMTQ5NDQ1NDg4OS45MTkyMDYxIl0%3D--c379df551f6d5d514dda483bcf3c6740539b68fc; _ga=GA1.2.1596808950.1479626705; _gid=GA1.2.16377653.1494454962; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1493331084,1493761829,1493761977; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1494454962; _session_id=djluY2dMQTcxNkhyeVBMcytYaGFvc2hSTnhlRWJBRC81TnRLakNCWjFscmZBMFNzandUUkY2N2t3WUNmdHJ3ZkpRUzhuRmZjcHY2WCt3Q0RpUDI2ZmQ3NC9nZVdMYTROVGVzNEtjUWhMMkNPMyszU0FHQnUzQ2FaL1lVYlFJY01URmpIK05OL3JvR3ZVMklxWTkxNXE2QzZ6eWc4VkpmVU1HOTNDRG9EeHdpRTFWdGNkbUVsUHQ4d3lXbDBDZHl0NmhMTmRzWGlQUW5EWDRXWTNqMFZVMG8ydWNZQzFhdTJaZXBaQW9paitPamtsNEExVFVGamFaelc0VTlyRm5FSWpsMWd2L2FhdGgwS2k0V0I5RVhMR3VqNGxNSnluQ08wekIyN1VrQlh2ajc1TUFKMGFyNGNDMjR6UFkyOE9FemFXbjMwY0YvTkFneFBVMDZFYjRkYU5FVVk3YzZ3M3pDTUxGa0NpdzdTb0lrMlQ2cGZFY0c5ZUc1d0JLYXppYllUUldaMTA2S1VPdkdMaHVzRW9YcW1Sd2xtSzZ6WnhKL2VyaUwyNllrTTNIST0tLWNUUVRNcm1UYlBvWDc3WFMxQXErWnc9PQ%3D%3D--18908551648588864676a18cd7025f8bd7e5b76c'

}
headers_img = {
    'Host': 'upload-images.jianshu.io',
    'Referer': 'http://www.jianshu.com/',
    'User-Agent': agent
}




title = ["127.看图说话10~手抓饭","126.与喵共舞65~端午宜家","125.与喵共舞64~端午奥运大道看灯","124.与喵共舞63~端午玩儿沙子","123.与喵共舞62~端午看蜗牛","122.与喵共舞61~端午和妹妹们一起","121.人间7~两家人的水果摊","120.朝花夕拾29~游泳在暑假","119.看图说话9~蹦床瞬间","118.与喵共舞60~逛超市、做冰棍","117.与喵共舞59~保养汽车、买裙子","116.读过什么1~奇怪的谜语书","115.与喵共舞58~幼儿园的同学们","114.与喵共舞57~六一儿童节","113.朝花夕拾28~第一次“走丢”","112.看图说话8~一年前和婷婷姐姐","111.与喵共舞56~和兜妹悦妹一起玩儿","110.与喵共舞55~去婷婷姐姐家","109.朝花夕拾27~游泳在地坛","108.与喵共舞54~幼儿园放学后","107.人间6~有意思的邻居","106.朝花夕拾26~游泳在一开始","105.看图说话7~一个人骑三轮车","104.与喵共舞53~周末土城探险","103.与喵共舞52~周末跳舞、秋千、饺子","102.朝花夕拾25~我的幼儿园生涯","101.与喵共舞51~早晨幼儿园操场","100.与喵共舞50~新舞蹈","099.朝花夕拾24~放学后，新华书店","098.看图说话6~抢玩具","097.与喵共舞49~爬“山”","096.与喵共舞48~去超市","095.与喵共舞47~幼儿园的早晨","094.朝花夕拾23~游泳在学前","093.与喵共舞46~开始帮厨","092.人间5~卖水果的夫妻店","091.看图说话5~马甸公园银杏","090.与喵共舞45~昨日重现","089.与喵共舞44~晒晒太阳","088.与喵共舞43~玩儿些什么","087.看电影3~头脑特工队","086.与喵共舞42~摔杯为号","085.看图说话4~地坛银杏","084.吃过什么7~哪里的炸酱面最香？","083.与喵共舞41~五一发烧在家","082.与喵共舞40~五一假期见闻","081.吃过什么6~隆福寺的灌肠","080.朝花夕拾22~放学后，向左走向右走","079.朝花夕拾21~听飞鱼秀练笔","078.与喵共舞39~再会小兔子","077.看图说话3~假如有3个孩子","076.与喵共舞38～周末晒太阳","075.与喵共舞37~说话算话","074.朝花夕拾20~和平里的和平鸽","073.人间4~西二旗城铁没有小摊了","072.朝花夕拾19~学校的阅览室","071.与喵共舞36~押解之旅","070.看图说话2~找到贝壳啦","069.朝花夕拾18~周五放学，客场还是主场","068.与喵共舞35～春游故宫","067.友人录2~大媒婆关婧","066.朝花夕拾17~合唱队","065.看图说话1~麦霸","064.吃过什么5~乐观的一喜寿司","063.朝花夕拾16~跑步去打饭","062.与喵共舞34~春游菜地","061.与喵共舞33~春游动物园","060.与喵共舞32~爸爸还会再陪我会儿","059.人间3~西二旗的早上","058.与喵共舞31~0到1岁喵","057.朝花夕拾15——北京动物园","056.菜谱1——最偷懒的酱牛肉","055.朝花夕拾14~北京粮店","054.吃过什么4~还是牛腱子？","053.朝花夕拾13~记忆中的春游","052.与喵共舞30~发烧总是不期而遇","051.与喵共舞29~每天早上去幼儿园的一路","050.与喵共舞28~我当老师，你们当小兔子","049.吃过什么3~好吃又好看","048.人间2~急诊室的大夫","047.朝花夕拾12~还记得47年的事吗？","046.与喵共舞27~妈妈住院之后","045.人间1~急诊观察室的病人","044.人间1~急诊观察室的一周","043.与喵共舞25~翻脸不认人的胰液","042.与喵共舞24~狼、鳄鱼、金雕","041.吃过什么2~再来6个","040.与喵共舞23~这次该爸爸去小黑屋","039.与喵共舞22~2015年度总结","038.朝花夕拾11~爷爷奶奶家","037.与喵共舞21~摇滚？滚球球，哈哈哈哈哈哈...","036.与喵共舞20~“长大”这两个字看似简单","035.与喵共舞20~与绿色为友","034.与喵共舞19~两根秒针","033.与喵共舞16~熟悉的味道，新的","032.与喵共舞18~爸爸说话了","031.吃过什么1~来自花果山上的月亮饼","030.与喵共舞17~再玩儿十分钟","029.与喵共舞16~幼儿园之《人在旅途洒泪时》","028.朝花夕拾10~你也看过这本书啊？","027.与喵共舞15~喵的新生活","026.与喵共舞14~老奶奶出来啦","025.与喵共舞13~自己拉臭了","024.与喵共舞12~与喵的谈话录，那永恒的“排骨白菜”","023.朝花夕拾9~记忆中的第一个世界杯","022.与喵共舞11~自己尿尿了","021.与喵共舞10~钢琴可以弹一弹","020.朝花夕拾8~不想睡的午觉","019.与喵共舞9~小警犬","018.与喵共舞8~谁来捡？","017.朝花夕拾7~两代人相同的回答","016.与喵共舞7~喵的四大金刚","015.友人录1~云已散，龙行远","014.朝花夕拾6~亲密的“客气”","013.与喵共舞6~喵起床说明书","012.朝花夕拾5~记忆中和父母去过的电影院","011.与喵共舞5~喵的幼儿急疹护理问题总结","010.与喵共舞4~喵的幼儿急疹记录","009.看电影2~从课堂上开始了解《教父》","008.看电影1~和姐姐妹妹一起看指环王（魔戒）","007.与喵共舞3~喵与“你”的2013","006.朝花夕拾4~你要摆头","005.与喵共舞2~思无崖（喵的小屋）的变迁史","004.朝花夕拾3~午后的评书连播","003.与喵共舞1~遇见过去的自己","002.朝花夕拾2~父亲那难以望其项背的好胃口","001.朝花夕拾1~母亲那一如既往马虎的爱"]
# title = ["760.朝花夕拾82~三源里"]

url = ["https://www.jianshu.com/p/c5ee54391e3b","https://www.jianshu.com/p/41db1ba59181","https://www.jianshu.com/p/32505274e84e","https://www.jianshu.com/p/15a517cc5bc2","https://www.jianshu.com/p/bc4e22878a04","https://www.jianshu.com/p/cf054bd28a7c","https://www.jianshu.com/p/4106772e20c3","https://www.jianshu.com/p/9d6ad02caf18","https://www.jianshu.com/p/b96f98dbdc5e","https://www.jianshu.com/p/a7fc125d8240","https://www.jianshu.com/p/86bf89e0dce0","https://www.jianshu.com/p/358937a9831e","https://www.jianshu.com/p/b5d084326d68","https://www.jianshu.com/p/c830b43e21a3","https://www.jianshu.com/p/756bd1e8cbc8","https://www.jianshu.com/p/bd19f3a8f176","https://www.jianshu.com/p/3261cc5b15cd","https://www.jianshu.com/p/f646b5426250","https://www.jianshu.com/p/42450aa9c566","https://www.jianshu.com/p/5bc03ae8b8a9","https://www.jianshu.com/p/8d9647c46355","https://www.jianshu.com/p/74236ada5d5a","https://www.jianshu.com/p/aa318c70804a","https://www.jianshu.com/p/27060ceee819","https://www.jianshu.com/p/53e501d554d3","https://www.jianshu.com/p/95e6e814d5e2","https://www.jianshu.com/p/da3bf92b1f37","https://www.jianshu.com/p/cd98684cbdf8","https://www.jianshu.com/p/43c18f0f78be","https://www.jianshu.com/p/0c786637e468","https://www.jianshu.com/p/d28f41bbc2ca","https://www.jianshu.com/p/38b9092c85c5","https://www.jianshu.com/p/398752bd6ac8","https://www.jianshu.com/p/c5cb5c36ead0","https://www.jianshu.com/p/d23e9288bba2","https://www.jianshu.com/p/762cd053b856","https://www.jianshu.com/p/bc3309177576","https://www.jianshu.com/p/56667f5cb8e2","https://www.jianshu.com/p/d035f9a45467","https://www.jianshu.com/p/d85f185dd919","https://www.jianshu.com/p/a5871d991ca4","https://www.jianshu.com/p/10b09298baba","https://www.jianshu.com/p/33dd0ee7cad3","https://www.jianshu.com/p/58a4abc56b9b","https://www.jianshu.com/p/c1ec69fc7853","https://www.jianshu.com/p/c4a39a19c300","https://www.jianshu.com/p/5df7ad61ba52","https://www.jianshu.com/p/f01b8363ec13","https://www.jianshu.com/p/e6660fe8f13e","https://www.jianshu.com/p/3188a3b45c69","https://www.jianshu.com/p/36f5e15c02dd","https://www.jianshu.com/p/b5bbf2cfcc30","https://www.jianshu.com/p/8a414ff7b00f","https://www.jianshu.com/p/2fcd19bdb653","https://www.jianshu.com/p/ca6ce19d3411","https://www.jianshu.com/p/08eb2377912f","https://www.jianshu.com/p/2d7b47670555","https://www.jianshu.com/p/a8e509adef72","https://www.jianshu.com/p/28d4434b15da","https://www.jianshu.com/p/f060d8315c60","https://www.jianshu.com/p/f42c6c8e53ae","https://www.jianshu.com/p/908aa73919b9","https://www.jianshu.com/p/1da41c3e0e89","https://www.jianshu.com/p/212eb9ad84bf","https://www.jianshu.com/p/acb80937bc66","https://www.jianshu.com/p/5c5c7875d2d2","https://www.jianshu.com/p/bc5655005874","https://www.jianshu.com/p/0692bff353f6","https://www.jianshu.com/p/15d0c44406eb","https://www.jianshu.com/p/64a5e08f6dac","https://www.jianshu.com/p/2eba4c09a870","https://www.jianshu.com/p/10f1bd502009","https://www.jianshu.com/p/ae7b181744ee","https://www.jianshu.com/p/af8d422ea8e7","https://www.jianshu.com/p/432575502010","https://www.jianshu.com/p/6df8446a66f1","https://www.jianshu.com/p/d92ed4f15a2f","https://www.jianshu.com/p/0cd7d0807711","https://www.jianshu.com/p/87e0e0c8128c","https://www.jianshu.com/p/d688e92a9e06","https://www.jianshu.com/p/4a8000683611","https://www.jianshu.com/p/e1384252cb73","https://www.jianshu.com/p/5ec7c3022356","https://www.jianshu.com/p/4e97c7e07350","https://www.jianshu.com/p/60d16681cff4","https://www.jianshu.com/p/32c9f8840483","https://www.jianshu.com/p/22233afb176a","https://www.jianshu.com/p/d7057826cce3","https://www.jianshu.com/p/6720bc652bfd","https://www.jianshu.com/p/df543a678f78","https://www.jianshu.com/p/579bbb44ead9","https://www.jianshu.com/p/0fdbeacb6cd3","https://www.jianshu.com/p/01045b32e858","https://www.jianshu.com/p/c7ded455c32e","https://www.jianshu.com/p/f1297859b1e4","https://www.jianshu.com/p/dd35a56bbf82","https://www.jianshu.com/p/0c725853e7f4","https://www.jianshu.com/p/c422f02511e3","https://www.jianshu.com/p/c34591c95423","https://www.jianshu.com/p/1c8241994ed5","https://www.jianshu.com/p/f7c2c50ea015","https://www.jianshu.com/p/d7978e091f95","https://www.jianshu.com/p/a3de0bd2b5c4","https://www.jianshu.com/p/2ec8e52f46c8","https://www.jianshu.com/p/693d93337cb5","https://www.jianshu.com/p/cdd07b8237ab","https://www.jianshu.com/p/07c0ee434a8f","https://www.jianshu.com/p/3c63f6be8b7e","https://www.jianshu.com/p/489041e08471","https://www.jianshu.com/p/0e21da532163","https://www.jianshu.com/p/872620f626ad","https://www.jianshu.com/p/ea9c5e9d2750","https://www.jianshu.com/p/6c63c7f93bae","https://www.jianshu.com/p/0ee80a615ef4","https://www.jianshu.com/p/b11621eae0fd","https://www.jianshu.com/p/e1decaee76b6","https://www.jianshu.com/p/4912bfc039b5","https://www.jianshu.com/p/7b4d7b41536f","https://www.jianshu.com/p/19701ef68760","https://www.jianshu.com/p/465f7986b9a1","https://www.jianshu.com/p/51188489697e","https://www.jianshu.com/p/34f8758e188b","https://www.jianshu.com/p/cceb50106cd1","https://www.jianshu.com/p/372fb13a1656","https://www.jianshu.com/p/9b86c0b4926f","https://www.jianshu.com/p/24e23df3c17d","https://www.jianshu.com/p/cae99322ded1"]
# url = ["https://www.jianshu.com/p/b83aa8bb3258"]

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













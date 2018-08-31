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




title = ["894.小学17~算术","893.读历史45~晋惠帝和阿甘","892.读书75~《刺杀骑士团长》下","891.与喵共舞435~银河护卫队","890.看图说话107~动物园里学英语","889.与喵共舞434~周末拍照","888.与喵共舞433~周末跳舞学琴","887.小学16~跑步","886.朝花夕拾92~教师教学参考书","885.读书74~《刺杀骑士团长》上","884.与喵共舞432~第一次养宠物","883.看图说话106~音羽瀑布","882.与喵共舞431~周末活动","881.与喵共舞430~周末活动","880.小学15~学跳绳","879.读历史44~大诰","878.读书73~《西游记3》完结","877.与喵共舞429~钢琴比赛的预演","876.看图说话105~教工食堂","875.与喵共舞428~周末活动","874.与喵共舞427~周末跳舞学琴","873.小学14~上学路","872.朝花夕拾91~世界杯决赛","871.读书72~《西游记2》","870.与喵共舞426~跳绳","869.看图说话104~钢琴课前","868.与喵共舞425~周末买桌子","867.与喵共舞424~周末玩儿水","866.小学13~回答问题","865.读历史43~九子夺嫡","864.读书71~《西游记1》","863.看图说话103~三亚沙滩","862.与喵共舞423~端午节","861.与喵共舞422~周末下大雨","860.与喵共舞421~周末看电影","859.小学12~吃午饭","858.朝花夕拾90~遇见外国人","857.读书70~《鲁迅生平大事年表》","856.与喵共舞420~练琴的大进步","855.看图说话102~小摄影师","854.与喵共舞419~周末在家","853.与喵共舞418~周末跳舞学琴","852.小学11~擦黑板","851.读历史42~杨朱的人人不损一毫","850.读书69~《鲁迅杂文精选》","849.与喵共舞417~正义联盟的英雄","848.看图说话101~百望山碑林","847.与喵共舞416~周末去商场","846.与喵共舞415~周末跳舞学琴奥林匹克","845.小学10~课间喝水","844.朝花夕拾89~早点馄炖","843.读书68~《1368个单词就够了》","842.与喵共舞414~幼儿园早上","841.看图说话100~五线谱","840.与喵共舞413~周末聚会","839.与喵共舞412~周末跳舞学琴","838.小学9~放学啦","837.读历史41~浔阳江","836.读书67~《朝花夕拾》","835.与喵共舞411~玩儿摇摆球","834.看图说话99~悬浮球","833.与喵共舞410~周末家乐福","832.与喵共舞409~周末团建","831.小学8~写作业","830.朝花夕拾88~郊游","829.读书66~《独领风骚：毛泽东心路解读》","828.与喵共舞408~打拳","827.看图说话98~玩积木","826.与喵共舞407~周末钢琴沙龙","825.与喵共舞406~周末跳舞学琴","824.小学7~体育课","823.读历史40~陈渠珍","822.读书65~《乌合之众》","821.与喵共舞405~《彼得兔》","820.看图说话97~超市买糖","819.与喵共舞404~周末奥森","818.与喵共舞403~周末跳舞学琴聚会","817.小学6~美术课","816.朝花夕拾87~红霞电影院","815.读书64~《闪击英雄》","814.与喵共舞402~三联书店三里屯店","813.与喵共舞401~五一聚会","812.与喵共舞400~周末散步","811.与喵共舞399~周末跳舞学琴","810.小学5~音乐课","809.读历史39~荆轲刺秦时卫士们呢？","808.读书63~《呐喊》","807.与喵共舞398~神奇女侠","806.看图说话96~冲浪板","805.与喵共舞397~周末雨中登长城","804.与喵共舞396~周末去长城","803.小学4~第一次见同学","802.朝花夕拾86~去昌平","801.读书62~《连城诀》","800.与喵共舞395~练琴每天要多久？","799.看图说话95~摘苹果","798.与喵共舞394~周末晒太阳","797.与喵共舞393~周末跳舞学琴","796.小学3~第一位老师","795.读历史38~杨振宁和生活大爆炸","794.读书61~《一本书读懂日本历史》","793.与喵共舞392~做噩梦","792.看图说话94~中央电视塔观玉渊潭","791.与喵共舞391~周末倒休上班","790.与喵共舞390~周末活动","789.与喵共舞389~清明聚会","788.朝花夕拾85~玉渊潭赏樱","787.读书60~《一句顶一万句》","786.与喵共舞388~双手配合的难度来了","785.看图说话93~幼儿园秋千","784.与喵共舞387~周末去商场","783.与喵共舞386~周末跳舞学琴","782.小学2~第一次进校园","781.读历史37~开尔文爵士","780.读书59~《什么是数学：对思想和方法的基本研究》","779.与喵共舞385~练琴的抱怨","778.看图说话92~爬小山","777.与喵共舞384~周末扫墓","776.与喵共舞383~周末跳舞学琴","775.小学1~学前班","774.朝花夕拾84~春节庙会","773.读书58~《丘吉尔第二次世纪大战回忆录1——从战争到战争》下","772.与喵共舞382~忘带书包","771.看图说话91~小店","770.与喵共舞381~周末生日聚会","769.与喵共舞380~生日跳舞学琴","768.拍照片65~聚会","767.读历史36~驸马升格","766.读书57~《丘吉尔第二次世纪大战回忆录1——从战争到战争》上","765.与喵共舞379~和同学的谈话","764.看图说话90~做手链","763.与喵共舞379~周末去超市","762.朝花夕拾83~送大爷爷","761.拍照片64~和婷婷姐姐、胖虎弟弟聚会"]
# title = ["760.朝花夕拾82~三源里"]

url = ["https://www.jianshu.com/p/021195146e1d","https://www.jianshu.com/p/3b548711df37","https://www.jianshu.com/p/c1d1ddabc2bf","https://www.jianshu.com/p/ab5fcb6a70dc","https://www.jianshu.com/p/feb782aceb70","https://www.jianshu.com/p/9930931c0c0c","https://www.jianshu.com/p/f823692bf59c","https://www.jianshu.com/p/46bc22246ee7","https://www.jianshu.com/p/459f57b803c4","https://www.jianshu.com/p/c76d00d8c1ef","https://www.jianshu.com/p/34c7091a41d8","https://www.jianshu.com/p/71606de69cbf","https://www.jianshu.com/p/fcfe8040e176","https://www.jianshu.com/p/e599e02c3a95","https://www.jianshu.com/p/fe403873566e","https://www.jianshu.com/p/0f25d193127e","https://www.jianshu.com/p/f68c536b5da9","https://www.jianshu.com/p/c8bf278f92cf","https://www.jianshu.com/p/5b08604fa9bc","https://www.jianshu.com/p/4f8ff23b3304","https://www.jianshu.com/p/ef8501b2d57e","https://www.jianshu.com/p/36c31088ffa6","https://www.jianshu.com/p/52662fcc597e","https://www.jianshu.com/p/cfefffe90b4d","https://www.jianshu.com/p/46fa2519c707","https://www.jianshu.com/p/b7b72fcf27fc","https://www.jianshu.com/p/4e904935c4c5","https://www.jianshu.com/p/d147caa65a56","https://www.jianshu.com/p/b24448ec0447","https://www.jianshu.com/p/2fcac0b95355","https://www.jianshu.com/p/91e00ffd7b83","https://www.jianshu.com/p/f9feab474062","https://www.jianshu.com/p/61751b9d6871","https://www.jianshu.com/p/e5b032eea87c","https://www.jianshu.com/p/1dc1f8e787ca","https://www.jianshu.com/p/5191277ba287","https://www.jianshu.com/p/005ac90cf12a","https://www.jianshu.com/p/b8e3fe6332f0","https://www.jianshu.com/p/3f208e11bb57","https://www.jianshu.com/p/9a50e7e725e0","https://www.jianshu.com/p/8514dd0e3bd0","https://www.jianshu.com/p/cb81f9c845ac","https://www.jianshu.com/p/05f176863eb2","https://www.jianshu.com/p/57f2ba8811ae","https://www.jianshu.com/p/03c681936a47","https://www.jianshu.com/p/9e2201f3d470","https://www.jianshu.com/p/024653f2ab11","https://www.jianshu.com/p/8aebedc54ffe","https://www.jianshu.com/p/a549f1e4df07","https://www.jianshu.com/p/a61be9a51d9d","https://www.jianshu.com/p/f4f7ccb9483e","https://www.jianshu.com/p/f22ffb1f966f","https://www.jianshu.com/p/2f48fce36777","https://www.jianshu.com/p/283aecbc77f1","https://www.jianshu.com/p/239cf9f68d77","https://www.jianshu.com/p/7beca81314eb","https://www.jianshu.com/p/40148b6ff2e4","https://www.jianshu.com/p/a58676771167","https://www.jianshu.com/p/26e2facee9c9","https://www.jianshu.com/p/915e3f21d1f8","https://www.jianshu.com/p/6907eed4075e","https://www.jianshu.com/p/3b5971509812","https://www.jianshu.com/p/982308159b46","https://www.jianshu.com/p/857d7311bc71","https://www.jianshu.com/p/c387ab45ed71","https://www.jianshu.com/p/577dac5604f2","https://www.jianshu.com/p/a4ea2f4bd541","https://www.jianshu.com/p/1a7e3bf63608","https://www.jianshu.com/p/5a78827ac506","https://www.jianshu.com/p/91642eccd44f","https://www.jianshu.com/p/ee4c5a27f6f3","https://www.jianshu.com/p/a28895482409","https://www.jianshu.com/p/0dfaf11cd864","https://www.jianshu.com/p/4367839101d2","https://www.jianshu.com/p/17ce00fadce0","https://www.jianshu.com/p/24da7f961257","https://www.jianshu.com/p/81328a0df2f1","https://www.jianshu.com/p/8183e7144721","https://www.jianshu.com/p/3f1fd315593a","https://www.jianshu.com/p/24a81034d294","https://www.jianshu.com/p/7efdcba7cd50","https://www.jianshu.com/p/1f5e891cae94","https://www.jianshu.com/p/695164b0d8fb","https://www.jianshu.com/p/363fec112c1a","https://www.jianshu.com/p/275acc0d68e7","https://www.jianshu.com/p/cb10fe1bc8cf","https://www.jianshu.com/p/02e8c1f9634e","https://www.jianshu.com/p/63195d31e2f5","https://www.jianshu.com/p/c68b0920a821","https://www.jianshu.com/p/adfaede4fa1a","https://www.jianshu.com/p/4ddcf3af27ff","https://www.jianshu.com/p/1e277aada596","https://www.jianshu.com/p/14cd6acce3ee","https://www.jianshu.com/p/d9159d55da97","https://www.jianshu.com/p/83ab9469fa71","https://www.jianshu.com/p/5b405f53bc67","https://www.jianshu.com/p/e53b34bfa2b0","https://www.jianshu.com/p/39cdfc0b060c","https://www.jianshu.com/p/daca92fe1605","https://www.jianshu.com/p/da0aefde15f9","https://www.jianshu.com/p/e226e0687ebc","https://www.jianshu.com/p/ec136e706a72","https://www.jianshu.com/p/2ac478bfb7e1","https://www.jianshu.com/p/10bf0b877c9c","https://www.jianshu.com/p/4cb540038d21","https://www.jianshu.com/p/a6b6b0a2c379","https://www.jianshu.com/p/8a1935966f28","https://www.jianshu.com/p/2f368d405242","https://www.jianshu.com/p/7b33588cbb3e","https://www.jianshu.com/p/049b5aacefa2","https://www.jianshu.com/p/a8468bd1fbce","https://www.jianshu.com/p/08ef0aa4a1d3","https://www.jianshu.com/p/66e2196a689f","https://www.jianshu.com/p/87954dc28a26","https://www.jianshu.com/p/f18fc172565e","https://www.jianshu.com/p/1162ca416982","https://www.jianshu.com/p/31ffaba5b58c","https://www.jianshu.com/p/f7eb1160a0c9","https://www.jianshu.com/p/2621e77897af","https://www.jianshu.com/p/1216c016eb27","https://www.jianshu.com/p/06ab9c145b45","https://www.jianshu.com/p/c3a6fc89411d","https://www.jianshu.com/p/d340f803bcc5","https://www.jianshu.com/p/235197e640b2","https://www.jianshu.com/p/677073d4cfa9","https://www.jianshu.com/p/42b700fc83e0","https://www.jianshu.com/p/26791a5a8059","https://www.jianshu.com/p/a2707fab2996","https://www.jianshu.com/p/28ad9e32c3cc","https://www.jianshu.com/p/a8d19b8e7ff9","https://www.jianshu.com/p/7aa287622c08","https://www.jianshu.com/p/5f5c94b7cec5","https://www.jianshu.com/p/cb64b9d9006f","https://www.jianshu.com/p/6a8dd488b68f"]
# url = ["https://www.jianshu.com/p/f060d8315c60"]

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













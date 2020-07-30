#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
Info
- author : "zhuxu"
- email  : "zhu.xu@qq.com"
- date   : "2016.11.11"
Update
'''
import time
import base64
import rsa
import binascii
import requests
import re
import random
try:
    from PIL import Image
except:
    pass
try:
    from urllib.parse import quote_plus
except:
    from urllib import quote_plus

import sys
import os
from syncart import init
import json
import string
import configparser
from selenium import webdriver

conf_path = '/Users/zhuxu/Documents/mmjstool/synctoweb/syncart/sync.conf'
chromedriver_path = '/Users/zhuxu/Documents/mmjstool/synctoweb/chromedriver'

'''
如果没有开启登录保护，不用输入验证码就可以登录
如果开启登录保护，需要输入验证码
'''

cf = configparser.RawConfigParser()
cf.read(os.path.dirname(__file__) + os.path.sep + 'sync.conf')
username = cf.get('weibo', 'username')
password = cf.get('weibo', 'password')
cookie = cf.get('weibo', 'cookie')

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': agent
}


def initial():

    print('init weibo')
    try:
        if checkLogin() != True:
            cookie = getCookie();
    except Exception as e:
        
        cookie = getCookie();

def checkLogin():

    # url = 'http://login.sina.com.cn/signup/signin.php'
    url = 'https://weibo.com/jiluofu/home?wvr=5'
    headers_weibo = {

        'Host': 'www.weibo.com',
        # 'Host': 'login.sina.com.cn',
        # 'Origin': 'https://www.weibo.com',
        # 'Referer': 'https://www.weibo.com',
        'User-Agent': agent,
        # 'Content-Type': 'text/html;charset=UTF-8',
        'Cookie': cf.get('weibo', 'cookie')

    }



    # 通过get_url，使得session获得专栏的cookie，里面有X-XSRF-TOKEN
    login_page = session.get(url, headers=headers_weibo, allow_redirects=False);
    print(login_page)
    
    pattern = r'摹喵居士'
    res = re.findall(pattern, login_page.text)
    if len(res) > 0:
        print('weibo cookie is ok.')
        return True;
    else:
        return False;


def getCookie():

    url = 'https://www.weibo.com'
    driver = webdriver.Chrome(chromedriver_path)
    driver.get(url)
    # time.sleep(5)
    # # print(username)
    # driver.find_element_by_id('username').send_keys(username)
    # driver.find_element_by_id('password').send_keys(password)

    input('去手动登录吧\n>  ')
    # 网页源码
    # page = driver.page_source
    # print(page)

    cookies = driver.get_cookies()
    cookies_str = ''
    for item in cookies:
        cookies_str += item['name'] + '=' + item['value'] + ';'
    cf.set('weibo', 'cookie', cookies_str)
    fp = open(conf_path, 'w')
    cf.write(fp)
    fp.close()
    cf.read(conf_path)



    # 关闭浏览器
    driver.close()

    return cookies_str

session = requests.session()

# 访问 初始页面带上 cookie
index_url = "http://weibo.com/login.php"
try:
    session.get(index_url, headers=headers, timeout=2)
except:
    session.get(index_url, headers=headers)
try:
    input = raw_input
except:
    pass


def get_su(username):
    """
    对 email 地址和手机号码 先 javascript 中 encodeURIComponent
    对应 Python 3 中的是 urllib.parse.quote_plus
    然后在 base64 加密后decode
    """
    username_quote = quote_plus(username)
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")


# 预登陆获得 servertime, nonce, pubkey, rsakv
def get_server_data(su):
    pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
    pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
    pre_url = pre_url + str(int(time.time() * 1000))
    pre_data_res = session.get(pre_url, headers=headers)

    sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))

    return sever_data


# print(sever_data)


def get_password(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
    message = message.encode("utf-8")
    passwd = rsa.encrypt(message, key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
    return passwd


def get_cha(pcid):
    cha_url = "http://login.sina.com.cn/cgi/pin.php?r="
    cha_url = cha_url + str(int(random.random() * 100000000)) + "&s=0&p="
    cha_url = cha_url + pcid
    cha_page = session.get(cha_url, headers=headers)
    with open("cha.jpg", 'wb') as f:
        f.write(cha_page.content)
        f.close()
    try:
        im = Image.open("cha.jpg")
        im.show()
        im.close()
    except:
        print(u"请到当前目录下，找到验证码后输入")


def login(username, password):
    # su 是加密后的用户名
    su = get_su(username)
    sever_data = get_server_data(su)
    servertime = sever_data["servertime"]
    nonce = sever_data['nonce']
    rsakv = sever_data["rsakv"]
    pubkey = sever_data["pubkey"]
    showpin = sever_data["showpin"]
    password_secret = get_password(password, servertime, nonce, pubkey)

    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'useticket': '1',
        'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
        'vsnf': '1',
        'su': su,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': password_secret,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
        }
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    if showpin == 0:
        login_page = session.post(login_url, data=postdata, headers=headers)
    else:
        pcid = sever_data["pcid"]
        get_cha(pcid)
        postdata['door'] = input(u"请输入验证码")
        login_page = session.post(login_url, data=postdata, headers=headers)
    login_loop = (login_page.content.decode("GBK"))
    # print(login_loop)
    pa = r'location\.replace\([\'"](.*?)[\'"]\)'
    loop_url = re.findall(pa, login_loop)[0]
    print(loop_url)
    # 此出还可以加上一个是否登录成功的判断，下次改进的时候写上
    login_index = session.get(loop_url, headers=headers)
    uuid = login_index.text
    uuid_pa = r'"uniqueid":"(.*?)"'
    uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
    web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
    weibo_page = session.get(web_weibo_url, headers=headers)
    weibo_pa = r'<title>(.*?)</title>'
    # print(weibo_page.content.decode("utf-8"))
    userID = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
    print(u"欢迎你 %s, 你在正在使用 xchaoinfo 写的模拟登录微博" % userID)


def upload_img(img_file):

    headers_pic = {

        'Origin': 'https://card.weibo.com',
        'Referer': 'https://card.weibo.com/article/v3/editor',
        'User-Agent': agent,
        # 'Cookie': cf.get('weibo', 'cookie')
    }

    post_url = 'https://picupload.weibo.com/interface/pic_upload.php?mime=image%2Fjpeg&marks=1&app=miniblog&url=0&markpos=1&logo=&nick='


    files = {

        'pic1': open(img_file, 'rb')
    }

    login_page = session.post(post_url, files=files, headers=headers_pic, allow_redirects=False);
    print(login_page.text)
    pattern = r'"pid":"(.*?)"'
    pid = re.findall(pattern, login_page.text)[0]
    img_new_url = 'https://wx3.sinaimg.cn/large/' + pid + '.jpg'

    return img_new_url



def get_img_file_new_url(file_parent_path, folder):

    file_pre = file_parent_path + os.path.sep + folder + os.path.sep

    img_file_new_url = {}
    img_files = init.listdir(file_pre + 'img')
    for i in range(0, len(img_files)):
        img_file_path = file_pre + 'img' + os.path.sep + img_files[i]
        img_file_new_url[img_files[i]] = upload_img(img_file_path)
        print(img_file_new_url[img_files[i]])

    # print(img_file_new_url)
    return img_file_new_url

def pub(file_parent_path, folder):

    login(username, password)
    # initial()

    img_file_new_url = get_img_file_new_url(file_parent_path, folder)
    init.get_folder_imgs(file_parent_path, folder, img_file_new_url, 'weibo')

    title = re.sub(r'_[^_]*_', '.', folder)

    file_pre = file_parent_path + os.path.sep + folder + os.path.sep
    file_html_path = file_pre + 'index_weibo.html'

    # 读取index.md
    index_html_file = open(file_html_path, 'r', encoding='utf-8')
    file_html_content = index_html_file.read()
    index_html_file.close()

    print(init.cover)
    weibo_cover_url = upload_img(init.cover['file_path'])



    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

    headers_art = {

        'Host': 'www.weibo.com',
        'Referer': 'https://card.weibo.com/article/v3/editor',
        'User-Agent': agent,
        'Origin': 'https://card.weibo.com',
        'Content-Type': 'application/x-www-form-urlencoded;',
        # 'Cookie': cf.get('weibo', 'cookie')
    }

    data = {

        'title': title,
        'cover': weibo_cover_url,
        'content': file_html_content,
        'type': 'draft'
    }

    print(data['content'])

    # post_url = 'https://www.weibo.com/ttarticle/p/aj/draft?ajwvr=6'
    post_url = 'https://card.weibo.com/article/v3/aj/editor/draft/create'
    login_page = session.post(post_url, data=data, headers=headers_art)

    print(data)
    # print(login_page.text)
    res = json.loads(login_page.text)
    print(res['msg'])
    
    pub_id = res['data']['id']
    print('###pub_id:' + pub_id)

    # setpayinfo
    data = {

        'id': pub_id,
        'pay_setting': '{"pid":"38001557","isreward":1,"isvclub":0,"ispay":0}'

    }
    post_url = 'https://card.weibo.com/article/v3/aj/editor/settings/setpayinfo'
    # login_page = session.post(post_url, data=data, headers=headers_art)
    # res = json.loads(login_page.text)
    # print(res)

    data = {

        'id': pub_id,
        'title': title,
        'status': 0,
        'isvclub': 0,
        # 'ispay': 0,
        'error_code': 0,
        'cover': weibo_cover_url,
        'content': file_html_content,
        'is_word': 0,
        'pay_setting':{"ispay":1, "isvclub":0},
        'save': 1,
        'isreward': 1,
        'content_type': 0
        
    }

    # post_url = 'https://www.weibo.com/ttarticle/p/aj/draft?ajwvr=6'
    post_url = 'https://card.weibo.com/article/v3/aj/editor/draft/save'
    login_page = session.post(post_url, data=data, headers=headers_art)

    print(data)
    # print(login_page.text)
    res = json.loads(login_page.text)
    print(res)
    time.sleep(2)
    # 发布
    data = {

        'id': pub_id,
        'text': '发布了头条文章：《' + title + '》',
        'follow_to_read': 1,
        'follow_official': 0,
        'sync_wb': 0,
        'is_original': 0
    }
    post_url = 'https://card.weibo.com/article/v3/aj/editor/draft/publish'
    login_page = session.post(post_url, data=data, headers=headers_art)
    res = json.loads(login_page.text)
    print(res)





#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
- pillow (可选)
Info
- author : "zhuxu"
- email  : "zhu.xu@qq.com"
- date   : "2016.11.11"
Update

'''
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
try:
    from PIL import Image
except:
    pass

from syncart import init
import json
import string
import configparser
from selenium import webdriver

cf = configparser.RawConfigParser()
cf.read(os.path.dirname(__file__) + os.path.sep + 'sync.conf')
username = cf.get('zhihu', 'username')
password = cf.get('zhihu', 'password')
cookie = cf.get('zhihu', 'cookie')

cfTag = configparser.RawConfigParser()
cfTag.read(os.path.dirname(__file__) + os.path.sep + 'tag.conf')

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()

conf_path = '/Users/zhuxu/Documents/mmjstool/synctoweb/syncart/sync.conf'
chromedriver_path = '/Users/zhuxu/Documents/mmjstool/chromedriver'


def initial():

    print('init zhihu')
    try:
        if checkLogin() != True:
            cookie = getCookie();
    except Exception as e:
        
        cookie = getCookie();


def checkLogin():

    
    url = 'https://zhuanlan.zhihu.com'
    headers_zhuanlan = {

        'Host': 'zhuanlan.zhihu.com',
        'Origin': 'https://zhuanlan.zhihu.com',
        'Referer': 'https://www.zhihu.com',
        'User-Agent': agent,
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': cookie

    }



    # 通过get_url，使得session获得专栏的cookie，里面有X-XSRF-TOKEN
    login_page = session.get(url, headers=headers_zhuanlan, allow_redirects=False);
    

    pattern = r'摹喵居士'
    res = re.findall(pattern, login_page.text)
    if len(res) > 0:
        return True;
    else:
        return False;

def getCookie():

        url = 'https://www.zhihu.com/signup'
        driver = webdriver.Chrome(chromedriver_path)
        driver.get(url)
        time.sleep(10)
        # print(username)
        # driver.find_element_by_name('username').send_keys(username)
        # driver.find_element_by_name('password').send_keys(password)

        input('去手动登录吧\n>  ')
        # 网页源码
        page = driver.page_source
        # print(page)

        pattern = r'(摹喵居士)'
        res = re.findall(pattern, page)
        print(res)

        cookies = driver.get_cookies()
        cookies_str = ''
        for item in cookies:
            cookies_str += item['name'] + '=' + item['value'] + ';'
        cf.set('zhihu', 'cookie', cookies_str)
        fp = open(conf_path, 'w')
        cf.write(fp)
        fp.close()
        cf.read(conf_path)



        # 关闭浏览器
        driver.close()

        return cookies_str

def upload_img(img_file_path):

    # 构造要发布的图片文件
    files = {'picture': open(img_file_path, 'rb')}
    data = {'source': 'article'}
    post_url = 'https://zhuanlan.zhihu.com/api/uploaded_images'
    headers_zhuanlan = {
        "Host": "zhuanlan.zhihu.com",
        "Origin": "https://zhuanlan.zhihu.com",
        "Referer": "https://zhuanlan.zhihu.com/write",
        'User-Agent': agent,
        'X-XSRF-TOKEN': '',
        'Content-Type': '*/*',
        'Cookie':cf.get('zhihu', 'cookie')
    
    }

    get_url = 'https://zhuanlan.zhihu.com/api/me'

    # 通过get_url，使得session获得专栏的cookie，里面有X-XSRF-TOKEN
    login_page = session.get(get_url, headers=headers_zhuanlan, allow_redirects=False);
    print(login_page.text)

    # session.cookies.save()

    # 读取cookie中的XSRF-TOKEN存入headers_专栏里的X-XSRF-TOKEN
    headers_zhuanlan['X-XSRF-TOKEN'] = requests.utils.dict_from_cookiejar(session.cookies)['XSRF-TOKEN']
    # post图片文件
    login_page = session.post(post_url, data=files, files=files, headers=headers_zhuanlan);
    print(login_page)
    print(headers_zhuanlan)
    print(22)
    login_code = eval(login_page.text)
    print(login_code)
    print(11)

    # 打印生成的图片url

    return login_code['src']

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

    initial()

    img_file_new_url = get_img_file_new_url(file_parent_path, folder)
    init.get_folder_imgs(file_parent_path, folder, img_file_new_url, 'zhihu')

    title = re.sub(r'_[^_]*_', '.', folder)

    file_pre = file_parent_path + os.path.sep + folder + os.path.sep
    file_html_path = file_pre + 'index_zhihu.html'

    # 读取index.md
    index_html_file = open(file_html_path, 'r', encoding='utf-8')
    file_html_content = index_html_file.read()
    index_html_file.close()

    post_url = 'https://zhuanlan.zhihu.com/api/drafts'
    headers_zhuanlan = {

        'Host': 'zhuanlan.zhihu.com',
        'Origin': 'https://zhuanlan.zhihu.com',
        'Referer': 'https://zhuanlan.zhihu.com/write',
        'User-Agent': agent,
        'X-XSRF-TOKEN': '',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': cf.get('zhihu', 'cookie')

    }

    # get_url = 'https://zhuanlan.zhihu.com/write'

    # # 通过get_url，使得session获得专栏的cookie，里面有X-XSRF-TOKEN
    # login_page = session.get(get_url, headers=headers_zhuanlan, allow_redirects=False);
    # print(login_page.text)

    get_url = 'https://zhuanlan.zhihu.com/api/me'

    # 通过get_url，使得session获得专栏的cookie，里面有X-XSRF-TOKEN
    login_page = session.get(get_url, headers=headers_zhuanlan, allow_redirects=False);
    # session.cookies.save()

    # 读取cookie中的XSRF-TOKEN存入headers_专栏里的X-XSRF-TOKEN
    headers_zhuanlan['X-XSRF-TOKEN'] = requests.utils.dict_from_cookiejar(session.cookies)['XSRF-TOKEN']
    print(headers_zhuanlan['X-XSRF-TOKEN'])
    print(init.cover)
    zhihu_cover_url = upload_img(init.cover['file_path'])
    data = {

        'topics': [],
        'title': title,
        'content': file_html_content,
        'titleImage': zhihu_cover_url,
        'column': '',
        'isTitleImageFullScreen': False

    }

    data_str = json.dumps(data)



    print(post_url)
    # print(data)
    login_page = session.post(post_url, data=data_str, headers=headers_zhuanlan);
    # session.cookies.save()

    # 知乎草稿返回结果403时，网页登录发文章页面，把cookie写入header_zhuanlan即可
    print(login_page)
    res = json.loads(login_page.text)
    pub_id = res['id']

    tagDic = {

        '人文': '20165532',
        '儿童': '19551506',
        '阅读': '19550564',
        '钢琴': '19551861',
        '回忆': '19556732',
        '历史': '19551077',
    }
    tagArr = init.getTags(cfTag.get('zhihu', 'tag'))
    for i in range(0, len(tagArr)):
        tag = tagDic[tagArr[i]]
        post_url = 'https://zhuanlan.zhihu.com/api/posts/' + str(pub_id) + '/topics'
        data = {

            'id': tag,
            'name': tagArr[i]
        }
        data_str = json.dumps(data)

        login_page = session.post(post_url, data=data_str, headers=headers_zhuanlan);
        res = json.loads(login_page.text)
        print(res)

    

    post_url = 'https://zhuanlan.zhihu.com/api/drafts/' + str(pub_id) + '/publish'
    data = {

        'author': {

            'bio':"学做父亲，个人微信公号：momiaojushi",
            'description':"开始练笔。",
            'hash':"152d5c51b3a7976e07f4404945c85238",
            'isBanned':False,
            'isFollowed':False,
            'isFollowing':False,
            'isOrg':False,
            'isOrgWhiteList':False,
            'name':"摹喵居士",
            'profileUrl':"https://www.zhihu.com/people/jiluofu",
            'slug':"jiluofu",
            'uid':26886444941312
        },
        'column': {

            'name': '摹喵居士',
            'slug': 'momiaojushi',
            'url': '/momiaojushi',
            'avatar': {

                'id': 'v2-c8a50c3ddd68ad1266ce49061048b68c',
                'template': 'https://pic1.zhimg.com/{id}_{size}.jpg'
            }
        },
        'commentPermission': 'anyone',
        'id': '20165532',
        'isTitleImageFullScreen': False,
        'sourceUrl': '',
        'state': 'draft',
        'title': title,
        'titleImage': zhihu_cover_url,
        'updatedTime': ''

    }
    data_str = json.dumps(data)

    login_page = session.put(post_url, data=data_str, headers=headers_zhuanlan);
    res = json.loads(login_page.text)
    print(login_page)



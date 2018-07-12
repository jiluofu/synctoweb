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
username = cf.get('douban', 'username')
password = cf.get('douban', 'password')
cookie = cf.get('douban', 'cookie')

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'Host': 'www.douban.com',
    'Referer': 'https://www.douban.com/',
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()

conf_path = '/Users/zhuxu/Documents/mmjstool/synctoweb/syncart/sync.conf'
chromedriver_path = '/Users/zhuxu/Documents/mmjstool/chromedriver'

# global global_note_id
# global global_upload_auth_token
# global global_img_file_new_url

def initial():

    print('init douban')
    try:
        if checkLogin() != True:
            cookie = getCookie();
    except Exception as e:
        
        cookie = getCookie();


def checkLogin():

    
    url = 'https://www.douban.com'
    headers_douban = {

        'Host': 'www.douban.com',
        'Origin': 'https://www.douban.com',
        'Referer': 'https://www.douban.com',
        'User-Agent': agent,
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': cookie

    }



    # 通过get_url，使得session获得专栏的cookie，里面有X-XSRF-TOKEN
    login_page = session.get(url, headers=headers_douban, allow_redirects=False);
    

    pattern = r'摹喵居士'
    res = re.findall(pattern, login_page.text)
    if len(res) > 0:
        print('douban cookie is ok.')
        return True;
    else:
        return False;

def getCookie():

        url = 'https://www.douban.com/'
        driver = webdriver.Chrome(chromedriver_path)
        driver.get(url)
        time.sleep(5)
        # print(username)
        driver.find_element_by_id('form_email').send_keys(username)
        driver.find_element_by_id('form_password').send_keys(password)

        input('去手动登录吧\n>  ')
        # 网页源码
        page = driver.page_source
        # print(page)

        pattern = r'(摹喵居士)'
        res = re.findall(pattern, page)
        # print(res)

        cookies = driver.get_cookies()
        cookies_str = ''
        for item in cookies:
            cookies_str += item['name'] + '=' + item['value'] + ';'
        cf.set('douban', 'cookie', cookies_str)
        fp = open(conf_path, 'w')
        cf.write(fp)
        fp.close()
        cf.read(conf_path)



        # 关闭浏览器
        driver.close()

        return cookies_str

def get_upload_img_data():

    headers_douban = {
        "Host": "www.douban.com",
        "Referer": "https://www.douban.com",
        'User-Agent': agent,
        'Origin': 'https://www.douban.com',
        'Cookie':cf.get('douban', 'cookie')
    }

    get_url = 'https://www.douban.com/note/create'
    login_page = session.get(get_url, headers=headers_douban);
    
    pattern = r'_NOTE_ID = \'(.*?)\';'
    res = re.findall(pattern, login_page.text)[0]
    data = {}
    data['note_id'] = res
    pattern = r'_POST_PARAMS = {([^;]*)};'
    res = re.findall(pattern, login_page.text)[0]
    pattern = r'value: \'(.*?)\''
    res = re.findall(pattern, login_page.text)[0]
    data['upload_auth_token'] = res
    return data


def upload_img(img_file_path):

    # 构造要发布的图片文件
    files = {

        'image_file': open(img_file_path, 'rb')
    }

    html_data = get_upload_img_data()
    global global_note_id 
    global_note_id = html_data['note_id']
    global global_upload_auth_token
    global_upload_auth_token = html_data['upload_auth_token']

    data = {

        'ck': 'cHzd',
        'note_id': global_note_id,
        'folder': '/note/',
        'upload_auth_token': global_upload_auth_token
    }
    post_url = 'https://www.douban.com/j/note/add_photo'
    headers_douban = {
        "Host": "www.douban.com",
        "Referer": "https://www.douban.com/note/create",
        'User-Agent': agent,
        'Origin': 'https://www.douban.com',
        'Cookie':cf.get('douban', 'cookie')
    }

    

    # 通过get_url，使得session获得专栏的cookie，里面有X-XSRF-TOKEN
    # login_page = session.get(get_url, headers=headers_douban, allow_redirects=False);
    # print(login_page.text)
    # session.cookies.save()

    # 读取cookie中的XSRF-TOKEN存入headers_专栏里的X-XSRF-TOKEN
    # headers_douban['X-XSRF-TOKEN'] = requests.utils.dict_from_cookiejar(session.cookies)['XSRF-TOKEN']

    # post图片文件
    login_page = session.post(post_url, data=data, files=files, headers=headers_douban);
    
    res = json.loads(login_page.text)
    print(res)
    image_url = res['photo']['url']
    # 打印生成的图片url
    

    return {

        'image_url': image_url,
        'id': res['photo']['id']
    }

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

def trim(str):
    pattern = r'(^([\s])+)|(([\s])+$)'
    res = re.sub(pattern, '', str)
    return res;

def mkToDouban(mk_content):

    res = trim(mk_content)
    pattern = r'([\n])+'
    res = re.sub(pattern, '\n', res)
    res = res.split('\n')
    data = {

        'blocks': [],
        'entityMap': {}
    }

    image_count = 0;
    for i in range(0, len(res)):
        lineObj = mkLineToDouban(res[i])
        lineObj['key'] = 'kk_' + str(i)
        if lineObj['type'] == 'atomic':
            lineObj['entityRanges'][0]['key'] = image_count
            imageObj = getDobanImageObj(res[i])
            data['entityMap'][str(image_count)] = imageObj
            image_count = image_count + 1;

        data['blocks'].append(lineObj)

    return json.dumps(data)
    
def mkLineToDouban(mk_line):
    
    obj = {}
    mk_line = trim(mk_line)

    pattern = r'^\*\*([^*]+)\*\*$'
    content = re.findall(pattern, mk_line)
    if len(content) > 0:
        
        obj = getDobanObj()
        obj['text'] = content[0]
        obj['inlineStyleRanges'][0]['length'] = len(content[0])
        obj['inlineStyleRanges'][0]['style'] = 'BOLD'
        return obj

    pattern = r'^\*\*\*([^*]+)\*\*\*$'
    content = re.findall(pattern, mk_line)
    if len(content) > 0:
        
        obj = getDobanObj()
        obj['text'] = content[0]
        obj['inlineStyleRanges'][0]['length'] = len(content[0])
        obj['inlineStyleRanges'][0]['style'] = 'BOLD'
        return obj

    pattern = r'^>(.*?)$'
    content = re.findall(pattern, mk_line)
    if len(content) > 0:
        
        obj = getDobanObj()
        obj['text'] = content[0]
        obj['type'] = 'blockquote'
        obj['inlineStyleRanges'] = []
        return obj

    pattern = r'^!\[\]\((.*?)\)$'
    content = re.findall(pattern, mk_line)
    if len(content) > 0:
        
        obj = getDobanObj()
        obj['text'] = ''
        obj['type'] = 'atomic'
        obj['inlineStyleRanges'] = []
        obj['entityRanges'] = [{
            
            'offset': 0,
            'length': 1,
            'key': 0
        }]
        return obj

    obj = getDobanObj()
    obj['text'] = mk_line
    obj['inlineStyleRanges'] = []
    return obj


def getDobanObj():

    return {
        
        'key': "bj9pr",
        'text': "2018.06.23",
        'type': "unstyled",
        'depth': 0,
        'inlineStyleRanges': [{
            'offset': 0,
            'length': 0,
            'style': ''         
        }],
        'entityRanges': [],
        'data': {}
    }

def getDobanImageObj(mk_line):

    pattern = r'^!\[\]\(\/\/upload-images\.jianshu\.io\/upload_images\/(.*?)\)$'
    content = re.findall(pattern, mk_line)
    
    if len(content) > 0:
        
        return {
            'type': 'IMAGE',
            'mutability': 'IMMUTABLE',
            'data': {
                'src': global_img_file_new_url[content[0]]['image_url'],
                'width': 600,
                'is_animated': 'false',
                'caption': '',
                'id': global_img_file_new_url[content[0]]['id'],
                "height": 400
            }
        }
        
    

def pub(file_parent_path, folder):

    initial()

    global global_img_file_new_url
    global_img_file_new_url = get_img_file_new_url(file_parent_path, folder)
    
    title = re.sub(r'_[^_]*_', '.', folder)

    file_pre = file_parent_path + os.path.sep + folder + os.path.sep
    file_mk_path = file_pre + 'index.md'

    # 读取index.md
    index_mk_file = open(file_mk_path, 'r', encoding='utf-8')
    file_mk_content = index_mk_file.read()
    index_mk_file.close()
    
    note_text = mkToDouban(file_mk_content)
    # print(note_text)


    # return
    post_url = 'https://www.douban.com/j/note/publish'
    headers_douban = {

        'Host': 'www.douban.com',
        'Origin': 'https://www.douban.com',
        'Referer': 'https://www.douban.com/note/create',
        'User-Agent': agent,
        # 'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': cf.get('douban', 'cookie')

    }

    data = {

        'is_rich': '1',
        'note_id': global_note_id,
        'note_title': title,
        'note_text': note_text,
        'introduction': '',
        'note_privacy': 'P',
        'cannot_reply': '',
        'author_tags': '人文',
        'accept_donation': '',
        'donation_notice': '',
        'is_original': 'on',
        'ck': 'cHzd',
        'action': 'new',
        # 'captcha-id':'O7cFkbicukr62rX7C3l0BlmD:en',
        # 'captcha-solution':'stomach'
    }

    login_page = session.post(post_url, data=data, headers=headers_douban)
    print(login_page.text)
    res = json.loads(login_page.text)
    # print(res)
    if ('captcha_id' in res) and res['captcha_id'] != '':
        data['captcha-id'] = res['captcha_id']
        data['captcha-solution'] = get_captcha(res['captcha_img'])    
        login_page = session.post(post_url, data=data, headers=headers_douban)
        res = json.loads(login_page.text)
        print(res)

    
def get_captcha(captcha_img_url):

    headers = {

        'Host': 'www.douban.com',
        'Origin': 'https://www.douban.com',
        'Referer': 'https://www.douban.com/note/create',
        'User-Agent': agent,
        'X-XSRF-TOKEN': '',
        # 'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': cf.get('douban', 'cookie')

    }

    r = session.get(captcha_img_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha    

    


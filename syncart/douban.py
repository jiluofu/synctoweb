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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from requests_toolbelt.multipart.encoder import MultipartEncoder

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
chromedriver_path = '/Users/zhuxu/Documents/mmjstool/synctoweb/chromedriver'


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
        'Content-Type': 'text/html;charset=UTF-8',
        'Cookie': cookie

    }



    # 通过get_url，使得session获得专栏的cookie，里面有X-XSRF-TOKEN
    login_page = session.get(url, headers=headers_douban, allow_redirects=False, verify=False);
    

    pattern = r'摹喵居士'
    res = re.findall(pattern, login_page.text)
    if len(res) > 0:
        print('douban cookie is ok.')
        return True;
    else:
        return False;


def getCookie():

    url = 'https://www.douban.com/'
    chrome_options = Options()
    service = Service(executable_path = chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(5)
    # print(username)
    # driver.find_element_by_id('form_email').send_keys(username)
    # driver.find_element_by_id('form_password').send_keys(password)

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
    login_page = session.get(get_url, headers=headers_douban, verify=False);
    
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

        'ck': ck,
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
    print(login_page.text)
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
            print(555555)
            imageObj = getDobanImageObj(res[i])
            print(imageObj)
            data['entityMap'][str(image_count)] = imageObj
            image_count = image_count + 1;

        data['blocks'].append(lineObj)
    print(data)
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

    pattern = r'([^\/]*\.(jpg|jpeg|png))'
    content = re.findall(pattern, mk_line)
    print(content)
    
    if len(content) > 0:

        return {
            'type': 'IMAGE',
            'mutability': 'IMMUTABLE',
            'data': {
                'src': global_img_file_new_url[content[0][0].replace('%20', ' ')]['image_url'],
                'width': 600,
                'is_animated': 'false',
                'caption': '',
                'id': global_img_file_new_url[content[0][0].replace('%20', ' ')]['id'],
                "height": 400
            }
        }
        
    

def pub(file_parent_path, folder):

    initial()

    headers_douban = {

        'Host': 'www.douban.com',
        'Origin': 'https://www.douban.com',
        'Referer': 'https://www.douban.com/note/create',
        'User-Agent': agent,
        # 'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': cf.get('douban', 'cookie')

    }

    url = 'https://www.douban.com/'
    login_page = session.get(url, headers=headers_douban, allow_redirects=False, verify=False);
    pattern = r'name="ck" value="([^"]*)"'
    res = re.findall(pattern, login_page.text)
    global ck
    ck = res[0]
    print(111)
    print(ck)


    global global_img_file_new_url
    global_img_file_new_url = get_img_file_new_url(file_parent_path, folder)
    print(222)
    print(global_img_file_new_url)
    
    title = re.sub(r'_[^_]*_', '.', folder)

    file_pre = file_parent_path + os.path.sep + folder + os.path.sep
    file_mk_path = file_pre + 'index.md'

    # 读取index.md
    index_mk_file = open(file_mk_path, 'r', encoding='utf-8')
    file_mk_content = index_mk_file.read()
    file_mk_content = file_mk_content.replace('?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240', '')
    file_mk_content = file_mk_content.replace('![封面]', '![]')
    index_mk_file.close()
    
    print(file_mk_content)
    note_text = mkToDouban(file_mk_content)
    # print(note_text)


    # return
    post_url = 'https://www.douban.com/j/note/publish'

    data = {

        'is_rich': '1',
        'note_id': global_note_id,
        'note_title': title,
        'note_text': note_text,
        'introduction': '',
        'note_privacy': 'P',
        'cannot_reply': '',
        'author_tags': '人文',
        'accept_donation': 'on',
        'donation_notice': '沽之哉，沽之哉！我待贾者也',
        'is_original': 'on',
        'ck': ck,
        'action': 'new',
        # 'captcha-id':'O7cFkbicukr62rX7C3l0BlmD:en',
        # 'captcha-solution':'stomach'
    }

    headers_douban_create = {

        'Host': 'www.douban.com',
        'Origin': 'https://www.douban.com',
        'Referer': 'https://www.douban.com/people/Jiluofu/notes',
        'User-Agent': agent,
        # 'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': cf.get('douban', 'cookie')

    }
    url = 'https://www.douban.com/note/create'
    login_page = session.get(url, headers=headers_douban_create);
    print(login_page.text)
    pattern = r'name="captcha-id" value="([^"]*)"'
    captcha_id = re.findall(pattern, login_page.text)
    print(captcha_id)
    pattern = r'id="captcha_image" src="([^"]*)"'
    captcha_img = re.findall(pattern, login_page.text)
    print(captcha_img)
    
    if len(captcha_id) > 0:
        data['captcha-id'] = captcha_id[0]
        data['captcha-solution'] = get_captcha(captcha_img[0])    

    m = MultipartEncoder(fields=data)
    print("mmmmmmmm")
    print(m.content_type)
    print(m)
    headers_douban['Content-Type'] = m.content_type
    headers_douban['Sec-Fetch-Dest'] = 'empty'
    headers_douban['Sec-Fetch-Mode'] = 'cors'
    headers_douban['Sec-Fetch-Site'] = 'same-origin'
    headers_douban['Accept-Encoding'] = 'gzip, deflate, br'
    print(headers_douban)

    
    

    login_page = session.post(post_url, data=m, headers=headers_douban)
    print(33333333)
    print(login_page.text)
    

    
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

    r = session.get(captcha_img_url, headers=headers, verify=False)
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

    



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

cf = configparser.RawConfigParser()
cf.read(os.path.dirname(__file__) + os.path.sep + 'sync.conf')
username = cf.get('zhihu', 'username')
password = cf.get('zhihu', 'password')
cookie = cf.get('zhihu', 'cookie')

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()



def get_xsrf():
    '''_xsrf 是一个动态变化的参数'''
    index_url = 'http://www.zhihu.com'
    # 获取登录时需要用到的_xsrf
    index_page = session.get(index_url, headers=headers)
    html = index_page.text

    pattern = r'name="_xsrf" value="(.*?)"'
    # 这里的_xsrf 返回的是一个list
    _xsrf = re.findall(pattern, html)

    return _xsrf[0]


# 获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        # vcode = pytesseract.image_to_string(im)
        # print(vode)
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"

    login_code = session.get(url, headers=headers, allow_redirects=False).status_code

    if login_code == 200:
        session.cookies.save()
        return True
    else:
        return False


def login(secret, account):

    # headers["X-Xsrftoken"] = get_xsrf()
    # headers["X-Requested-With"] = "XMLHttpRequest"

    # 通过输入的用户名判断是否是手机号
    if re.match(r"^1\d{10}$", account):
        print("手机号登录 \n")
        post_url = 'http://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': get_xsrf(),
            'password': secret,
            'remember_me': 'true',
            'phone_num': account,
        }
    else:
        if "@" in account:
            print("邮箱登录 \n")
        else:
            print("你的账号输入有问题，请重新登录")
            return 0
        post_url = 'https://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': get_xsrf(),
            'password': secret,
            'remember_me': 'true',
            'email': account,
        }
    # try:
    #     # 不需要验证码直接登录成功
    #     login_page = session.post(post_url, data=postdata, headers=headers)
    #     login_code = login_page.text
    #     print(login_page.status_code)
    #     print(login_code)
    # except:
    # 需要输入验证码后才能登录成功


    postdata["captcha"] = get_captcha()

    login_page = session.post(post_url, data=postdata, headers=headers)
    # print(login_page.text)
    login_code = eval(login_page.text)

    session.cookies.save()
    # print(session.cookies['zhihu.com'])

try:
    input = raw_input
except:
    pass

def initial():

    print('init zhihu')

    # 使用登录cookie信息
    session.cookies = cookielib.LWPCookieJar(filename='cookies_zhihu')

    try:
        session.cookies.load(ignore_discard=True)
    except:
        print("Cookie 未能加载")

    if isLogin():
        print('您已经登录zhihu')

    else:
        # account = input('请输入你的用户名\n>  ')
        account = username
        secret = password
        login(secret, account)

def upload_img(img_file_path):

    # 构造要发布的图片文件
    files = {'upload_file': open(img_file_path, 'rb')}

    post_url = 'https://zhuanlan.zhihu.com/api/upload'
    headers_zhuanlan = {
        "Host": "zhuanlan.zhihu.com",
        "Referer": "https://zhuanlan.zhihu.com/",
        'User-Agent': agent,
        'X-XSRF-TOKEN': ''
    }

    get_url = 'https://zhuanlan.zhihu.com/api/me'

    # 通过get_url，使得session获得专栏的cookie，里面有X-XSRF-TOKEN
    login_page = session.get(get_url, headers=headers_zhuanlan, allow_redirects=False);
    session.cookies.save()

    # 读取cookie中的XSRF-TOKEN存入headers_专栏里的X-XSRF-TOKEN
    headers_zhuanlan['X-XSRF-TOKEN'] = requests.utils.dict_from_cookiejar(session.cookies)['XSRF-TOKEN']

    # post图片文件
    login_page = session.post(post_url, files=files, headers=headers_zhuanlan);
    login_code = eval(login_page.text)

    # 打印生成的图片url

    return login_code['msg'][0]

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
        # 'Cookie': cookie

    }

    # get_url = 'https://zhuanlan.zhihu.com/write'

    # # 通过get_url，使得session获得专栏的cookie，里面有X-XSRF-TOKEN
    # login_page = session.get(get_url, headers=headers_zhuanlan, allow_redirects=False);
    # print(login_page.text)

    get_url = 'https://zhuanlan.zhihu.com/api/me'

    # 通过get_url，使得session获得专栏的cookie，里面有X-XSRF-TOKEN
    login_page = session.get(get_url, headers=headers_zhuanlan, allow_redirects=False);
    session.cookies.save()

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
    session.cookies.save()

    # 知乎草稿返回结果403时，网页登录发文章页面，把cookie写入header_zhuanlan即可
    print(login_page)



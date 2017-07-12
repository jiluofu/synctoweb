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
# import pytesseract
import hashlib
import json
import sys

from syncart import init
import configparser

cf = configparser.RawConfigParser()
cf.read(os.path.dirname(__file__) + os.path.sep + 'sync.conf')
username = cf.get('mpwx', 'username')
password = cf.get('mpwx', 'password')
tag = cf.get('mpwx', 'tag')

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'Host': 'mp.weixin.qq.com',
    'Referer': 'https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN',
    'User-Agent': agent,
    'Origin': 'https://mp.weixin.qq.com'
}

# 使用登录cookie信息
session = requests.session()

token = ''
ticket = ''


def login(username, password):


    t = str(int(time.time() * 1000))

    # 微信公众平台的密码要md5
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    password = m.hexdigest()

    post_url = 'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin'


    data = {

        'username': username,
        'f': 'json',
        'pwd': password,
        'imgcode': ''
    }

    login_page = session.post(post_url, data=data, headers=headers, allow_redirects=False)
    # print(login_page.text)
    print(session.cookies)
    # session.cookies.save()



    url = 'https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&token=&lang=zh_CN&token=&lang=zh_CN&f=json&ajax=1&random=0.202972810079751'
    login_page = session.get(url, headers=headers)
    print("ask0:" + login_page.text)



    # 二维码的图片url，需要上面的ticket和uuid
    img_url = 'https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300&rd=' + t
    print(img_url)

    r = session.get(img_url, headers=headers)
    with open('qrcode.jpg', 'wb') as f:
        f.write(r.content)
        f.close()

    im = Image.open('qrcode.jpg')
    im.show()
    im.close()


    print('waiting for qrcode')
    time.sleep(20)
    print('going on')

    try:
        url = 'https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&token=&lang=zh_CN&token=&lang=zh_CN&f=json&ajax=1&random=0.202972810079751'
        login_page = session.get(url, headers=headers)
        print("ask1:" + login_page.text)
    except Exception as e:
        print(e)

    time.sleep(1)

    try:
        url = 'https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&token=&lang=zh_CN&token=&lang=zh_CN&f=json&ajax=1&random=0.202972810079751'
        login_page = session.get(url, headers=headers)
        print("ask2:" + login_page.text)
    except Exception as e:
        print(e)

    post_url = 'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login'
    data = {

        'token': '',
        'f': 'json',
        'ajax': '1',
        'lang': ''
    }

    login_page = session.post(post_url, data=data, headers=headers)
    print("bizlogin?action=login:" + login_page.text)
    session.cookies.save()
    res = eval(login_page.text)


    if 'redirect_url' not in res:
        print('请刷二维码')
        sys.exit()

    global token
    pattern = r'token=([^&=]*)'
    token = re.findall(pattern, res['redirect_url'])
    token = token[0]
    print(token)

    url = 'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&token=' + token + '&lang=zh_CN'
    login_page = session.get(url, headers=headers)
    # print(login_page.text)
    pattern = r'ticket:"([^"]*)",'
    global ticket
    ticket = re.findall(pattern, login_page.text)
    ticket = ticket[0]
    print("get ticket:" + ticket)



try:
    input = raw_input
except:
    pass

def inital():

    print('init mpwx')
    # return False


    # 使用登录cookie信息
    session.cookies = cookielib.LWPCookieJar(filename='cookies_mpwx')

    try:
        session.cookies.load(ignore_discard=True)
    except:
        print("Cookie 未能加载")

    login(username, password)

    return False

def upload_img_by_url(img_file_path):

    # print(img_file_path)

    pattern = r'/([^/]*)$'
    img_file_name = re.findall(pattern, img_file_path)
    img_file_name = img_file_name[0]
    img_url = 'https://upload-images.jianshu.io/upload_images/' + img_file_name + '?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'
    print(img_url)

    # print(token)
    post_url = 'https://mp.weixin.qq.com/cgi-bin/uploadimg2cdn?lang=zh_CN&token=' + token
    # print(post_url)
    data = {

        'imgurl': img_url,
        't': 'jax-editor-upload-img'
    }

    login_page = session.post(post_url, data=data, headers=headers)
    # print(login_page.text)
    res = eval(login_page.text)
    if res['errcode'] != 0:
        return ''

    url = res['url'].replace('\\', '')



    return url

def upload_img(img_file_path):

    pattern = r'/([^/]*)$'


    # print(token)
    post_url = 'https://mp.weixin.qq.com/cgi-bin/filetransfer'
    # print(post_url)
    data = {

        'action': 'upload_material',
        'f': 'json',
        'writetype': 'doublewrite',
        'groupid': '3',
        'ticket_id': 'momiaojushi',
        'ticket': ticket,
        # 'svr_time': '1499588746',
        'seq': '1'
    }

    files = {

        'file': open(img_file_path, 'rb')
    }

    login_page = session.post(post_url, data=data, files=files, headers=headers)
    print(login_page.text)
    res = eval(login_page.text)
    if res['base_resp']['ret'] != 0:
        return ''

    url = res['cdn_url'].replace('\\', '')



    return url

def get_img_file_new_url(file_parent_path, folder):

    file_pre = file_parent_path + os.path.sep + folder + os.path.sep

    img_file_new_url = {}
    img_files = init.listdir(file_pre + 'img')
    retry = 30
    for i in range(0, len(img_files)):
        img_file_path = file_pre + 'img' + os.path.sep + img_files[i]
        img_file_new_url[img_files[i]] = upload_img(img_file_path)

        for j in range(0, retry):

            if img_file_new_url[img_files[i]] == '':
                print('mpwx传图失败' + str(j + 1) + '/' + str(retry) + '，1秒后重试')
                time.sleep(1)
                img_file_new_url[img_files[i]] = upload_img(img_file_path)
            else:
                break;


        if img_file_new_url[img_files[i]] == '':
            print('mpwx传图最终失败')
            sys.exit()

        print(img_file_new_url[img_files[i]])

    # print(img_file_new_url)
    return img_file_new_url

def get_qsj_cover(file_parent_path, qsj_folder):

    qsj_cover = {}
    qsj_cover['folder'] = qsj_folder

    index_md_path = file_parent_path + os.sep + 'tmp' + os.sep + qsj_folder + os.sep + 'index.md'
    index_md_file = open(index_md_path, 'r', encoding='utf-8')
    file_md_content = index_md_file.read()
    index_md_file.close()

    pattern = r'\!\[\]\(([^\(\)]*?)\)'
    cover_url = re.findall(pattern, file_md_content)

    # if len(cover_url) == 1:
    #     cover_url = cover_url[0]
    # elif len(cover_url) >= 2:
    #     cover_url = cover_url[1]
    cover_url = cover_url[len(cover_url) - 1]

    # qsj_cover['cover_url'] = upload_img(cover_url)
    qsj_cover['cover_url'] = get_qsj_cover_local_by_url(file_parent_path, qsj_folder, cover_url)

    return qsj_cover

def get_qsj_cover_local_by_url(file_parent_path, qsj_folder, cover_url):


    cover_img_path = file_parent_path + os.sep + 'tmp' + os.sep + qsj_folder + os.sep + 'img'

    pattern = r'\/([^\/]*)$'
    cover_file_name = re.findall(pattern, cover_url)
    cover_file_path = cover_img_path + os.sep + cover_file_name[0]
    cover_url = upload_img(cover_file_path)


    return cover_url

def pub(file_parent_path, folder, qsj_folder_arr, url):

    inital()
    img_file_new_url = get_img_file_new_url(file_parent_path, folder)
    init.get_folder_imgs(file_parent_path, folder, img_file_new_url, 'mpwx')

    qsj_cover_arr = []
    print(qsj_folder_arr)

    for i in range(0, len(qsj_folder_arr)):
        img_file_new_url = get_img_file_new_url(file_parent_path + os.path.sep + 'tmp', qsj_folder_arr[i]['folder'])
        init.get_folder_imgs(file_parent_path + os.path.sep + 'tmp', qsj_folder_arr[i]['folder'], img_file_new_url, 'mpwx')
        qsj_cover = get_qsj_cover(file_parent_path, qsj_folder_arr[i]['folder'])
        qsj_cover_arr.append(qsj_cover)


    t = str(int(time.time() * 1000))

    title = re.sub(r'_[^_]*_', '.', folder)

    file_pre = file_parent_path + os.path.sep + folder + os.path.sep
    file_html_path = file_pre + 'index_mpwx.html'
    print(file_html_path)

    # 读取index.md
    index_html_file = open(file_html_path, 'r', encoding='utf-8')
    file_html_content = index_html_file.read()
    index_html_file.close()

    print(token)

    post_url = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?t=ajax-response&sub=create&type=10&token=' + token + '&lang=zh_CN'

    mpwx_cover_url = upload_img(init.cover['origin_file_path'])

    print(init.cover['origin_file_path'])
    file_html_content = file_html_content + add_qr_html()
    file_html_content = re.sub(r'[\n]', '', file_html_content)
    file_html_content = re.sub(r'<p>', '<p style="margin-top: 20px; margin-bottom: 20px;">', file_html_content)

    print(file_html_content)
    data = {

        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': t,
        'AppMsgId': '',
        'count': (len(qsj_folder_arr) + 1),
        'title0': title,
        'content0': file_html_content,
        'digest0': '',
        'author0': '喵爸',
        'fileid0': '',
        'cdn_url0': mpwx_cover_url,
        'music_id0': '',
        'video_id0': '',
        'show_cover_pic0': '0',
        'shortvideofileid0': '',
        'vid_type0': '',
        'need_open_comment0': '1',
        'only_fans_can_comment0': '0',
        'sourceurl0': url,
        'fee0': '0',
        'reprint_permit_type0': '1',
        'copyright_type0': '1',
        'original_article_type0': tag,
        'can_reward0': '1',
        'reward_wording0': '沽之哉，沽之哉！我待贾者也'

    }

    for i in range(0, len(qsj_folder_arr)):

        qsj_file_pre = file_parent_path + os.path.sep + 'tmp' + os.path.sep + qsj_folder_arr[i]['folder'] + os.path.sep
        qsj_file_html_path = qsj_file_pre + 'index_mpwx.html'
        qsj_index_html_file = open(qsj_file_html_path, 'r', encoding='utf-8')
        qsj_file_html_content = qsj_index_html_file.read()
        qsj_index_html_file.close()
        qsj_file_html_content = re.sub(r'[\n]', '', qsj_file_html_content)
        qsj_file_html_content = re.sub(r'<p>', '<p style="margin-top: 20px; margin-bottom: 20px;">', qsj_file_html_content)

        num = str(i + 1)
        data['title' + num] = '喵妈 | ' + qsj_folder_arr[i]['folder']
        data['content' + num] = qsj_file_html_content
        data['author' + num] = '喵妈'
        data['cdn_url' + num] = qsj_cover_arr[i]['cover_url']

        # data['fee' + num] = 1
        # data['need_open_comment' + num] = 1
        # data['only_fans_can_comment' + num] = 0
        # data['reprint_permit_type' + num] = 1
        # data['copyright_type' + num] = 1
        # data['original_article_type' + num] = '餐饮美食'


    # print(data)


    print(post_url)
    print(data)
    login_page = session.post(post_url, data=data, headers=headers);
    session.cookies.save()

    print(login_page.text)

def add_qr_html():

    html = '<p><img src="https://mmbiz.qlogo.cn/mmbiz_jpg/uDI3FLln00Yw8TN9swqCyMvEPGHH0IicT50wV24dsDZdAXcuibow9TkVtcQLjT8WTo6cTK72mZqhhib4uBBibfSKPg/0?wx_fmt=jpeg"></p>'

    return html








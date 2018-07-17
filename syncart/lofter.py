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
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path

from syncart import init
import configparser


cf = configparser.RawConfigParser()
cf.read(os.path.dirname(__file__) + os.path.sep + 'sync.conf')
cookie = cf.get('lofter', 'cookie')

session = requests.session()

agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

headers = {

    'Host': 'www.lofter.com',
    'Referer': 'http://www.lofter.com/login?urschecked=true',
    'User-Agent': agent,
    'Content-Type': 'text/plain'

}




def upload_img(img_file):

    t = str(int(time.time() * 1000))

    post_url = 'http://www.lofter.com/dwr/call/plaincall/ImageBean.genTokens.dwr'


    files = {

        'callCount': '1',
        'scriptSessionId': '${scriptSessionId}187',
        'httpSessionId': '',
        'c0-scriptName': 'ImageBean',
        'c0-methodName': 'genTokens',
        'c0-id': '0',
        'c0-param0': 'string:jpg',
        'c0-param1': 'string:',
        'c0-param2': 'string:',
        'c0-param3': 'string:',
        'c0-param4': 'string:1',
        'batchId': t
    }


    login_page = session.post(post_url, data=files, headers=headers);
    res = login_page.text

    pattern = r's0.bucketName="(.*?)";'
    bucketName = re.findall(pattern, res)[0]

    pattern = r's0.objectName="(.*?)";'
    objectName = re.findall(pattern, res)[0]

    pattern = r's0.uploadToken="(.*?)";'
    uploadToken = re.findall(pattern, res)[0]

    # imglf0或者是imglf1，也是根据上一个接口获得
    post_url = 'http://nos.netease.com/' + bucketName
    headers_lofter = {

        "Host": "nos.netease.com",
        "Referer": "http://www.lofter.com/",
        'User-Agent': agent,
    }

    # Object和x-nos-token是一一对应关系，这里写死的话，就是反复上传修改同一张图片而已
    # 需要上一个接口获得新的uploadToken和objectName
    post_data = {

        'Object': objectName,
        'x-nos-token': uploadToken
    }

    files = {

        'file': open(img_file, 'rb')
    }

    login_page = session.post(post_url, data=post_data, files=files, headers=headers_lofter, allow_redirects=False);

    img_new_url = 'http://' + bucketName + '.nosdn.127.net/' + objectName

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

    img_file_new_url = get_img_file_new_url(file_parent_path, folder)
    init.get_folder_imgs(file_parent_path, folder, img_file_new_url, 'lofter')

    title = re.sub(r'_[^_]*_', '.', folder)

    file_pre = file_parent_path + os.path.sep + folder + os.path.sep
    file_html_path = file_pre + 'index_lofter.html'

    # 读取index.md
    index_html_file = open(file_html_path, 'r', encoding='utf-8')
    file_html_content = index_html_file.read()
    index_html_file.close()

    session = requests.session()

    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

    headers = {

        'Host': 'www.lofter.com',
        'Referer': 'http://www.lofter.com/login?urschecked=true',
        'User-Agent': agent,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': cookie

    }

    t = str(int(time.time() * 1000))

    post_url = 'http://www.lofter.com/blog/jiluofu/new/text/'

    tagArr = init.getTags(cf.get('lofter', 'tag'))
    tag = ','.join(tagArr)
    
    data = {

        'allowView': '0',
        'blogId': '260597',
        'blogName': 'jiluofu',
        'cctype': '3',
        'content': file_html_content,
        'isPublished': 'true',
        'photoInfo': '[]',
        'syncSites': '',
        'tag': tag,
        'title': title,
        'valCode': ''
    }


    login_page = session.post(post_url, data=data, headers=headers);
    res = login_page.text
    print(res)






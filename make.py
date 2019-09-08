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
import shutil
import markdown
import codecs
import os
import time
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

from pyquery import PyQuery as pyq
import shutil
import configparser

cf = configparser.RawConfigParser()
sync_conf_path = os.path.dirname(__file__) + os.path.sep + os.path.sep + 'sync.conf'
cf.read(sync_conf_path)

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'Host': 'www.jianshu.com',
    'Referer': 'http://www.jianshu.com/',
    'User-Agent': agent,
    'Cookie': '__yadk_uid=3IwA3DYEI77kPvOoQoOjm0J4yfqh1OZy; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1563491638,1563577270,1563751778,1563920408; locale=zh-CN; read_mode=day; default_font=font1; remember_user_token=W1s1MTAwMV0sIiQyYSQxMCRXeDNPa2hvOWIxUXlVWjV6Znlnc0xPIiwiMTU2NDAwNjYzNS4xMzk4MzM1Il0%3D--538e215f5851a4adbd3ae6072e4e4e96a4c7e648; _m7e_session_core=cd060d5206077e85eca41f1c8a5ca0e2; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2251001%22%2C%22%24device_id%22%3A%2216c075d198f227-06b50d7bfdb19f-37677e02-2073600-16c075d1990eb6%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216c075d198f227-06b50d7bfdb19f-37677e02-2073600-16c075d1990eb6%22%7D; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1564006687'

}

headers_img = {
    'Host': 'upload-images.jianshu.io',
    'Referer': 'http://www.jianshu.com/',
    'User-Agent': agent
}

file_parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir) + os.path.sep)
root_path = file_parent_path + os.path.sep + 'momiaojushi'

# lofter_tag = cf.get('lofter', 'tag')
# lofter_tag_custom = input('lofter 自定义tag，英文逗号分隔>\n')


# 使用登录cookie信息
session = requests.session()
cover = {}

print('make')


def fetch_mk(root_path, title, no_cover = False):

    # dir_name = title.replace('.', '_' + date.replace('.', '') + '_')
    dir_path = root_path + os.path.sep + title

    # print(dir_name)


    index_md_path = dir_path + os.sep + 'index.md'
    index_file_new = open(index_md_path, 'r', encoding='utf-8')
    file_content = index_file_new.read()
    index_file_new.close()

    file_content = re.sub(r'!\[[^封面\[\]]*\]', '![]', file_content)
    file_content = file_content.replace('(media/', '(/Users/zhuxu/Documents/docs/media/')
    
    index_file_new = open(index_md_path, 'w', encoding='utf-8')
    index_file_new.write(file_content)
    index_file_new.close()

    img_dir_path = dir_path + os.sep + 'img'
    shutil.rmtree(img_dir_path)
    os.mkdir(img_dir_path)
    # print(file_content)

    imgs = get_imgs(file_content)
    
    for i in range(0, len(imgs)):
        
        img_file_name = imgs[i]

        cmd = 'cp ' + img_file_name.replace(' ', '\ ') + ' ' + img_dir_path
        print(cmd)
        os.system(cmd)
        
    # # 查找封面图
    # if no_cover == False:
    #     get_cover(file_content, dir_path)

    # index_html_path = dir_path + os.sep + 'index.html'
    # md_file = codecs.open(index_md_path, "r", "utf-8")
    # md_text = md_file.read()
    # index_html_content = markdown.markdown(md_text)  
    # index_file_new = open(index_html_path, 'w', encoding='utf-8')
    # index_file_new.write(index_html_content)
    # index_file_new.close()

    return title

def listdir(dir):
    imgs = []
    arr = os.listdir(dir)
    for i in range(0, len(arr)):
        # print(dir)
        if not arr[i].startswith('.'):
            imgs.append(arr[i])
    return imgs

def makeDir(file_name):

    index_md_path = root_path + os.path.sep + file_name
    index_file_new = open(index_md_path, 'r', encoding='utf-8')
    file_content = index_file_new.read()
    index_file_new.close()
    date = ''
    pattern = r'\*\*(\d\d\d\d\.\d\d\.\d\d)\*\*'
    res = re.findall(pattern, file_content)
    
    if len(res) > 0:
        date = res[0].replace('.', '')
    res = file_name.replace('.md', '').split('.')
    dir_name = file_name
    if len(res) == 2:
        dir_name = res[0] + '_' + date + '_' + res[1]
    else:
        dir_name = res[0].split('-')[1] + res[0].split('-')[2] + '-' + file_content.split('\n')[0]
    
    print(dir_name)
    print(file_name)

    img_dir_path = root_path + os.sep + dir_name

    print(img_dir_path)
    if os.path.isdir(img_dir_path):
        shutil.rmtree(img_dir_path)
    os.mkdir(img_dir_path)
    os.mkdir(img_dir_path + os.sep + 'img')
    
    shutil.copyfile(root_path + os.sep + file_name, img_dir_path + os.sep + 'index.md')
    shutil.move(root_path + os.sep + file_name, img_dir_path + os.sep)

def run():
    
    print(root_path)
    img_files = listdir(root_path)
    for i in range(0, len(img_files)):
        if (img_files[i].find('.md') != -1 and img_files[i] != 'sample.md' ):

            print(img_files[i])
            makeDir(img_files[i])

run()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
Info
- author : "zhuxu"
- email  : "zhu.xu@qq.com"
- date   : "2016.11.16"
Update

'''

import os.path
import re
import time

from syncart import lofter
from syncart import zhihu
from syncart import mpwx

mpwx_token = ''
mpwx_session = ''
mpwx_cover = ''
zhihu_cover = ''

def listdir(dir):
    imgs = []
    arr = os.listdir(dir)
    for i in range(0, len(arr)):
        # print(dir)
        if not arr[i].startswith('.'):
            imgs.append(arr[i])
    return imgs


def get_img_file_new_url(file_parent_path, folder, site):

    eval(site + '.init(mpwx_token, mpwx_session)')

    file_pre = file_parent_path + os.path.sep + folder + os.path.sep

    img_file_new_url = {}
    img_files = listdir(file_pre + 'img')
    for i in range(0, len(img_files)):
        img_file_path = file_pre + 'img' + os.path.sep + img_files[i]
        img_file_new_url[img_files[i]] = eval(site + '.upload_img(img_file_path)')
        print(img_file_new_url[img_files[i]])

    if site == 'mpwx':
        global mpwx_token
        mpwx_token = mpwx.token
        global mpwx_session
        mpwx_session = mpwx.session

    # print(img_file_new_url)
    return img_file_new_url

'''

'''
def get_imgs(file_parent_path, folder, site):

    # 文章index.md所在目录路径
    file_pre = file_parent_path + os.path.sep + folder + os.path.sep

    # 文章index.md文件路径
    file_path = file_pre + 'index.md'
    file_html_path = file_pre + 'index.html'

    # 读取index.md
    index_file = open(file_path, 'r', encoding='utf-8')
    file_content = index_file.read()
    index_file.close()

    index_html_file = open(file_html_path, 'r', encoding='utf-8')
    file_html_content = index_html_file.read()
    index_html_file.close()


    # 从img目录里找到所有的图片文件名数组
    img_files = listdir(file_pre + 'img')

    # 构建原始图片文件名和旧图片url的kv对象
    # 查找图片的markdown标签
    pattern = r'\!\[\]\((.*?)\)'

    # 得到所有就图片url的数组
    img_urls = re.findall(pattern, file_content)
    print(file_content)
    # if len(img_urls) == 0:
    #     pattern_img = r'<img data-original-src="([^"]*?)"[^<>]*?/>'
    #     img_urls = re.findall(pattern_img, file_content)
    #     #?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240
    #     for i in range(0, len(img_urls)):
    #         img_urls[i] = img_urls[i] + '?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'


    # 遍历找对应关系
    img_file_url = {};
    for i in range(0, len(img_files)):
        for j in range(0, len(img_urls)):
            if img_files[i] in img_urls[j]:
                img_file_url[img_files[i]] = img_urls[j]


    # 所有img的图片文件上传到服务器，获得原始图片文件名和图片url的kv对象
    img_file_new_url = {}
    img_file_new_url = get_img_file_new_url(file_parent_path, folder, site)
    print(img_file_new_url)

    global mpwx_cover
    global zhihu_cover
    for i in range(0, len(img_files)):
        if 'cover' in img_files[i]:
            if site == 'mpwx':
                mpwx_cover = img_file_new_url[img_files[i]]
            elif site == 'zhihu':
                zhihu_cover = img_file_new_url[img_files[i]]


    # index.md里寻找原始文名对应的图片url，将其对应的图片url换成上传后的图片url
    for i in range(0, len(img_files)):
        # print(img_files[i])
        if img_files[i] in img_file_url:
            file_content = file_content.replace(img_file_url[img_files[i]], img_file_new_url[img_files[i]])

    # 上传到指定网址后，生成对应的index_xxx.md
    index_file_new = open(file_pre + 'index_' + site + '.md', 'w', encoding='utf-8')
    index_file_new.write(file_content)
    index_file_new.close()

    # index.html里寻找原始文名对应的图片url，将其对应的图片url换成上传后的图片url
    for i in range(0, len(img_files)):
        if img_files[i] in img_file_url:
            file_html_content = file_html_content.replace(img_file_url[img_files[i]], img_file_new_url[img_files[i]])

    file_html_content = re.sub(r'<img src="([^\?]*?)\?(.*?)"([^<>]*?)/>', '<img src="\\1">', file_html_content)

    # 上传到指定网址后，生成对应的index_xxx.md
    index_file_new = open(file_pre + 'index_' + site + '.html', 'w', encoding='utf-8')
    index_file_new.write(file_html_content)
    index_file_new.close()
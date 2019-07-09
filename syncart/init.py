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
    'Cookie': 'co=doutui90100476227f59b52dc96fbb; __yadk_uid=RQx4A3aMJbJmlpb72vZCDk9JBtVuz2Eh; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1560981899,1561068014; locale=zh-CN; read_mode=day; default_font=font1; remember_user_token=W1s1MTAwMV0sIiQyYSQxMCRXeDNPa2hvOWIxUXlVWjV6Znlnc0xPIiwiMTU2MTQxMzkwOS4zNjM5ODI0Il0%3D--90160795986a0d33b4ea57e19852d5d0fd30ea16; _m7e_session_core=0b1b4aea03554d40a6987864c28bab1f; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1561414279; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216b71c585e0952-07abcc6a8d8661-37647e03-1296000-16b71c585e1720%22%2C%22%24device_id%22%3A%2216b71c585e0952-07abcc6a8d8661-37647e03-1296000-16b71c585e1720%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22%22%7D'

}

headers_img = {
    'Host': 'upload-images.jianshu.io',
    'Referer': 'http://www.jianshu.com/',
    'User-Agent': agent
}

# lofter_tag = cf.get('lofter', 'tag')
# lofter_tag_custom = input('lofter 自定义tag，英文逗号分隔>\n')


# 使用登录cookie信息
session = requests.session()
cover = {}

print('init')

def fetch_url(root_path, url, no_cover = False):

    html = session.get(url, headers=headers).text

    # 清除@JeanneQ后面奇怪字符引起的错误
    html = re.sub(r'@JeanneQ[^>]*', '', html)
    # print(html)
    pattern = r'<h1 class="title">(.*?)</h1>'
    # print(html)
    title = re.findall(pattern, html)[0]
    print(title)

    
    d = pyq(html);
    content = d('.show-content')
    d = pyq(content)

    p = d.find('p');
    date = p.eq(0).text()
    # print(date)


    dir_name = title.replace('.', '_' + date.replace('.', '') + '_')
    dir_path = root_path + os.path.sep + dir_name
    print(dir_name)

    # # 不下载图片
    # index_html_path = dir_path + os.sep + 'index.html'
    # index_file_new = open(index_html_path, 'r', encoding='utf-8')
    # file_content = index_file_new.read()
    # get_cover(file_content, dir_path)
    # return dir_name
    # # 不下载图片


    if os.path.exists(dir_path):
        shutil.rmtree(dir_path) 
    
    os.mkdir(dir_path)

    img_dir_path = dir_path + os.sep + 'img'
    os.mkdir(img_dir_path)

    content_html = content.html()


    
    pattern = r'<img data-original-src="([^"]*?)"[^<>]*?/>'
    content_html = re.sub(pattern, '<img src="\\1?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240"/>', content_html)
    # content_html = content_html.replace('<img src="https://github.com/jiluofu/jiluofu.github.com/raw/master/momiaojushi/static/qrcode.jpg" data-original-src="https://github.com/jiluofu/jiluofu.github.com/raw/master/momiaojushi/static/qrcode.jpg"/>', '')
    content_html = re.sub(r'<([^<>]*?)qrcode([^<>]*?)/>', '', content_html)
    

    content_html = re.sub(r'<div[^<>]*?>', '', content_html)
    content_html = content_html.replace('</div>', '')

    # print(content_html)
    imgs = get_imgs(content_html)
    
    for i in range(0, len(imgs)):
        pattern = r'/([^\?\/]*)\?[^\?\/]*/'

        img_file_name = re.findall(pattern, imgs[i])[0]

        print(imgs[i])
        print(img_file_name)
        # img_file_name = re.sub(r'http://(.*?)/([^/]+$)', '\\2', imgs[i])
        img_src_tmp = imgs[i];
        if img_src_tmp.find('http:') < 0:
            img_src_tmp = 'http:' + img_src_tmp;

        r = session.get(img_src_tmp, headers=headers_img)
        with open(img_dir_path + os.sep + img_file_name, 'wb') as f:
            f.write(r.content)
            f.close()
            print(img_file_name)

    index_html_path = dir_path + os.sep + 'index.html'
    file_content = content_html
    index_file_new = open(index_html_path, 'w', encoding='utf-8')
    index_file_new.write(file_content)
    index_file_new.close()

    index_md_path = dir_path + os.sep + 'index.md'
    file_content = html_to_mk(content_html)


    # 查找封面图
    if no_cover == False:
        get_cover(file_content, dir_path)
    index_file_new = open(index_md_path, 'w', encoding='utf-8')
    index_file_new.write(file_content)
    index_file_new.close()

    index_git_md_path = dir_path + os.sep + 'index_git.md'
    index_file_new = open(index_git_md_path, 'w', encoding='utf-8')
    index_file_new.write(file_content.replace('//upload-images.jianshu.io/upload_images/', 'img/'))
    index_file_new.close()

    

    return dir_name

def fetch_mk(root_path, title, no_cover = False):

    dir_name = title.replace('.', '_' + date.replace('.', '') + '_')
    dir_path = root_path + os.path.sep + dir_name
    print(dir_name)


    index_md_path = dir_path + os.sep + 'index.md'
    index_file_new = open(index_md_path, 'r', encoding='utf-8')
    file_content = index_file_new.read()
    index_file_new.close()

    img_dir_path = dir_path + os.sep + 'img'
    os.mkdir(img_dir_path)


    
    pattern = r'<img data-original-src="([^"]*?)"[^<>]*?/>'
    content_html = re.sub(pattern, '<img src="\\1?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240"/>', content_html)
    # content_html = content_html.replace('<img src="https://github.com/jiluofu/jiluofu.github.com/raw/master/momiaojushi/static/qrcode.jpg" data-original-src="https://github.com/jiluofu/jiluofu.github.com/raw/master/momiaojushi/static/qrcode.jpg"/>', '')
    content_html = re.sub(r'<([^<>]*?)qrcode([^<>]*?)/>', '', content_html)
    

    content_html = re.sub(r'<div[^<>]*?>', '', content_html)
    content_html = content_html.replace('</div>', '')

    # print(content_html)
    imgs = get_imgs(content_html)
    
    for i in range(0, len(imgs)):
        pattern = r'/([^\?\/]*)\?[^\?\/]*/'

        img_file_name = re.findall(pattern, imgs[i])[0]

        print(imgs[i])
        print(img_file_name)
        # img_file_name = re.sub(r'http://(.*?)/([^/]+$)', '\\2', imgs[i])
        img_src_tmp = imgs[i];
        if img_src_tmp.find('http:') < 0:
            img_src_tmp = 'http:' + img_src_tmp;

        r = session.get(img_src_tmp, headers=headers_img)
        with open(img_dir_path + os.sep + img_file_name, 'wb') as f:
            f.write(r.content)
            f.close()
            print(img_file_name)

    index_html_path = dir_path + os.sep + 'index.html'
    file_content = content_html
    index_file_new = open(index_html_path, 'w', encoding='utf-8')
    index_file_new.write(file_content)
    index_file_new.close()

    index_md_path = dir_path + os.sep + 'index.md'
    file_content = html_to_mk(content_html)


    # 查找封面图
    if no_cover == False:
        get_cover(file_content, dir_path)
    index_file_new = open(index_md_path, 'w', encoding='utf-8')
    index_file_new.write(file_content)
    index_file_new.close()

    index_git_md_path = dir_path + os.sep + 'index_git.md'
    index_file_new = open(index_git_md_path, 'w', encoding='utf-8')
    index_file_new.write(file_content.replace('//upload-images.jianshu.io/upload_images/', 'img/'))
    index_file_new.close()

    

    return dir_name

def get_cover(index_md_content, img_dir_path):
    pattern = r']\(([^\(\)]*)\)[\s]*封面'
    imgs = re.findall(pattern, index_md_content)

    if len(imgs) > 0:
        img = imgs[0] + '?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'
        pattern = r'\.([^\.]*)$'
        ext = re.findall(pattern, imgs[0])
        ext = ext[0]
        pattern = r'/([^/\.]*\.[^\.]*)$'
        origin_file_name = re.findall(pattern, imgs[0])
        origin_file_name = origin_file_name[0]
        cover['url'] = img
        cover['file_name'] = 'cover.' + ext
        cover['origin_file_name'] = origin_file_name
        cover['ext'] = ext 
        cover['origin_file_path'] = img_dir_path + os.sep + 'img' + os.sep + origin_file_name
        cover['file_path'] = img_dir_path + os.sep + cover['file_name']

        img_src_tmp = img;
        if img_src_tmp.find('http:') < 0:
            img_src_tmp = 'http:' + img_src_tmp;

        r = session.get(img_src_tmp, headers=headers_img)
        with open(cover['file_path'], 'wb') as f:
            f.write(r.content)
            f.close()
    else:
        img_file = listdir(img_dir_path + os.sep + 'img')
        img_file = img_file[0]
        # cover['url'] = img_url = 'http://upload-images.jianshu.io/upload_images/' + img_file + '?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'

        cover['origin_file_path'] = img_dir_path + os.sep + 'img' + os.sep + img_file
        cover['file_path'] = img_dir_path + os.sep + 'img' + os.sep + img_file
        

def get_qsj_folder(file_parent_path, qsj_url):
    
    qsj_folder = {}

    print(qsj_url)
    qsj_folder['folder'] = fetch_url(file_parent_path + os.path.sep + 'tmp', qsj_url, True)

    return qsj_folder


   
def get_imgs(html):
    
    pattern = r'<img src="([^"]*?)"[^<>]*?/>'
    imgs = re.findall(pattern, html)
    # if len(imgs) == 0:
    #     pattern = r'<img data-original-src="([^"]*?)"[^<>]*?/>'
    #     imgs = re.findall(pattern, html)
    #     #?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240
    #     for i in range(0, len(imgs)):
    #         imgs[i] = imgs[i] + '?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'
    return imgs
    
def html_to_mk(html):

    html = html.replace('<strong>', '**')
    html = html.replace('</strong>', '**')

    html = html.replace('<em>', '*')
    html = html.replace('</em>', '*')

    html = re.sub(r'<p>\n*', '\n', html)
    html = html.replace('</p>', '')

    html = re.sub(r'<div class="image-caption">', '', html)
    html = re.sub(r'<div(.*?)>', '', html)

    html = html.replace('</div>', '')
    html = html.replace('<br/>', '')
    html = html.replace('<hr/>', '')

    html = re.sub(r'<img src="([^\?]*?)\?(.*?)"/>', '![](\\1)', html)
    html = re.sub(r'<a href="([^"]*?)" [^<>]*?>([^<>]*?)</a>', '[\\2](\\1)', html)

    html = html.replace('</blockquote>', '\n')
    html = re.sub(r'<blockquote>\s*', '>', html)
    # html = re.sub(r'\n{2}', '\n', html)

    html = re.sub(r'<ul>\s*', '', html)
    html = html.replace('</ul>', '')
    html = html.replace('</li>', '')
    html = html.replace('<li>', '* ')


    mk = html

    return mk

def listdir(dir):
    imgs = []
    arr = os.listdir(dir)
    for i in range(0, len(arr)):
        # print(dir)
        if not arr[i].startswith('.'):
            imgs.append(arr[i])
    return imgs

def clean_tmp(tmp_path):

    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path) 
    
    os.mkdir(tmp_path)

def get_folder_imgs(file_parent_path, folder, img_file_new_url, site):

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
    # img_file_new_url = {}
    # img_file_new_url = get_img_file_new_url(file_parent_path, folder)
    print(img_file_new_url)

    # global mpwx_cover
    # global zhihu_cover
    # for i in range(0, len(img_files)):
    #     if 'cover' in img_files[i]:
    #         if site == 'mpwx':
    #             mpwx_cover = img_file_new_url[img_files[i]]
    #         elif site == 'zhihu':
    #             zhihu_cover = img_file_new_url[img_files[i]]


    # index.md里寻找原始文名对应的图片url，将其对应的图片url换成上传后的图片url
    for i in range(0, len(img_files)):
        # print(img_files[i])
        if img_files[i] in img_file_url:
            file_content = file_content.replace(img_file_url[img_files[i]], img_file_new_url[img_files[i]])
            file_content = file_content.replace('[封面]', '')

    # 上传到指定网址后，生成对应的index_xxx.md
    index_file_new = open(file_pre + 'index_' + site + '.md', 'w', encoding='utf-8')
    index_file_new.write(file_content)
    index_file_new.close()

    # index.html里寻找原始文名对应的图片url，将其对应的图片url换成上传后的图片url
    for i in range(0, len(img_files)):
        if img_files[i] in img_file_url:
            file_html_content = file_html_content.replace(img_file_url[img_files[i]], img_file_new_url[img_files[i]])

    file_html_content = re.sub(r'<img src="([^\?]*?)\?(.*?)"([^<>]*?)/>', '<img src="\\1">', file_html_content)
    file_html_content = file_html_content.replace('<div class="image-caption">封面</div>', '')
    
    # 上传到指定网址后，生成对应的index_xxx.md
    index_file_new = open(file_pre + 'index_' + site + '.html', 'w', encoding='utf-8')
    index_file_new.write(file_html_content)
    index_file_new.close()

def getTags(tags):
    tagArr = tags.split(',')
    arr = []
    pa = r'^-(.*)?'
    
    for i in range(0, len(tagArr)):
        res = re.findall(pa, tagArr[i])
        if len(res) == 0:
            arr.append(tagArr[i])
    return arr

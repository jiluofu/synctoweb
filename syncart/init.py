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

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'Host': 'www.jianshu.com',
    'Referer': 'http://www.jianshu.com/',
    'User-Agent': agent,
    'Cookie': 'UM_distinctid=15abf6020014ed-0cbf592aad2c5c-1d336f50-232800-15abf602002747; CNZZDATA1258679142=2085407508-1479623066-%7C1493240676; _gat=1; remember_user_token=W1s1MTAwMV0sIiQyYSQxMCRtc3JidDFZei90T2tvWWNkdXRNajV1IiwiMTQ5NDQ1NDg4OS45MTkyMDYxIl0%3D--c379df551f6d5d514dda483bcf3c6740539b68fc; _ga=GA1.2.1596808950.1479626705; _gid=GA1.2.16377653.1494454962; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1493331084,1493761829,1493761977; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1494454962; _session_id=djluY2dMQTcxNkhyeVBMcytYaGFvc2hSTnhlRWJBRC81TnRLakNCWjFscmZBMFNzandUUkY2N2t3WUNmdHJ3ZkpRUzhuRmZjcHY2WCt3Q0RpUDI2ZmQ3NC9nZVdMYTROVGVzNEtjUWhMMkNPMyszU0FHQnUzQ2FaL1lVYlFJY01URmpIK05OL3JvR3ZVMklxWTkxNXE2QzZ6eWc4VkpmVU1HOTNDRG9EeHdpRTFWdGNkbUVsUHQ4d3lXbDBDZHl0NmhMTmRzWGlQUW5EWDRXWTNqMFZVMG8ydWNZQzFhdTJaZXBaQW9paitPamtsNEExVFVGamFaelc0VTlyRm5FSWpsMWd2L2FhdGgwS2k0V0I5RVhMR3VqNGxNSnluQ08wekIyN1VrQlh2ajc1TUFKMGFyNGNDMjR6UFkyOE9FemFXbjMwY0YvTkFneFBVMDZFYjRkYU5FVVk3YzZ3M3pDTUxGa0NpdzdTb0lrMlQ2cGZFY0c5ZUc1d0JLYXppYllUUldaMTA2S1VPdkdMaHVzRW9YcW1Sd2xtSzZ6WnhKL2VyaUwyNllrTTNIST0tLWNUUVRNcm1UYlBvWDc3WFMxQXErWnc9PQ%3D%3D--18908551648588864676a18cd7025f8bd7e5b76c'

}

headers_img = {
    'Host': 'upload-images.jianshu.io',
    'Referer': 'http://www.jianshu.com/',
    'User-Agent': agent
}



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
    title = re.findall(pattern, html)[0]
    print(title)

    
    d = pyq(html);
    content = d('.show-content')
    d = pyq(content)

    p = d.find('p');
    date = p.eq(0).text()
    print(date)


    dir_name = title.replace('.', '_' + date.replace('.', '') + '_')
    dir_path = root_path + os.path.sep + dir_name
    print(dir_name)


    if os.path.exists(dir_path):
        shutil.rmtree(dir_path) 
    
    os.mkdir(dir_path)

    img_dir_path = dir_path + os.sep + 'img'
    os.mkdir(img_dir_path)
    imgs = get_imgs(content.html())
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
    file_content = content.html()
    index_file_new = open(index_html_path, 'w', encoding='utf-8')
    index_file_new.write(file_content)
    index_file_new.close()

    index_md_path = dir_path + os.sep + 'index.md'
    file_content = html_to_mk(content.html())


    # 查找封面图
    if no_cover == False:
        get_cover(file_content, dir_path)
    index_file_new = open(index_md_path, 'w', encoding='utf-8')
    index_file_new.write(file_content)
    index_file_new.close()

    

    return dir_name
def get_cover(index_md_content, img_dir_path):
    pattern = r']\(([^\(\)]*)\)封面'
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
    print(111)
    print(qsj_url)
    qsj_folder['folder'] = fetch_url(file_parent_path + os.path.sep + 'tmp', qsj_url, True)

    return qsj_folder


   
def get_imgs(html):
    
    pattern = r'<img src="([^"]*?)"[^<>]*?/>'
    imgs = re.findall(pattern, html)
    # print(imgs)
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


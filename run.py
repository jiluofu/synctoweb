#!/usr/local/bin/python3
# from syncart import  art
from syncart import  init

from syncart import lofter
from syncart import zhihu
from syncart import mpwx
from syncart import weibo
import os.path
import sys
import configparser

cf = configparser.RawConfigParser()
sync_conf_path = os.path.dirname(__file__) + os.path.sep + 'syncart' + os.path.sep + 'sync.conf'
cf.read(sync_conf_path)


try:
    input = raw_input
except:
    pass

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = input('请输入要处理的url\n>  ')


if (url.strip() == ''):
    print('要处理的文章url为空')
    print('上次填写的url是:' + cf.get('target', 'url'))

    ok = input('是否使用上次的文章url？y/n\n')
    if (ok == 'y'):
        url = cf.get('target', 'url')
    else:
        sys.exit()

cf.set('target', 'url', url)
cf.write(open(sync_conf_path, 'w'))


qsj = input('请输入要处理的qsj链接，空格分隔\n>  ')
# qsj = 'http://www.jianshu.com/p/c0159a3e2f73 http://www.jianshu.com/p/0f39cf1bd4b2'


if qsj.strip() != '':
    qsjurl = qsj.strip()
    qsj = qsjurl.split(' ')
    cf.set('target', 'qsjurl', qsjurl)
    cf.write(open(sync_conf_path, 'w'))
else:

    print('上次填写的qsj_url是:' + cf.get('target', 'qsjurl'))

    ok = input('是否使用上次qsj_url？y/n\n')
    if (ok == 'y'):
        qsjurl = cf.get('target', 'qsjurl')
        qsj = qsjurl.split(' ')
    else:
        qsjurl = ''
        qsj = []




# 根据简书发布的文章url，生成文章目录、img和index.md
# # 文章存放的路径在sync.py所在目录的上一级
file_parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir) + os.path.sep)
file_parent_path = file_parent_path + os.path.sep + 'momiaojushi'


folder = init.fetch_url(file_parent_path, url)
print(folder)
qsj_folder_arr = []
for i in range(0, len(qsj)):

    # qsj_folder = {}
    # qsj_folder['folder'] = init.fetch_url(file_parent_path + os.path.sep + 'tmp', qsj[i])

    qsj_folder = init.get_qsj_folder(file_parent_path, qsj[i])
    qsj_folder_arr.append(qsj_folder)


lofter.pub(file_parent_path, folder)
zhihu.pub(file_parent_path, folder)
weibo.pub(file_parent_path, folder)
mpwx.pub(file_parent_path, folder, qsj_folder_arr, url)

init.clean_tmp(file_parent_path + os.sep + 'tmp')





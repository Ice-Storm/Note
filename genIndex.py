#!/usr/bin/python
# encoding: utf8
import os
import re
Head = \
    'Index\n' \
    '=====\n' \
    '\n'

for root, dirs, files in os.walk('./', topdown=False):
    print root, dirs, files
    # 排除 images 文件夹
    if len(re.findall('/images$', root)) > 0:
        # if 'index.md' in files:
        #   os.unlink(root+'/index.md')
        continue
    # 排除隐藏文件夹
    if len(re.findall('/\.', root)) > 0:
        # if 'index.md' in files:
        # 	os.unlink(root+'/index.md')
        continue
    # 去除同名文件（如果已经有同名但是大小写不同，文件名不会程序被改变）
    os.unlink(root + '/index.md')
    index = open(root + '/index.md', 'w')
    index.write(Head)
    for d in dirs:
        # 排除隐藏文件夹和 images 文件夹
        if len(re.findall('^\.|^images$', d)) > 0:
            continue
        index.write('* [%s](%s/index.md)\n' % (d, d))
    index.write('\n' + '-'*20 + '\n\n')
    for f in files:
        if f == 'index.md' or f.strip() == '':
            continue
        # 排除隐藏文件
        if len(re.findall('^\.', f)) > 0:
            continue        
        index.write('* [%s](%s)\n' % (f.split('.')[0], f))

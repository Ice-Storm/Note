#!/usr/bin/python
# encoding: utf8
import os
import re
Head = '# Summary\n\n'

for root, dirs, files in os.walk('./'):
    print root, dirs, files
    # 排除 images 文件夹
    if len(re.findall('/images$', root)) > 0:
        # if 'index.md' in files:
        #   os.unlink(root+'/index.md')
        continue
    # 排除隐藏文件夹
    if len(re.findall('/\.', root)) > 0:
        # if 'index.md' in files:
        #   os.unlink(root+'/index.md')
        continue
    # 去除同名文件（如果已经有同名但是大小写不同，文件名不会程序被改变）
    # Mac OS X的默认情况下是“不区分大小写但保持大小写”
    # os.unlink(root + '/index.md')
    index = open(root + '/SUMMARY.md', 'w')
    head = root.rsplit('/',1)[-1]
    if head == '': 
        head = Head
    else:
        head = '# %s\n\n' % head
    index.write(head)
    
    if "README.md" in files:
        index.write('* [%s](%s)\n' % ('Introduce', "README.md"))
        files.remove("README.md")

    for d in dirs:
        # 排除隐藏文件夹和 images 文件夹
        if len(re.findall('^\.|^images$', d)) > 0:
            continue
        index.write('* [%s](%s/SUMMARY.md)\n' % (d, d))
        li = os.listdir(root + '/' + d)
        for l in li:
            if len(re.findall('^\.|^images$|^SUMMARY.md$', l)) > 0:
                continue
            index.write('\t* [%s](%s/%s)\n' % (l.rsplit('.', 1)[0], d, l))

    for f in files:
        # 排除目录和空白名字文件
        if f == 'SUMMARY.md' or f.strip() == '':
            continue
        # 排除隐藏文件
        if len(re.findall('^\.', f)) > 0:
            continue
        index.write('* [%s](%s)\n' % (f.rsplit('.', 1)[0], f))

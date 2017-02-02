#!/usr/bin/python
# encoding: utf8
import os
import re
Head = '# Summary\n\n'

summary = open('./SUMMARY.md', 'w')

summary.write(Head + '* [Introduce](./README.md)\n')

for root, dirs, files in os.walk('./'):
    print root
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
    # os.unlink(root + '/SUMMARY.md')
    # continue

    ds = root.split('/')
    if '' in ds:
        ds.remove('')
    indent = '\t' * (len(ds) - 1)
    print indent.count('\t')
    if ds[-1] != '.':
        summary.write(
            '%s* [%s](%s)\n' % ('\t' * (len(ds) - 2), ds[-1], os.path.join(root, 'README.md')))

    for f in files:
        # 排除隐藏文件
        if len(re.findall('^\.', f)) > 0:
            continue
        # 不是 markdown 文件就离开
        if f.rsplit('.', 1)[-1] != 'md':
            continue
        # 如果是 README 就直接离开
        if f == 'README.md' or f == 'SUMMARY.md':
            continue
        summary.write('%s* [%s](%s)\n' %
                      (indent, f.rsplit('.', 1)[0], os.path.join(root, f)))

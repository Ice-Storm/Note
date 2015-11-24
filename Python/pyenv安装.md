pyenv安装
=========

#pyenv安装
系统： centos 6.5 i686
系统python版本：2.6
pyenv安装： 根据github官方教程安装

安装完毕

#安装python2.7
先添加依赖包：

    sudo yum install readline readline-devel readline-static
    sudo yum install openssl openssl-devel openssl-static
    sudo yum install sqlite-devel
    sudo yum install bzip2-devel bzip2-libs

安装过程中错误处理：

* 缺少zlib
    - sudo apt-get install libbz2-dev (Debian)
    - sudo yum install libbz2-devel // or bzip2-devel (centos)
* 缺少sqlite3
    - sudo yum install sqlite-devel

#安装pyenv-virtualenv
查看github官方库，那里有详细教程。
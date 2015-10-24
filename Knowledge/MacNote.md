Note on Mac
===========
［TOC］

#Mac使用逻辑
Mac的'Command+'属于系统级快捷键，为整个系统提供了最小差异的快捷键方式。
'Control+'属于应用级的快捷键，每个应用内部的功能可以不同。
'option'键属于快捷键的补充组合。

Mac下命令行工具和linux下的命令行工具虽然接近，但是还是有区别的，想要获得和linux下相同的使用效果，可以考虑使用brew安装linux版本的命令行工具。

Mac 的默认分区是日志式，不区分大小写

#常用快捷键
command+tab 切换程序
command+`   切换同一程序下的窗口

#brew
是一个mac下很好用的包管理软件，类似linux下的apt-get，默认软件安装目录是/usr/local/，通过它安装的软件都会出现在该目录下，方便管理。
>brew 除了默认的库意外还有很多其他的库，详情可以看brew的github

##brew升级

    brew update
    brew outdated
    brew upgrade [software]
    brew cleanup

#brew cask
brew cask是brew下的gui管理软件，可以替代mac store使用，方便软件的安装和卸载。
要在brew cask下升级软件，直接使用cask卸载软件，再安装软件，就能升级。

#dash
mac下非常好用的编程文档查看器，程序员必备，付费软件。

#VoodooPad
一个很好的个人数据管理软件，可以写出类似wiki相互链接的笔记，方便索引和管理，正版需要收费。

#alfred
快速启动软件，配合workflow提高工作效率。

#python
可以通过brew在/usr/local安装一个python替代系统自带的python，方便以后添加和修改模块设置。python可以通过以下命令查看安装路径：

    print sys.path

>系统自带的easy_install安装pip遇到问题，下载完安装包后报No Error，但是又没有真的安装上pip，安装包的位置也没有找到(看easy_install源码应该是下载到了系统默认的临时文件夹，使用了tempfile模块)，为了避免以后遇到类似问题，开始使用用brew安装的/usr/local/目录下的python。

使用brew安装完python 后会提示

    pip install --upgrade setuptools
    pip install --upgrade pip

 但是升级setuptools失败，需要用pip卸载setuptools后手动安装，但是之后再用pip升级pip时，会出现一个6.0的巨大跨度版本，导致pip之后无法使用，所以升级完setuptools后暂时先不要升级pip，或者用easy_install来升级pip，否则只能

    remove (or backup) /usr/local/lib/python2.7, and
    brew rm python && brew install python

更温和的方法：

    From /usr/local/lib/python2.7/site-packages just remove:
    easy-install.pth
    pip-1.2.1-py2.7.egg or other versions of pip you have.
    distribute-0.6.34-py2.7.egg or other versions

##pyenv and pyenv-virtualenv
提供了单独为每个python项目配置python版本和模块的功能，虽然比不上docker，但是好在这是本地化的，也是必不可少的一个软件。

#coreutils

    brew install xz coreutils

通过在mac下安装gnu工具替代mac自带工具，获得和linux下更加一致的工具体验（只有一些基本的）。

#iterm
mac下的第三方终端，有着更加丰富的功能和配色。

#dircolor
配置终端配色，选用dircolors-solarized配色

#istat menu
实时显示mac下的硬件工作状态，需要付费。

#flux
支持全平台，能够调整屏幕色温，保护眼睛。

nginx搭建视频服务器
=================

1. nginx.conf中的user配置很重要，如果user和要访问的文件拥有者不同，很有可能出现404错误。
2. root和alias的区别，root不会叠加。
3. 无法直接访问到flv: flv和mp4下要指定root，大部分网上的教程都没指定，因为它们在同一目录下，如果不是一定要指定（使用绝对路径指定），flv正则匹配要加上播放器swf。
4. nginx无法从外网访问：
	- 确认nginx配置是否ok。(本机测试)
	- 确认网络是否可达。(telnet测试)
	- 是否受防火墙安全控制等。(修改防火墙设置)
	- 排除以上原因之后，远程实际再测试。

在centos7中我虽然关闭了防火墙，外部还是无法访问，打开防火墙后设置

    firewall-cmd --add-service=http              (即时打开)
    firewall-cmd --permanent --add-service=http  (写入配置文件)
telnet 80端口成功登录，网页访问正常。
5. 安装uwsgi时报错缺少Python.h，安转python-devel解决（缺少头文件一般是由于缺少对应的开发包）
6. uwsgi使用的python版本和virtualenv环境很重要，最好直接调用virtualenv中的uwsgi
7. uwsgi_params文件

```
	uwsgi_param QUERY_STRING $query_string;
	uwsgi_param REQUEST_METHOD $request_method;
	uwsgi_param CONTENT_TYPE $content_type;
	uwsgi_param CONTENT_LENGTH $content_length;
	uwsgi_param REQUEST_URI $request_uri;
	uwsgi_param PATH_INFO $document_uri;
	uwsgi_param DOCUMENT_ROOT $document_root;
	uwsgi_param SERVER_PROTOCOL $server_protocol;
	uwsgi_param REMOTE_ADDR $remote_addr;
	uwsgi_param REMOTE_PORT $remote_port;
	uwsgi_param SERVER_ADDR $server_addr;
	uwsgi_param SERVER_PORT $server_port;
	uwsgi_param SERVER_NAME $server_name;
```
 
8. uwsgi使用麻烦，可以考虑gunicorn代替。
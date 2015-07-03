Python编码
==========

在python3中，默认编码是Unicode，在2中默认编码是ascii，想要默认使用Unicode编码，可以在文件头部添加以下内容：

	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')

Python编码
==========

在python3中，默认编码是Unicode，在2中默认编码是ascii，想要默认使用Unicode编码，可以在文件头部添加以下内容：

	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')

python 对不同编码的字符串进行迭代时，是安照单元进行迭代，也就是"你好"分别遍历"你"和"好"两个字，而不是按照 byte 遍历。


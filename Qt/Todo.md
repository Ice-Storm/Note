# Qt pro 文件
Mac 下使用 Qt 编译界面程序默认会生成 app 文件，如果不想要，可以添加

	config -= app_bundle
	
# QString 
utf16

# QByteArray
byte 8bit.	 

# QTimer
QTimer 同线程内不 signal 不排序?。
QTimer 测试发现时钟间隔是以这样的逻辑进行的：

```python
while True:
	total_time += elapse_time         
	# 时间不是累计的，每一次在 timeout 槽中执行任务超过中断时间，之后立即发出新的 timeout 信号偿还，然后清空时间重新记录。
	if total_time > internal_time:
		total_time = 0
		emit timeout()  //
```
	
	
	


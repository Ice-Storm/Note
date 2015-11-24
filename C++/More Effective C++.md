# Operator
		    
	new operator ----> operator new : alloc memory
	           |-----> constructor
	
	delete operator ----> destructor
	              |-----> operator delete : release memory

     

# Exception
catch(...) 可以捕获所有 Exception 吗？ 答案是不，它不能捕获 Unexpected Exception, 默认情况下 Unexpected Exception 会直接 terminate 程序，可以通过 set_unexpected() 改变行为。

在函数调用链中，其中抛出了一个异常 A，一直向上传递，如果遇到 Exception specifications，但是 specifications 漏掉了该异常 A 的情况，则会发生 Unexpected Exception 错误，默认会直接结束程序。

# Virtual
纯虚函数并不代表不用实现，而是表示：

* 目前这个 class 是抽象的。
* 任何继承此 class 的具体类，都必须将该纯虚函数重新声明为一个正常的虚函数（也就是说，不可以令他“==0”）。


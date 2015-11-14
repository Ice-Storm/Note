# Python 内置函数

```
	__contains__ (如果未定义)-> __iter__ + __next__ (如果未定义) -> __getitem__
	
	__getattr__ (获取未定义属性)
	
	__getattribute__ （获取所有属性，包括未定义的，小心死循环，类需要继承 object 才有用）
	
	__getattribute__ (raise AttributeError)-> __getattr__
	
	__setattr__ (负责所有属性赋值，注意不要再__setattr__内调用__setattr__）
	
	__get__	(用于描述符获取属性）
	
	__set__ (用于描述符设置属性）
	
	__repr__ (返回字符串代表对象，在交互式情况下，每行的结果或调用__repr__输出)
	
	__str__ (当 print 和转换字符串时被自动调用)
	
	__str__ （在需要 __str__而未定义时）-> __repr__
	
	__add__, __iadd__, __radd__
	
	__mul__, __imul__, __rmul__
	
	__call__ 仿函数
	
	__lt__, __gt__, __eq__等， 没有 right-side 方法，而是互为 right-side,比如 __lt__ 和 __gt__, __eq__和__eq__, __ne__和__ne__.
	有些比较操作间没有必然的隐含关系，；例如==为真并不表示!=为假，例如，需要同时定义__eq__和__ne__保证正确。
	__cmp__是最底层的比较函数，如果其他比较没有定义的情况下会被底层调用，它的返回要处理成 True 和 False， 这个方法优先级比 right-side 函数还低。(removed in 3.0)
	
	__bool__ (if not define)-> __len__ -> True 
	Boolean test 环境下优先调用__bool__，如果未定义，调用 __len__获取长度，根据长度返回 bool 值，如果都未定义，返回 True。
	
	__del__ destructor method. 在垃圾收集时间会被自动调用。
```

>注意，python 不支持赋值运算符重载，这和 C++不同，python 的引用更像 C++的指针，而不是引用，对 python 的变量名赋值将改变变量名的引用对象，对 C++的引用赋值则将调用引用的对象的赋值方法。


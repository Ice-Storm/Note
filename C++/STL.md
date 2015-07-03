STL中需要注意的地方
================

#map
insert时相同的key不会被覆盖,你想表达的应该是下标访问表达式,map[key] =value;这样的调用是会被重写相应key的值的。

#thread
使用std::thread时，经常会报错误 *attempt to use a deleted function*，这通常是由于thread的invoke函数的参数是非const引起的。
C++ ODB Library
===============

[ODB: C++ Object-Relational Mapping (ORM)](http://www.codesynthesis.com/products/odb/)

libodb 是一个 c++ 的 ORM 库，支持 Qt，Boost 等库。

libodb value 类型无法嵌套容器，需要改成 object 类型才能嵌套，object 无法直接嵌套，需要改成指针类型形成成员关系，指针包括原始指针、智能指针（auto_ptr, weak_ptr, shared_ptr等）。还可以把容器序列化，转换成没有容器对象。其中 boost 有序列化库，google 有代码自动生成的序列化库[protocol-buffers](https://developers.google.com/protocol-buffers/docs/overview)


persist and update

persist auto id increase
update auto id stay

## Change-Tracking vector
数据库写入需要一个完整事务，如果有一部分失败就全体 rollback，对于内存中的对象，ODB 也尝试提供这种功能，可以和数据库同步 rollback。



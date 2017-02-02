# 初始化列表
c++ 11 中支持初始化列表语法。

```cpp
struct MyObject {
	MyObject (vector<int>){};
	vector<int> paraList;
};

std::vector<MyObject> objectList {{{0, 1, 2}} , {{0, 3, 1}} , {{5, 7, 5, 6}} ,{{4}}};
```


```
```


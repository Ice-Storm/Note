C++的模板摘要
===========

#函数模板重载
为了避免引起语言定义的麻烦，对模板的参数只允许准确的匹配，而且在解析重载问题时更偏向于具有同样名称的常规函数：
具有同样名称的模板函数和其他函数的重载解析可以分为以下3个步骤进行[ARM]:
1. 在函数中查找准确匹配
2. 查找这样的函数模板，从它出发能够生成出可以通过准确匹配进行调用的函数
3. 试着去做函数重载的解析
在上述过程中如果没有找到一个能够调用的函数，那么这个调用是错误的，若个在某一步发现了多个能匹配的候选者，则也是错误的。

#模板中的条件
C++模板不提供查询指定类型是否具有某个方法的功能，因此想要在模板中实现根据类型提供的不同方法调用不同的函数需要一些技巧。
以下是一个reverse()模板的例子：
```cpp
void f(LIstIter<int> 11, ListIter<int> 12, int* p1, int* p2)
{
    reverse(p1, p2);
    reverse(l1, l2);
}
template<class Iter>
inline void reverse(Iter first, Iter last)
{
    rev(first, last, IterType(first));
}
class RandomAccess{};
template<class T> inline RandomAccess IterType(T*)
{
    return RandomAccess();
}
class Forward{};
template<class T> inline Forward IterType(ListIterator<T>)
{
    return Forward();
}
```
在这里，int*将选择RandomAccess，而Lister将选择Forward.
```cpp
template<class Iter>
inline void rev(Iter first, Iter last, Forward)
{

}
template<class Iter>
inline void rev<Iter first, Iter last, RandomAccess)
{

}
```
如果其他方式都不行，有时还可以借助运行时类型识别机制。

#组合技术
模板能支持一些安全而又强有力的组合技术，例如，模板可以递归使用，可以派生。

#模板类之间的关系
在同一个模板生成出的类之间并不存在任何默认的关系，如果我们需要，可以使用继承来实现想要的关系。
还有一种技术可以实现同一个模板生成的类之间进行转化：
```cpp
template<class T> class Ptr { // point to T
    T* tp;
    Ptr(T*);
    friend template<class T2> class Ptr<T2>;
public:

    template<class T2> operator Ptr<T2>() {
        return Ptr<T2>(p); // works if p can be converted to a T2*
    }
};
```
但是不存在一种通用的方法，可以用于定义一个模版类产生出的不同类型之间的转换。
但是有一个比较好用的方法可以考虑：
```cpp
template<class scalar> class complex {
    scalar re, im;
public:

    template<class T2> complex(const complex<T2>& c)
        : re(c.re), im(c.im) {}
};
```


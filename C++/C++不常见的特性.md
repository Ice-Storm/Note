C++不常见的特性
=============

#成员指针
考虑C/C++里最辉煌的函数语法：

```c
int f(char* p) {}
int (*pf)(char* ) = &f;
int i = (*pf)("hello");
```
现在为成员函数构造出一种平行的东西：

```cpp
class S {
    int mf(char*);
};

int S::mf(char* p) {}
int (S::*pmf)(char*) = &S::mf;

S* p;
int i = (p->*pmf)("hello");
```

#运行时类型信息（RTTI）
* dynamic_cast 从对象的基类指针得到派生类指针。
* typeid 从基类指针识别出确切类型
* type_info 作为与有关类型的更多运行时类型信息的挂接点（hook）。

##一个例子：简单的对象I/O
说明用户如何与一个简单的对象I/O系统一起使用RTTI，并描述一个这样的对象I/O系统的肯能实现方案。用户希望能通过流直接读对象，确定它们具有某种预期的类型，然后使用它们。

```cpp
void user()
{
    // open file assumed to hold shapes, and
    // attach ss as an istream for that file
    // ...
    io_obj* p = get_obj(ss); // read object from stream
    if(Shape* sp = dynamic_cast<Shap*>(p)) {
        sp->draw();  // use the Shape
        //...
    }else{
        // oops: non-shape in Shape file
    }

}

typedef io_obj* (*PF)(istream&);
Map<String, PF> io_map;  // maps string to creation functions
io_obj* get_obj(istream& s)
{
    String str;
    if(get_word(s, str)==0) // read initial word into str
        throw no_class
    PF f = io_map[str]; // lookup 'str' to get function
    if(f == 0) throw unknown_class; // no match for 'str'
    io_obj* p = f(s); // construct object from stream
    if(debug) cout << typeid(*p).name() << '\n';
}
```
我们可以像平常一样定义Shape，除了令它从io_obj派生之外。
```cpp
class Shape: pblic io_obj {
    // ...
};
```

如果能够不加修改使用前面已经定义的Shape类层次，那当然是更有意思的（在许多情况下也是更实际的）：

```cpp
class iocircle: public Circle, public io_obj {
public:
    iocircle* clone() // override io_obj::clone()
    { return new iocircle(*this); }
    iocircle(istream&); // initialize from input stream
    static iocircle* new_circle(istream& s)
    {
        return new iocircle(s);
    }
    // ...

};
```

这里iocircle(istream&)的构造函数从自己的istream参数得到的数据去初始化相应的对象，new_circle就是应该被放进io_map里，使对象I/O系统能够知道这个类的函数。例如写：

```cpp
io_map["iocircle"] = &iocircle::new_circle;
class iotriangle: public Triangle, public io_obj {
    // ...
};
```
如果建立对象I/O的框架变得太冗长乏味，那么就可以用一个模板：

```cpp
template<class T>
class io: public T, public io_obj {
public:
    io* clone() // override io_obj::clone()
    { return new io(*this); }
    io(istream&);
    static io* new_io(istream& s)
    {
        return new io(s);
    }
    // ...

};
typedef io<Circle> iocircle;
```
我们当然还要明确定义io<Circle>::io(istream&)，因为它必须知道Circle的实现细节。
这个简单的对象I/O系统可能没有包含人们想要的所有东西，但它几乎可以放进一页纸里，其中许多地方使用了各种关键机制。一般的说，这种技术可以用到基于用户提供的字符串调用函数的任何地方。

当然，我们还是应该尽量减少RTTI的使用：

1. 最可取的是根本就不用运行时的类型信息机制，完全依靠静态的（编译时的）类型检查。
2. 如果这样做不行，我们最好只用动态强制。在这种情况下我们甚至不必知道对象的类型，也不必包含任何与RTTI有关的头文件。
3. 如果必须的话，我们可以做typeid()的比较。
4. 最后，如果确实需要知道关于一个类型的更多信——比如我们要实现一个调试系统，一个数据库系统，或者其他形式的对象I/O系统——那么我们就需要使用定义在typeid上的操作，以获得更详细的信息。

#强制的一种新记法
无论从语法上还是从语义上，强制都是C和C++中最难看的特征之一。这也就导致了一种持续的努力，为强制探寻各种替代品：函数声明使参数的隐式转换成为可能；模板、放松对虚函数的覆盖规则等，每个都清除掉一些强制的需要。另一方面，dynamic_cast运算符也是针对一类特殊情况，为原有强制提供的一种替代品。

* static_cast<T>(e)         //reasonable well-behaved casts
* dynamic_cast<T>(e)        //casts rely on runing information
* reinterpret_cast<T>(e)    //casts yielding values that must
* const_cast<T>(e)          //casting away const

C语言的强制有很多问题，并不推荐使用。
```cpp
class D: public A, private B {

} ;
void f(D* pd)
{
    B* pb1 = (B*)pd; // access to D's private base B
    B* pb2 = static_cast<B*>(pd); // error, can't access private
}
```

#通过派生对模板加强限制（不推荐）

```cpp
template<class T> 
class Comparable {
    T& operator=(const T&);
    int operator==(const T&, const T&);
};
template<class T: Comparable>
class vector{

};
```
这样能将检查错误和报告时间提前到相对独立编译单元进行编译的时候。
但是变现模板的人不可能预见到模板的全部应用。这就导致程序员在初期给模板参数加上了过分的限制，并且导致继承的滥用，它将继承机制用到了某些并不是子类型的事情上。

如果不调用，C++不会对一个特定的模板参数生成相应的函数版本，因此类型参数只要支持代码中调用到的方法需要使用的方法就行了。

#函数模板参数的显示描述
可以显示指定返回类型
```cpp
template<class T, class U> T convert(U u) { return u; }
void g(int i)
{
    convert(i);                 // error： cant't deduce T.
    convert<double>(i);         // T is double, U is int;
    convert<char, double>(i)
    convert<char*, double>(i)   // error: cantnot convert a double to a char*
}
```

#C++异常
在异常的设计中做了如下假定。

* 异常基本上是为了处理错误。
* 与函数定义相比，异常处理器是很少的
* 与函数调用相比，异常出现的频率低得多
* 异常是语言层的概念——不仅有实现问题，还不是错误处理策略。

异常处理的核心实际上是资源管理。特别是，一个函数掌握着某项资源，发生了异常情况，如果要编写容错的系统，我们就必须解决这类问题。

#空白基类最优化
C++裁定凡是独立（非附属）对象都必须有非零大小，通常C++官方勒令默默安插一个char到空对象内。
这个约束不适用于derived class对象内的base class成分，因为它们不是独立的。
```
class HoldsAnInt: private Empty {
private:
    int x;
}
```
sizeof(HoldsAnInt)==size(int)，这是所谓的EBO(empty base optimization; 空白基类最优化)，EBO一般只在单一继承中可行。

#virtual继承
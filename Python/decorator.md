Python 装饰器
=============

Python的函数也是对象，每次def创建一个新的对象。
Python对不同作用域访问的同一个变量会创建不同的cell对象。
Python的decorator可以起到和Ruby中使用block类似的作用。
#Managing Calls and Instances
#Managing Functions and Classes
#Coding Function Decorators
##Tracing Calls
##State Information Retention Options
##Timing Calls

```python
import time
class timer:
    def __init__(self, func):
        self.func = func
        self.alltime = 0
    def __call__(self, *args, **kargs):
        start = time.clock()
        result = self.func(*args, **kargs)
        esalpsed = time.clock() - start
        self.alltime += elapsed
        print('%s: %.5f, %5.f' % (self.func.__name__, elapsed, self.alltime))

@timer
def listcomp(N):
    return [x * 2 for x in range(N)]

@timer
def mapcall(N):
    return map((lambda x: x * 2), range(N))

result = listcomp(5)
print(result)
print('allTime = %s' % listcomp.alltme)
result = mapcall(5)
print(result)
print('allTime = %s' % mapcall.alltime)
```

##Adding Decorator Arguments

#Coding Class Decorators

##Singleton Classes

#常用 decorator

```python
# class property([fget[, fset[, fdel[, doc]]]])
class Parrot(object):
    def __init__(self):
        self._voltage = 100000

    @property
    def voltage(self):
        """Get the current voltage."""
        return self._voltage
# property 可以把函数名变成变量名，省去定义变量的麻烦，

@property
def cn(self):
    return ' '.join([name.encode('utf-8')
                     for name in (self.first_name, self.last_name)
                     if name])
# 获得的变量名其实是作为函数 cn的代理，每次获取变量，都使用了__get__内置方法（__get__在类中作为属性才有作用）

# classmethod
class C(object):
    @classmethod
    def f(cls, arg1, arg2, ...):
        pass

# staticmethod
class C(object):
    @staticmethod
    def f(arg1, arg2, ...):
        pass
```



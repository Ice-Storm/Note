Python 易错陷阱
==============

# List
```python
l = [[0]*2]*2 
l[0][0] = 1
# l = [[1, 0], [1, 0]]
```
这种方式创建的 list，每个子 list 指向相同的对象，因此改变一个子 list 的内部数据，相当于改变了所有的子 list。

# enclosure
```python
def fun():
	count = 0
	def _fun():
		count = count + 1
		return count
	return _fun()
fun()
# UnboundLocalError: local variable 'count' referenced before assignment
```
const 变量不要作为 enclosure 变量进行赋值，只能获取值，如果要赋值，需要使用 mutable 变量，如 list。

#  yield

```python
def fun():
    for i in range(3):
        yield i
fun()
# <generator object f at 0x0346EB98>
fun()
# 并不是每次调用返回一个数字，而是每次返回一个新的generator，这个generator从第一个开始迭代
for i in fun():
    print i
# 0
# 1
# 2

for i in fun():
    print i
# 0
# 1
# 2
```
Makefile 简记
=============

#Makefile中的预定义变量

- CC，C语言编译器的名称，cc
- CPP, C语言预处理器的名称，$(CC) -E
- CXX, C++语言的编译器名称，g++
- RM，删除文件程序的名称，rm -f
- CFLAGS, C语言编译器的编译选项，无默认值
- CPPFLAGS，C语言预处理器的编译选项，无默认值
- CXXFLAGS，C++语言编译器的编译选项，无默认值

>注：在使用RM时，一般使用如下语句： -$(RM) $(TARGET) $(OBJS), 符号“-”表示在操作失败时不报错，而是继续执行。例如在不存在TARGET时将继续删除OBJS。

#Makefile中的自动变量

- $*, 表示目标文件的名称，不包含扩展名
- $@, 表示目标文件的名称，包含扩展名
- $+, 表示所有的依赖文件，以空格隔开，可能含有重复的文件
- $^, 表示所有的依赖文件，以空格隔开，不重复
- $<, 表示依赖性中第一个依赖文件的名称
- $?, 依赖项中，所有比目标文件新的依赖文件

#搜索路径：

- VPATH，路径之间用：隔开
- 声明伪目标：
	.PHONY:clean

#Makefile中的函数：

- wildcard, 用法$(wildcard PATTERN), 查找当前目录下所有符合PATTERN的文件，返回文件名，用空格隔开，如$(wildcard *.c)
- patsubst, 用法$(patsubst PATTERN,REPLACEMENT,SOURCE), 查找SOURCE中符合PATTERN的单词，用REPLACEMENT规则替换，注意，要使用%通配符表示0到n个字符。例：$(patsubst %.c, %.o, $(wildcard *.c))
- foreach,一般用于多目录下文件的遍历。用法$(foreach VAR,LIST,TEXT), 将LIST字符串中一个空格分隔的单词，先传给VAR，再执行TEXT的表达式，TEXT表达式的返回值作为整个foreach的返回值。


自动推导：

	objects = main.o kbd.o command.o display.o \
	insert.o search.o files.o utils.o
	edit : $(objects)
		cc -o edit $(objects)

	main.o : defs.h
	kbd.o : defs.h command.h
	command.o : defs.h command.h
	display.o : defs.h buffer.h
	insert.o : defs.h buffer.h
	search.o : defs.h buffer.h
	files.o : defs.h buffer.h command.h
	utils.o : defs.h
	.PHONY : clean
	clean :
		rm edit $(objects)

自动生成依赖：

	cc -M main.c

自动生成依赖文件：

	%.d: %.c
	@set -e; rm -f $@; \
	$(CC) -M $(CPPFLAGS) $< > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$

变量赋值：
	
	A = $(B)
	B = $(A)  ＃ 会无限循环

	x := foo
	y := $(x) bar  ＃ 会立即展开
	x := later

	＃等价于
	y := foo bar
	x := later

	FOO ?= bar ＃ 如果FOO没有定义过，那么变量FOO的值就是bar，如果定义过，就什么也不做。





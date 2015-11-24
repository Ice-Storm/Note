Linux Kernel 2.6 Hacking之Kconfig
=====================================
[TOC]

linux在2.6以后将配置文件由原来的config.in改为kconfig，对于kconfig的语法在/Documentation/kbuild/kconfig-language.txt中做了详细介绍，这里给出个人翻译。
介绍
----
在配置数据库的配置选项以树的形式组织。

    +- Code maturity level options
    |  +- Prompt for development and/or incomplete code/drivers
    +- General setup
    |  +- Networking support
    |  +- System V IPC
    |  +- BSD Process Accounting
    |  +- Sysctl support
    +- Loadable module support
    |  +- Enable loadable module support
    |     +- Set version information on all module symbols
    |     +- Kernel module loader
    +- ...

每个条目都有其自己的依赖关系。这些关系决定了这个条目是否可见的。父条目可见，子条目才可见。

菜单项
------
大多数条目定义为配置选项，其他条目用来帮助组织他们。一条单独的配置选项定义如下：

    config MODVERSIONS
    bool "Set version information on all module symbols"
    depends on MODULES
    help
    Ususlly,modules have to be recompiled whenever you switch to a new kernel ...

每一行以一个关键词开始，并且可以跟随多个参数。“config”开始一个新的配置条目。这之后的几行定义了该配置选项的属性。属性中可以是该配置选项的类型，输入提示（input prompt），依赖关系，帮助信息和默认值。一个配置选项可以用相同名字定义多次，但是每个定义只能拥有一个输入提示（指所有同名项还是每个条目）并且类型不能冲）。

菜单属性
-------
一个菜单条目可以拥有很多属性。这些属性并不是在所有地方都可以使用（见语法）。

- 类型定义： "bool"/"tristate"/"string"/"hex"/"int"
  每个配置项必须拥有一个类型。这里一共只有两个基本类型：tristate和string；其他类型都是基于这两个类型的。类型定义可以用输入提示，所以这两个例子是等价的：
```
bool "Networking support"
和
bool
prompt "Networking support"
```
- 输入提示： 
```
"prompt" <prompt> ["if" <expr>]
```

  每个菜单条目可以拥有最多一个提示显示给用户。可以添加"if"来表示依赖关系，当然这是可选的。

- 默认值： 
```
"default" <expr> ["if" <expr>]
```

  一个配置项可以拥有任意多个默认值。如果拥有多个默认值，则只有第一个是有效的。默认值定义并不局限于他们被定义的菜单项（Default values are not limited to the menu entry where they are defined.）这意味着默认值可以被定义在任意位置或被更早的的定义覆盖。
  只有当用户没有设置配置项时（通过上面的用户提示），默认值会作为该配置项的值。如果输入提示可见，那么默认值也会显示给用户，并且可以让用户修改。
  可以添加"if"来设置依赖，这是可选项。

- 类型定义+默认值
```
"def_bool"/"def_tristate" <expr> ["if" <expr>]
```

  这是一个类型定义加上值的快捷符号定义。
  可选项"if"声明依赖。

- 依赖： 
```
"depends on" <expr>
```

  这为菜单条目定义了依赖。如果需要定义多个依赖，使用"&&"链接。依赖应用于当前菜单条目的所有选项（同样可以使用"if"表达式），所以下面两个例子是相同的。
```
bool "fool" if BAR
default y if BAR
和
depends on BAR
bool "fool"
default y
```

- 反向依赖： 
```
"select" <symbol> ["if" <expr>]
```

  尽管普通依赖可以减少选项的上限，使用反向依赖能把这一限制降得更低。当前菜单项的值是symbol的最小值，如果symbol被选择了多次，上限就是其中的最大值。
  反向依赖只能用在boolean和tristate选项上。

>注：select必须小心使用。select会强制设置符号值而不检查依赖。滥用select你可以选者符号FOO，尽管FOO的依赖BAR没有设置。总的来说select用来设置不可见符号（没有提示符）和没有依赖的符号。这会降低可用性但是另一方面避免了不合法的配置出现。

- 数据范围： 
```
"range" <symbol> <symbol> ["if" <expr>]
```

  为int和hex类型的选项数据设置可以接受的输入范围。用户只可以输入大于等于第一个symbol和小于等于第二个symbol的symbol。

- 帮助信息： 
```
"help" 或 "---help---"
```

  定义了帮助信息。帮助信息的结束以徐哦进水平决定，这也就意味着在比第一个帮助信息缩进小的行结束。
  "---help---"和"help"在行为上没有区别，"---help---"有助于开发人员可视化分开配置逻辑和帮助信息。

- 其他选项： 
```
"option" <symbol> [=<value>]
```

  通过这个选项语法可以定义各种普通选项用来修改菜单项以及配置符号的行为。以下这些选项目前可用：

  - "defconfig_list"
    这个定义了查找默认配置时使用的默认的项目表（当.config不存在的时候）
  - "modules"
    定义了被用作MODULES的符号，使所有配置符号都能获取到该符号状态。
  - "env"=<value> 
    导入环境变量到Kconfig。

菜单依赖关系
-----------
依赖关系决定了菜单条目是否可见，也可以减少tristate的输入范围。tristate逻辑比boolean逻辑在表达式中用更多的状态（state）来表示模块的状态。依赖关系拥有以下语法：

```
<expr> ::= <symbol>                                             (1)
           <symbol> '=' <symbol>                                (2)
           <symbol> '!=' <symbol>                               (3)
           '(' <expr> ')'                                       (4)
           '!' <expr>                                           (5)
           <expr>  '&&' <expr>                                  (6)
           <expr>  '||' <expr>                                  (7)
```

表达式以优先级降序列出。

(1)把符号赋给表达式。boolean和tristate类型都直接赋值给表达式。其他所有类型都赋值'n'
(2)如果两个symbol的值相等，返回'y'，否则返回'n'
(3)如果两个symbol的值相等，返回'n'，否则返回'y'
(4)返回表达式的值，用来改变优先级
(5)返回(2-/expr/)的结果
(6)返回min(/expr/,/expr/)
(7)返回max(/expr/,/expr/)

一个表达式可以有'n'，'m'，'y'（或者计算结果0，1，2）三个其中之一的值。一个菜单项的子菜单当他的表达式的值等于'm'或'y'时才可见。

symbol类型有两种：常量和非常量。非常量的symbol是最普遍的，由'config
'语句定义，完全由字符，数字和下划线组成。
常量symbol只是表达式的一部分。常量通常有单引号或双引号包裹，在引号中任意字符都可以使用，并且允许使用'\'转义。

菜单结构
--------

菜单项在树中的位置有两个方法决定。第一个是现实指定：
```
menu "Network device support"
    depends on NET
config NETDEVICES
    ...
endmenu
```
所有的条目包含在"menu"..."endmenu"中变成了"Network device support"的子菜单。所有子菜单都继承了父菜单的依赖关系，比如，"NET"依赖关系被加到了配置选项NETDEVICES依赖列表中。

还有一种方法生成菜单结构就是分析依赖关系。如果菜单选项一定程度上依赖前面的选项，它就能成为前面选项的子菜单。首先，前面的选项（父）必须是依赖列表的一部分并且必须满足下面两个条件：
- 如果父选项为'n'，子选项不可见
- 只有父选项可见，子选项才可见

```
config MODULES
    bool "Enable loadable module support"

config MODVERSIONS
    bool "Set version information on all module symbols"
    depends on MODULES

comment "module support disabled"
    depends on !MODULES
```
MODVERSIONS直接依赖MODULES，也就是说只有当MODULES不是'n'时MODVERSIONS才可见。
(The comment on the other hand is always
visible when MODULES is visible (the (empty) dependency of MODULES is
also part of the comment dependencies).似乎矛盾)

Kconfig语法
-----------

配置文件描述了一系列菜单项，每行都以关键字开头（除了帮助信息）。下面的关键字结束菜单选项：
- config
- menuconfig
- choice/endchoice
- comment
- menu/endmenu
- if/endif
- source
前五个同样可以开始定义一个菜单项。

config：

    "config" <symbol>
    <config options>

这定义了一个配置符号<symbol>比并且可以使用以上介绍的所有属性。

```
menuconfig:
    "menuconfig" <symbol>
    <config options>
```
这和上面提到的简单配置项类似，但是这个提供了一个提示在头部，所有的子选项作为独立行列表显示。

choices:

    "choice" [symbol]
    <choice options>
    <choice block>
    "endchoice"

该关键字定义了一组选项，并且选项可以使用前面所有的属性。一个选项只能是bool或tristate类型，如果是boolean类型的choice，则只允许选择其中一个配置选项，如果是tristate则允许任意数量个配置选项设置成'm'。这在一个硬件有多个驱动，只有一个驱动能编译并加载到内核，但是所有驱动能编译成模块的时候是很有用。
一个choice里可以接受的另一个选项是"optional"，这样就允许choice设置成'n'，没有条目被选中。
如果没有[symbol]和choice关联，你不能重复定义该choice。如果有[symbol]关联该choice，那么你可以在其他地方定义相同的choice（有同样的条目）

comment:

    "comment" <prompt>
    <comment options>

这里定义了在配置过程中给用户的注释，该注释还将写入输出文件中。唯一可用的选项是依赖关系。

menu:

    "menu" <prompt>
    <menu options>
    <menu block>
    "endmenu"

这个定义了一个菜单块，详细信息看前面的"菜单结构"。唯一可用的选项是依赖关系。

if:

    "if" <expr>
    <if block>
    "endif"

定义了一个if块结构，所有依赖关系<expr>会被添加到块里的菜单项中。

source:

    "source" <prompt>

读取指定的配置文件，该文件始终会被解析。

mainmenu:

    "mainmenu" <prompt>

如果配置程序选择使用它，就会设置配置程序的标题栏。这个条目应该被放在配置的顶部，所有语句的前面。

Kconfig 示例
------------
这里收集了Kconfig的例子，大多数无法一眼看明白，其中大多数内容是成为了Kconfig文件中的常用语句。

添加通用特性并完成使用配置

```
It is a common idiom to implement a feature/functionality that are
relevant for some architectures but not all.
The recommended way to do so is to use a config variable named HAVE_*
that is defined in a common Kconfig file and selected by the relevant
architectures.
An example is the generic IOMAP functionality.

We would in lib/Kconfig see:

# Generic IOMAP is used to ...
config HAVE_GENERIC_IOMAP

config GENERIC_IOMAP
    depends on HAVE_GENERIC_IOMAP && FOO

And in lib/Makefile we would see:
obj-$(CONFIG_GENERIC_IOMAP) += iomap.o

For each architecture using the generic IOMAP functionality we would see:

config X86
    select ...
    select HAVE_GENERIC_IOMAP
    select ...

Note: we use the existing config option and avoid creating a new
config variable to select HAVE_GENERIC_IOMAP.

Note: the use of the internal config variable HAVE_GENERIC_IOMAP, it is
introduced to overcome the limitation of select which will force a
config option to 'y' no matter the dependencies.
The dependencies are moved to the symbol GENERIC_IOMAP and we avoid the
situation where select forces a symbol equals to 'y'.

Build as module only
```
为了限制一个部件只能编译成module，指定它的配置符号 "depends on m".  例如:

```
config FOO
    depends on BAR && m


limits FOO to module (=m) or disabled (=n).
```

参考文献
--------
[kconfig基本语法](http://blog.csdn.net/taoshengyang/article/details/5604216)
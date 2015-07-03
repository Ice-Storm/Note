Overview in OpenGL
===================
[TOC]

OpenGL是一个图形接口标准，以下的一些介绍可能把标准和实现混用，但并不妨碍对OpenGL的大致理解。

OpenGL早期使用的是固定管线，目前基本抛弃了固定管线，全面使用可编程管线，因此很多早期的API都已经没有用了，像glTranslate这类函数已经作用不大，glBegin、glVertex、glEnd更是早就被抛弃了，可是网上的资料还是很多讲这类函数的，诚然学习这些早期API对理解OpenGL的工作方式有一定的帮助，但是必须在这些例子里说明使用是固定管道编程方式，用的是固定管道的API，否则和可编程管道同时存在时很容易产生迷惑，比如这些API和可编程管道如何共存。

#OpenGL版本
OpenGL版本经历了多次演化，从1.0到4.0，每个版本都提供了新的API，也提供了对之前版本API的一定的兼容性，但随之带来的就是API的数目越来越多，因此OpenGL还推出了Core版本，只包含当前版本的基本API，精简了API的数目和使用，提高了程序的稳定性。

随着嵌入式终端的增加，OpenGL还推出了嵌入式版本OpenGL ES，这是一个OpenGL的子集，
从OpenGL裁剪定制而来的，去除了glBegin/glEnd，四边形（GL_QUADS）、多边形（GL_POLYGONS）等复杂图元等许多非绝对必要的特性。

OpenGL1.0支持固定管线，OpenGL ES 2.0针对可编程管线，而较新的OpenGL ES 3.0的支持设备相对来说还不是那么广泛。因此从可移植角度来考虑，使用OpenGL ES 2.0是一个较好的选择。

OpenGL ES 2.0参照OpenGL2.0规范定义，common profile发布于2005-8，OpenGL ES 3.0于2012年公布，加入了大量的新特性，OpenGL还有一个safety-critical profile。
##OpenGL Q&A

Q：OpenGL已经落伍了，更新的也非常的慢，再努力几年也赶不上技术雄厚的Direct3D。
A：近几年Khronos Group接手OpenGL之后，发展速度迅猛，新版本的OpenGL已经更新到了OpenGL 4.4，其功能略超过Direct3D 11，且被Nvidia和AMD主流显卡全面支持；值得注意的是有96.8%手持设备都只使用桌面OpenGL的子集OpenGL ES作为他们的图形编程接口；许多家用游戏机也使用OpenGL作为其图形的编程接口。OpenGL已经重新回到主流的地位，我想或许你的教科书真的是太老了！

Q：OpenGL的功能会比Direct3D少，且OpenGL的速度不如Direct3D来得快。
A：PC上的OpenGL和Direct3D工作在同样的硬件上，他们的功能是基本一致的，另外你应该看看这个。
 
Q：从哪里才能下载到OpenGL的SDK？
A：OpenGL并没有SDK，想要启用高级OpenGL都是通过获取相应的函数指针来完成的，当然必须由显卡的驱动支持才行。不过有些库可以帮你完成这类繁琐的工作，比如GLEW。

Q：OpenGL的扩展是什么？
A：OpenGL功能的实现都是靠一个个扩展实现的，如果实现了OpenGL版本规范规定的扩展，那么就是实现了相应的OpenGL扩展。

Q：我如何知道我的设备支持了多少OpenGL扩展以及什么OpenGL扩展？
A：在编程中你可以使用特定的库比如GLEW检测相应的扩展是否被支持；你也可以下载OpenGL Extensions Viewer直观的查看支持的OpenGL的特性和扩展，这个软件也有多个平台的版本。 

Q：感觉OpenGL的文档都太不详细了，我在搜索引擎里搜索的结果都很令人失望。
A：详细的OpenGL文档都在其官网里：①OpenGL Registry里面有上百个OpenGL扩展的文档；②OpenGL Reference Page里面有各个函数的使用方法；③OpenGL Reference Card能帮助你宏观地了解OpenGL的所有主要函数；④OpenGL Specification其实是扩展文档的集合，不过也是非常的详细和有用。

Q：什么是Core Profile和Compatibility Profile？
A：在OpenGL的发展历程中，总是兼顾向下兼容的特性，但是到了一定的程度之后，这些旧有的OpenGL API不再适应时代的需要，还有一些扩展并不是驱动一定要实现的扩展，这些被统一划入可选的Compatibility Profile；而由OpenGL规范规定必须支持的扩展，则是Core Profile，想要支持先进的OpenGL，相应的Core Profile扩展必须被实现。

Q：有什么好的入门书籍可以介绍吗？
A：《OpenGL Superbible》和《OpenGL Shading Language Cookbook》以及《OpenGL Insights》都非常的不错。

Q：OpenGL如何进行Debug，DirectX的PIX真的很好用呢。
A：现在支持GLSL和OpenGL跟步调试的只有Nvidia的Nsight，只支持Nvidia的显卡；其他的基本都是track，不支持GLSL的跟步调试，比如AMD的GPUPerfClient以及gDEBugger。还有AMD的GPU ShaderAnalyzer也非常的不错，能看到相应的GLSL汇编代码。

Q：OpenGL有多少引擎支持呢！
A：基本主流的引擎都会在上层抽象一层，然后都有用OpenGL和Direct3D分别实现的模块；绝大部分的主流引擎都留有了OpenGL的实现。


#GLSL版本
不同的OpenGL版本支持不同的GLSL版本。
|-|-|
|OpenGL|GLSL|
|2.0|1.1|
|2.1|1.2|
|3.0|1.3|
|3.1|1.4|
|3.2|1.5|
|3.3|3.3|
|4.0|4.0|

可以发现OpenGL从3.3开始版本号和GLSL同步，方便了版本的记忆。

#API分类
OpenGL APL分为三类，分别为gl，glu和glut开头，其中gl开头的API是OpenGL的基本API，提供了OpenGL的所有基本功能，glu（OpenGL Utility）提供了一些常用功能的封装，都是利用gl函数实现的，glut（OpenGL Utility Tools）提供了一些工具函数和窗口函数，方便OpenGL在不同系统间移植。


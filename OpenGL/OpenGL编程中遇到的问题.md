OpenGL编程中遇到的问题
====================
[TOC]

QT
---
Qt为OpenGL提供了很多封装函数，方便了OpenGl代码的编写同时也引入了很多问题，让初学者者不知所措，这里简单对我遇到的问题进行记录，方便日后查找

#Qt下OpenGL开发流程
Qt为OpenGL提供了QGLWidget和QOpengGLWidget两个控件，方便OpenGL的绘制。在这些控件中需要注意三个接口函数，分别是
- initializeGL()

    注册函数，在此设置GL的渲染绘制属性、定义显示列表、载入固定纹理等初始化工作。在initializeGL()在调用paintGL()之前只被调用一次，之后不再调用。

- resizeGL(int width, int height)

    paintGL()第一次调用之前，initializeGL()调用之后被第一次被调用， 之后每当QGLWidget的不见大小发生改变时，都将调用该函数来对视图、投影矩阵等进行相应的设置。

- paintGL()

    绘制函数，在此使用OpenGL中的接口进行场景绘制，QGLWidget的paintEvent( QPaintEvent* )将会自动调用 paintGL()进行部件的显示绘制。也可在需要重绘时通过updateGL()时调用paintGL()。

三个，只要完成这三个接口，OpenGL控件就能自动完成图像的绘制和显示。
>注意：使用Qt的OpenGL函数接口类时，需要使用initializeOpenGLFunctions()函数进行初始化。

#OpenGL开发容易遇到的错误
##参数错误
OpenGL进入可编程管线开发时代以来，需要记忆的API数量已经减少了很多，大部分工作已经移到的Shader上进行，尽管如此，那少部分的API还是有可能出错，比如glBindBuffer(GL_ARRAY_BUFFER, &m_vbo)中的GL_ARRAY_BUFFER错用成GL_VERTEX_ARRAY,编译时并不会报错，甚至运行时也不会报错，但是没有图像，而且在调用函数glVertexAttribPointer()时，最后一个pointer参数设置成NULL时，有可能会造成程序崩溃，因为程序之前并没有创建正确的Buffer，这里对它的引用就可能造成错误。

##顶点错误
有时代码无法产生图像，无论如何也找不出原因，那有可能是顶点数据有问题，无法渲染出正确的图像

##QMatrix
Qt提供了方便的QMatrix类进行矩阵变换，但是需要注意的是Qt的矩阵默认是以行主序的，而OpenGL的矩阵是以列主序的，因此在它们之间传输数据时需要注意转换。

##QUAD
OpenGL ES 2.0中只支持三角形等简单多边形，并不支持四边形，因此使用GL_QUADS并不能得到正确的结果。

##z为1的三角形不显示
定义了一个简单的三角形，z为1时没有图像，当z小于1时有图像，注意如果在GLSL中没有进行任何变换，也就是输入z是1，输出z还是1，那么生成的图形在规范视见体外面,规范视见体：

    x +- 1
    y +- 1
    z +- 1


##OpenGL API中出现段错误
有可能是GLSL中访问了没有被赋值的变量，或者向API传输了本地变量地址，而API需要的是服务器段的数据地址。

#多个VBO绑定一个属性索引
绘制多个子图形时，想每个图形都用一个vbo，绑定相同的属性索引，绘制相应图形时enable相应的vbo，但是事实是只能画出最后设置的vbo图形，猜测属性索引只能绑定一个vbo。


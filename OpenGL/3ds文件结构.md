3ds文件结构
==========
[TOC]

|-|-|-|
|Offset|Length|Name|
|0  |2  |Chunk-ID|
|2  |4  |Chnk-length = 6+n+m|
|6  |n  |Data|
|6+n|m  |Sub-chunks|

#1、读取规则 3ds文件的读取规则
字节：直接读取；
字：先读低位字节，后读高位字节，如ed 3c读出后的字为3c ed；
双字：先读低位字，后读高位字，如ed 3c 25 43读出后的双字为43 25 3c ed；
浮点数：直接读取四个字节。

#2、CHUNK
chunk是3ds文件的基本构成单位。每一个chunk包括一个头和一个主体。chunk是相互嵌套的，这就决定了你必须以递归的方式读取它们。chunk的头又由两部分组成：ID长一个字，chunk的长度（以字节为单位，包括头）长一个双字。ID表示chunk的含义。事实上有上千个chunk，它们构成了一个复杂但灵活的文件系统，你不需要知道所有的就可以顺利的读完整个文件。我基本搞清楚的chunk有：

根（0x4D4D）
|
|--编辑器主chunk(0x3D3D)，包含网格信息、灯光信息、摄像机信息和材质信息。
|      |-网格主chunk(0x4000)，包含了所有网格。
|            |-网格信息(0x4100)，包含网格名称、顶点、面、纹理坐标等。
|               |-顶点信息（0x4110），顶点个数（字）顶点坐标（三个浮点数x、y、z）
|               |-面信息（0x4120），面个数（字）顶点索引（三个字一个索引1、2、3）
|               |-与网络相关的材质信息（0x4130）
|               |-纹理坐标（0x4140）
|               |-转换矩阵（0x4160）
|--材质信息(0xaaff)
|       |-材质名称（0xa000）
|       |-满射色（0xa020）
|       |-纹理帖图（0xa200）
|            |-帖图名称 （0xa300）
|--关键帧（0xB000）
        |-关键帧的起点和终点（0xB008）
        |-网格的关键帧信息（0xB002）
            |-关键帧的层次信息（0xB010）
            |-关键帧的Duymmy（0xB011）
            |-支点坐标（0xB013）
            |-移动的关键帧信息（0xB020）
            |-转动的关键帧信息（0xB021）
            |-缩放的关键帧信息（0xB022）
            |-关键帧的索引（0xB030）

|——任何可能的chunk
        |-浮点数格式的颜色（0x0010）
        |-字节格式的颜色（0x0011）
        |-字节格式的gamma矫正（0x0012）
        |-浮点格式的gamma矫正（0x0013）
        |-字格式的百分比（0x0030）
        |-浮点数格式的百分比（0x0031）

##0x4D4D：根chunk，每一个3ds文件都起自它，它的长度也就是文件的长度。它包含了两个chunk：编辑器，和关键帧。
父chunk：无
子chunk：0x3D3D、0xB000
长度：头长度+子chunk长度
内容：无


##0x3D3D：编辑器主chunk，它包含有：网格信息、灯光信息、摄象机信息和材质信息。
父chunk：0x4D4D
子chunk：0x4000、0xafff
长度：头长度+子chunk长度
内容：无


##0x4000：网格主chunk，它包含了所有的网格。
父chunk：0x3D3D
子chunk：0x4100
长度：头长度+子chunk长度+内容长度
内容：名称（以空字节结尾的字符串）


##0x4100：网格信息，包含网格名称、顶点、面、纹理坐标等。
父chunk：0x4000
子chunk：0x4110、0x4120、0x4140、0x4160
长度：头长度+子chunk长度
内容：无


##0x4110：顶点信息。
父chunk：0x4100
子chunk：无
长度：头长度+内容长度
内容：顶点个数（一个字）顶点坐标（三个浮点数一个坐标x、y、z，个数*3*浮点数）


##0x4120：面信息。
父chunk：0x4100
子chunk：0x4130
长度：头长度+子chunk长度+内容长度
内容：面个数（一个字）顶点索引（三个字一个索引1、2、3，个数*3*字）


##0x4130：与网格相关的材质信息。
父chunk：0x4120
子chunk：无
长度：头长度+内容长度
内容：名称（以空字节结尾的字符串）与材质相连的面的个数（一个字）与材质相连的面的索引（个数*字）


##0x4140：纹理坐标。
父chunk：0x4100
子chunk：无
长度：头长度+内容长度
内容：坐标个数（一个字）坐标（两个浮点数一个坐标u、v，个数*2*浮点数）
 

##0x4160：转换矩阵。
父chunk：0x4100
子chunk：无
长度：头长度+内容长度
内容： x轴的向量（三个浮点数u、v、n） y轴的向量（三个浮点数u、v、n） z轴的向量（三个浮点数u、v、n）源点坐标（三个浮点数x、y、z）


##0xafff：材质信息。
父chunk：0x4D4D
子chunk：0xa000、0xa020、0xa200
长度：头长度+子chunk长度
内容：无


##0xa000：材质名称。
父chunk：0xafff
子chunk：无
长度：头长度+内容长度
内容：名称（以空字节结尾的字符串）

 
##0xa020：满射色。
父chunk：0xafff
子chunk：0x0011、0x0012
长度：头长度+子chunk长度
内容：无

 
##0xa200：纹理帖图。
父chunk：0xafff
子chunk：0xa300
长度：头长度+子chunk长度
内容：无
 

##0xa300：帖图名称。
父chunk：0xa200
子chunk：无
长度：头长度+内容长度
内容：名称（以空字节结尾的字符串）


##0xB000：关键帧主chunk，包含所有的关键帧信息。
父chunk：0x4D4D
子chunk：0xB008、0xB002
长度：头长度+子chunk长度
内容：无
 

##0xB008：关键帧的起点和终点。
父chunk：0xB000
子chunk：无
长度：头长度+内容长度
内容：起始帧（一个双字）结尾帧（一个双字）


##0xB002：网格的关键帧信息。
父chunk：0xB000
子chunk：0xB010、0xB011、0xB013、0xB020、0xB021、0xB022、0xB030
长度：头长度+子chunk长度
内容：无


##0xB010：关键帧的层次信息，包括名称和上一级关键帧的索引，名称与它指向的网格名称一致。
父chunk：0xB002
子chunk：无
长度：头长度+内容长度
内容：名称（以空字节结尾的字符串）两个未知的字上一级关键帧的索引（一个字）

 
##0xB011：关键帧的dummy名称，我不知道dummy在这里的具体含义，但只要你在上一个chunk中读到的名称是“$$$DUMMY”那么你就要到这里来读它真正的名称。因为这说明它指向的不是网格而是虚拟的组。

父chunk：0xB002
子chunk：无
长度：头长度+内容长度
内容：名称（以空字节结尾的字符串）
 

##0xB013：支点坐标。
父chunk：0xB002
子chunk：无长度：头长度+内容长度
内容：三个浮点数x,y,z


##0xB020：移动的关键帧信息。
父chunk：0xB002
子chunk：无
长度：头长度+内容长度
内容：五个未知的字帧个数（一个字）一个个数那么多的循环结构{ 帧索引（一个字）一个未知的双字移动的向量（三个浮点数x,y,z） }

 
##0xB021：转动的关键帧信息。
父chunk：0xB002
子chunk：无
长度：头长度+内容长度
内容：五个未知的字帧个数（一个字）一个个数那么多的循环结构{ 帧索引（一个字）一个未知的双字转动角度（一个浮点数）绕之转动的向量（三个浮点数x,y,z） }
 

##0xB022：缩放的关键帧信息。
父chunk：0xB002
子chunk：无
长度：头长度+内容长度
内容：五个未知的字帧个数（一个字）一个个数那么多的循环结构{ 帧索引（一个字）一个未知的双字伸缩的向量（三个浮点数x,y,z） }

 
##0xB030：关键帧的索引。
父chunk：0xB002
子chunk：无
长度：头长度+内容长度
内容：关键帧的索引（一个字）


以下的chunk可能出现在任何chunk中：
 

##0x0010：浮点数格式的颜色。
父chunk：任何可能的chunk
子chunk：无
长度：头长度+内容长度
内容：颜色（三个浮点数red,green,blue）

 

##0x0011：字节格式的颜色。
父chunk：任何可能的chunk
子chunk：无
长度：头长度+内容长度
内容：颜色（三个字节red,green,blue）
 

##0x0012：字节格式的gamma矫正。
父chunk：任何可能的chunk
子chunk：无
长度：头长度+内容长度
内容：颜色（三个字节red,green,blue）


##0x0013：浮点数格式的gamma矫正。
父chunk：任何可能的chunk
子chunk：无
长度：头长度+内容长度
内容：颜色（三个浮点数red,green,blue）
 

##0x0030：字格式的百分比。
父chunk：任何可能的chunk
子chunk：无
长度：头长度+内容长度
内容：百分比（一个字0~100）

 
##0x0031：浮点数格式的百分比。
父chunk：任何可能的chunk
子chunk：无
长度：头长度+内容长度
内容：百分比（一个浮点数0~100）

#块存储
3ds文件是基于“块”存储的，这些块描述了诸如场景，每个编辑窗口(Viewport)的状态，材质，网格对象等等数据。
##1、3DS块的组织方式

    　　  MAIN3DS (0x4D4D)    //基本信息块
    　　 |
    　　  +--VERSION (0x0002) //版本信息块
    　　  |
    　　 +--EDIT3DS (0x3D3D)  //编辑信息块
    　　 | |
    　　 | +--EDIT_MATERIAL (0xAFFF)  //材质
    　　 | | |
    　　 | | +--MAT_NAME01 (0xA000) //材质名称
    　　 | | +--MAT_AMBCOL (0xA010) //环境色
    　　 | | +--MAT_DIFCOL (0xA020) //漫射色
    　　 | | +--MAT_SPECOL (0xA030) //反射色
    　　| | +--MAT_SHININESS (0xA040) //亮度
    　　| | +--MATMAP (0xA200) //材质的纹理？？？？？ 
    　　| | +--MATMAPFILE (0xA300) //保存纹理的文件名
    　　 | |
    　　 | +--EDIT_CONFIG1 (0x0100)   //配置信息1
    　　 | +--EDIT_CONFIG2 (0x3E3D) //配置信息2
    　　 | +--EDIT_VIEW_P1 (0x7012)   //视窗1
    　　 | | |
    　　 | | +--TOP (0x0001) //顶视图
    　　 | | +--BOTTOM (0x0002) //底视图
    　　 | | +--LEFT (0x0003) //左视图
    　　 | | +--RIGHT (0x0004) //右视图
    　　 | | +--FRONT (0x0005) //前视图
    　　 | | +--BACK (0x0006) //后视图
    　　 | | +--USER (0x0007) //用户自定义
    　　 | | +--CAMERA (0xFFFF) //相机
    　　 | | +--LIGHT (0x0009) //灯光
    　　 | | +--DISABLED (0x0010) //禁用
    　　 | | +--BOGUS (0x0011) //虚拟
    　　 | |
    　　 | +--EDIT_VIEW_P2 (0x7011)   //视窗2
    　　 | | |
    　　 | | +--TOP (0x0001) //顶视图
    　　 | | +--BOTTOM (0x0002) //底视图
    　　 | | +--LEFT (0x0003) //左视图
    　　 | | +--RIGHT (0x0004) //右视图
    　　 | | +--FRONT (0x0005) //前视图
    　　 | | +--BACK (0x0006) //后视图
    　　 | | +--USER (0x0007) //用户自定义
    　　 | | +--CAMERA (0xFFFF) //相机
    　　 | | +--LIGHT (0x0009) //灯光
    　　 | | +--DISABLED (0x0010) //禁用
    　　 | | +--BOGUS (0x0011) //虚拟
    　　 | |
    　　 | +--EDIT_VIEW_P3 (0x7020)   //视窗3
    　　 | +--EDIT_VIEW1 (0x7001) //视图
    　　 | +--EDIT_BACKGR (0x1200) //背景
    　　 | +--EDIT_AMBIENT (0x2100)   //环境
    　　 | +--EDIT_OBJECT (0x4000)    //对象（包括面、点等信息）
    　　 | | |
    　　 | | +--OBJ_TRIMESH (0x4100) //三角形网格对象
    　　 | | | |
    　　 | | | +--TRI_VERTEX (0x4110) //顶点
    　　 | | | +--TRI_VERTEXOPTIONS (0x4111) //顶点选项
    　　 | | | +--TRI_MAPPINGCOORS (0x4140) //纹理映射坐标
    　　 | | | +--TRI_MAPPINGSTANDARD (0x4170) //标准映射
    　　 | | | +--TRI_FACEL1 (0x4120) //面
    　　| | | +--TRI_SMOOTH (0x4150) //
    　　 | | | +--TRI_MATERIAL (0x4130) //材质名称
    　　 | | | +--TRI_LOCAL (0x4160) //
    　　 | | | +--TRI_VISIBLE (0x4165) //可见与否
    　　 | | |
    　　 | | +--OBJ_LIGHT (0x4600)    //灯光
    　　 | | | |
    　　 | | | +--LIT_OFF (0x4620)
    　　 | | | +--LIT_SPOT (0x4610)
    　　 | | | +--LIT_UNKNWN01 (0x465A) //未知块
    　　 | | | 
    　　 | | +--OBJ_CAMERA (0x4700)
    　　 | | | |
    　　 | | | +--CAM_UNKNWN01 (0x4710) //未知块
    　　 | | | +--CAM_UNKNWN02 (0x4720) //未知块
    　　 | | |
    　　 | | +--OBJ_UNKNWN01 (0x4710) //未知块
    　　 | | +--OBJ_UNKNWN02 (0x4720) //未知块
    　　 | |
    　　 | +--EDIT_UNKNW01 (0x1100) //未知块
    　　 | +--EDIT_UNKNW02 (0x1201) //未知块
    　　 | +--EDIT_UNKNW03 (0x1300) //未知块
    　　 | +--EDIT_UNKNW04 (0x1400) //未知块
    　　 | +--EDIT_UNKNW05 (0x1420) //未知块
    　　 | +--EDIT_UNKNW06 (0x1450) //未知块
    　　 | +--EDIT_UNKNW07 (0x1500) //未知块
    　　 | +--EDIT_UNKNW08 (0x2200) //未知块
    　　 | +--EDIT_UNKNW09 (0x2201) //未知块
    　　 | +--EDIT_UNKNW10 (0x2210) //未知块
    　　 | +--EDIT_UNKNW11 (0x2300) //未知块
    　　 | +--EDIT_UNKNW12 (0x2302) //未知块
    　　 | +--EDIT_UNKNW13 (0x2000) //未知块
    　　 | +--EDIT_UNKNW14 (0xAFFF) //未知块
    　　 |
    　　 +--KEYF3DS (0xB000)  //关键帧信息块
    　　 |
    　　 +--KEYF_UNKNWN01 (0xB00A) //未知块
    　　 +--EDIT_VIEW1 (0x7001) //视图
    　　 +--KEYF_FRAMES (0xB008)  //帧
    　　 +--KEYF_UNKNWN02 (0xB009) //未知块
    　　 +--KEYF_OBJDES (0xB002) //对象描述？？？
    　　 |
    　　 +--KEYF_OBJHIERARCH (0xB010) //层级
    　　 +--KEYF_OBJDUMMYNAME (0xB011) //虚拟体名称
    　　 +--KEYF_OBJUNKNWN01 (0xB013) //未知块
    　　 +--KEYF_OBJUNKNWN02 (0xB014) //未知块
    　　 +--KEYF_OBJUNKNWN03 (0xB015) //未知块
    　　 +--KEYF_OBJTRANSLATE (0xB020) //偏移
    　　 +--KEYF_OBJROTATE (0xB021) //旋转
    　　 +--KEYF_OBJSCALE (0xB022) //缩放
    　　另外还有一些块是在整个文件中都会经常出现的，那就是颜色块
    　　COL_RGB   0x0010  //RGB色彩模式，以float存放3个分量
    　　COL_TRU   0x0011  //真彩色模式，以char存放3个分量
    　　COL_UNKNOWN 0x0013    //未知块
    　　SHI_PER 0x0030 //百分比亮度

3ds文件中数据的存储方式是Intel式的，也就是说是高位放在后面，低位放在前面。比如：网格对象块的块头ID：0x4000在文件里是以00 40存放的，对于windows程序员来说，无需做任何转换。
　　按3ds文件的划分方式，有一个块总是位于整个文件的最开始，是其他所有块的根块，我们称之为主块或基本信息块（MAIN3D块）。主块下包含两个块，他们是一级子块：一个描述场景数据的主编辑块和一个描述关键帧数据的关键帧块。相对于关键帧块，主编辑块对我们更重要。它包含了场景中使用的材质（纹理是材质的一部分），配置，视口的定义方式，背景颜色，物体的数据等等一系列数据，可以说他就表示了我们当前编辑场景的状况和当前窗口的配置数据。
　　主编辑块的子块虽然是按照一定的次序存放，但其中有些块并不是一定存在的（比如：如果你没有定义材质，使用缺省材质，这里将不存在材质块）。材质块定义了使用于物体上的材质的属性，包括:材质名称,环境色,漫射色,反射色,亮度,材质的纹理及保存纹理的文件名，其中材质名称是一字符串，环境色、漫射色、反射色是颜色块。然后是网格对象块，其包含了大部分我们所关心的物体的几何数据以及灯光、相机等相关信息。

##2、基本块的数据结构及读取方式
　　每个块都包含一个块头：块ID+块长度，紧跟着块头便是相应的数据了。以一个最基本的块TRI_VERTEXL(0x4110)顶点块为例，在文件中其存储形式如图：
　　如此可见，块头包括ID和Size两项，共占6位，Size指得是整个块的长度，而不是数据的长度，一定要注意了。所以读一个顶点块的代码可写为：
```c
　　ReadChunckHeader(&CH);    //读入一个块头信息
　　switch(CH.ChunckID){      //判断块的类型
　　   //……
　　case TRI_VERTEXL:         //是对象的顶点块
　　  p3DObject->NumVerts = ReadInt();//获得顶点的总数目
　　  p3DObject->pVertices = ::new CVertex[p3DObject->NumVerts]; //分配足够空间
　　  if(!p3DObject->pVertices)
　　  AfxMessageBox( "Error Allocating Memory");
　　  for(i = 0; i < p3DObject->NumVerts; i++)//逐个顶点读入其三维坐标值
　　  {   
　　  fread(&p3DObject->pVertices[i].x, 4, 1, m_3dsFile);
　　  fread(&p3DObject->pVertices[i].y, 4, 1, m_3dsFile);
　　  fread(&p3DObject->pVertices[i].z, 4, 1, m_3dsFile);
　　  }
　　}
```
　　而要跳过一个块的代码可写为：（两种方法是等价的）
```c
　　//方法1：  
fseek(m_3dsFile, -6, SEEK_CUR);//文件指针后退6位
fseek(m_3dsFile, CH.ChunckSize, SEEK_CUR);//跳过块的长度
　　//方法2： 
fseek(m_3dsFile, CH.ChunckSize-6, SEEK_CUR);
```

##3、块的层级结构及读取方式
　　3ds文件格式并不是一些基本的块堆积而成的，而是一个层级结构，基本块是一个文件必须有的，处于顶级，主块有版本信息块、编辑信息块和关键帧信息块，编辑信息块中的一级块又包括材质信息块、对象信息块等等。对象信息块中的二级块包括网格对象信息块、灯光信息块、相机信息等。网格对象信息块中的三级信息块包括顶点信息、面信息、材质名称、映射坐标等。所以说，3ds文件是一个复杂而有序的整体，若从基本块开始讲起，那就得绘出整个文件了，呵呵，这样一个浩大的工程留给比较有耐心的你吧。现在从EDIT_OBJECT开始，我们来分析一下网格对象块中数据的读取问题。
　　如图所示Data22是EDIT_OBJECT块的数据，Size22等于Data22+6 {注：ID号是int型2位，Size22是long型4位}，在Data22中包含三级子块，其中一个三级子块是OBJ_TRIMESH，对应的数据是Data31,Size31等于Data31+6,同理在Data31中包含一系列四级子块，TRI_VERTEX是其中的一个子块，而且TRI_VERTEX是一个基本块，不能再往下细分。Data41中存储的是顶点的坐标值。例如，网格对象中一共有100个顶点，Data41等于100*4=400位{注：顶点三级坐标是以float存储的，故为4位}，所以Size41等于Data41+6=406,代表了整个TRI_VERTEX的长度{注：包括ID号和Size41本身}。
　
　　
　　块长编号设为：
　　MAIN3DS(0x4D4D) Size00
　　|
　　+--VERSION(0x0002) Size11
　　+--EDIT3DS(0x3D3D) Size12 
　　| |
　　| +--EDIT_MATERIAL(0xAFFF) Size21
　　| +--EDIT_OBJECT(0x4000) Size22
　　| | |
　　| | +--OBJ_TRIMESH(0x4100) Size31
　　| | | |
　　| | | +--TRI_VERTEX(0x4110) Size41
　　| | | +--TRI_VERTEXOPTIONS(0x4111) Size42
　　| | | +--…… 
　　所以，我们如果要读入网格对象的顶点坐标，可以用一个switch块来逐级判断，找到TRI_VERTEX块，然后将其数据Data41读入到我们的自定义数据结构中。
　　ReadChunckHeader(&CH);    //读入一个块头信息
　　switch(CH.ChunckID) //判断块的类型
　　{ ……
　　case EDIT_OBJECT: //是网格对象块
　　  ObjectName = ReadName();    //获得对象的名称
　　  ObjectFound = 2;    //置计数为2，意味着要读出对象的面信息和顶点信息2个块
　　  Success= true; //成功标识
　　  delete[] ObjectName;    //清空字符串用于下一个对象的读取
　　  ObjectName = NULL;  
　　  break;  //跳出循环读下一个块头
　　case TRI_VERTEXL: //是对象的顶点块
　　if(ObjectFound)   //计数不为0
　　{ 
　　  ObjectFound--;  //将计数减一
　　  p3DObject->NumVerts = ReadInt();    //获得顶点的总数目
　　  p3DObject->pVertices = ::new CVertex[p3DObject->NumVerts];  //分配足够空间
　　  if(!p3DObject->pVertices)
　　  AfxMessageBox("Error Allocating Memory");
　　  for(i = 0; i < p3DObject->NumVerts; i++)    //逐个顶点读入其三维坐标值
　　  {   
　　  fread(&p3DObject->pVertices[i].x, 4, 1, m_3dsFile);
　　  fread(&p3DObject->pVertices[i].y, 4, 1, m_3dsFile);
　　  fread(&p3DObject->pVertices[i].z, 4, 1, m_3dsFile);
　　  }
　　}
　　else  //计数为0时将跳过此顶点块，跳过一基本块的方法在上一节有介绍
　　{
　　  fseek(m_3dsFile, -6, SEEK_CUR);
　　  fseek(m_3dsFile, CH.ChunckSize, SEEK_CUR);
　　}
　　break;    //跳出循环读下一个块头
　　……
　　}
　　
　　结论：虽然说Autodesk公司并没有发布官方的3ds文件的文档，但是从网上收集的资料来看，我们完全可以将我们所关心的数据读入到自定义的数据结构中，然后利用OpenGL强大的图形函数库将它绘制出来。以上是一篇入门文档，只对其原理和数据块的读取做了一个简单的介绍，如果你有更高的要求可以参考以下几篇文档：
　　[1]《3DS文件结构(.3ds)》——作者：Martin van Velsen 翻译：樱
　　[2]《The Unofficial 3DStudio 3DS File Format》——作者：Jeff Lewis
　　[3]《从3DS文件中导入网格数据》——作者：故乡的云

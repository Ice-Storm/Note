OpenGL光照（固定管线）
==========

OpenGL的传统Fixed Function Pipeline中，支持4种不同的光源，分别是方向光Directional Light、点光源Point Light、聚光灯Spot Light，以及环境光Ambient Light。
OpenGL中的光照以百分比形式表示。

#为图元指定法向量

OpenGL必须通过图元的法线向量来确定图元的明暗程度
通过计算得到法线向量后，我们需要在绘制顶点前调用glNormal函数为顶点或图元指定法

使用glTranslate*函数或者glRotate*函数可以改变物体的外观，但法线向量并不会随之改变。然而，使用glScale*函数，对每一坐标轴进行不同程度的缩放，很有可能导致法线向量的不正确，虽然OpenGL提供了一些措施来修正这一问题，但由此也带来了各种开销。因此，在使用了法线向量的场合，应尽量避免使用glScale*函数。即使使用，也最好保证各坐标轴进行等比例缩放

对光源进行平移或旋转，使之相对于静止的物体移动，这可以在指定模型变换后设置光源位置，然后通过修改模型变换来改变光源的位置。

#设置光照
1.设置一个或多个光源，设定它的有关属性；
2.选择一种光照模型；
3.设置物体的材料属性。

##设置光源
###光源种类
1. 方向光Directional Light（平行光，镜面光）
简单地说，就是只具有方向和颜色属性的光源，它常被用来模拟太阳，计算太阳的光线时简化成只有方向属性，忽略距离的因素。

2. 点光源Point Light
具有位置和颜色属性，它在空间中占据一个点，并向四面八方散射。光线照到某个物体后，反射光的强度与物体表面的法线和入射光线的夹角有关，这点和方向光类似。不同的是，点光源具有位置属性，所以光线到每个顶点的方向和距离都不同，并且它还会光源随着物体的距离的增大而衰减。点光源在自然界中并不存在，自然界中的光源不可能只是一个点，它一定会呈某种形状，而且都有体积。

3. 聚光灯Spot Light
聚光灯同事具有了方向、位置、颜色这些属性，还需要指定光柱圆锥的发射角度，落在光柱中偏外的物体所得的光线强度会比较弱：完全落在光柱外的物体则接受不到光线。聚光灯的其他属性和点光源相同，光线同样会随着距离的增大而衰减，反射强度同样会随着光线入射角的改变而改变。

4. 环境光Ambient Light
现实世界中，光线会在不同的物体表面间反射，这种通过反射得到的光源，很难把它们轨道前三种光源中的一种。但是这一类光源通常无法忽略，如果直接忽略的话，光照结果会太暗。
在Fixed Function Pipeline中，处理这一类因为反射而得到的光源的最简单的方法就是再加一入一个环境光Ambient Light。环境光没有位置，也没有方向，仅仅提供了一个基本的光源强度。让物体在没有直接被三种光源的任何一种光照到时，还能得到一个最基本的亮度。环境光是用来模拟通过反射所得到的间接光源，否则有些物体可能会因为太暗而看不到。

这种通过反射所得的光源，在3D绘图中被称为Global Illumination或者Indirect Illumination;不是通过反射，而是直接照射的光源，被称为Direct Illumination。使用环境光是解决Global Illumination最简单的方法。

####创建聚光灯（这些属性只对位置性光源有效）
```c
glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, LightCutOff);
```
GL_SPOT_DIRECTION、GL_SPOT_EXPONENT、GL_SPOT_CUTOFF属性。

表示将光源作为聚光灯使用。很多光源都是向四面八方发射光线，但有时候一些光源则是只向某个方向发射，比如手电筒，只向一个较小的角度发射光线。

- GL_SPOT_DIRECTION 属性有三个值，表示一个向量，即光源发射的方向。光源的默认方向是(0.0,0.0,-1.0),即指向z轴负方向

- GL_SPOT_EXPONENT  属性只有一个值，表示聚光的程度，为零时表示光照范围内向各方向发射的光线强度相同，为正数时表示光照向中央集中，正对发射方向的位置受到更多光照，其它位置受到较少光照。数值越大，聚光效果就越明显。

- GL_SPOT_CUTOFF    属性也只有一个值，表示一个角度，它是光源发射光线所覆盖角度的一半，其取值范围在0到90之间，也可以取180这个特殊值。取值为180时表示光源发射光线覆盖360度，即不使用聚光灯，向全周围发射。即一个点光源。

###光的成份
对于每一种光源，都有漫射光和平行光两种成分。在OpenGL中，环境光也被作为一种特殊的光源的成分来看待。漫射光是指在光源中能够被漫反射的光的颜色成分(白色则包含所有颜色)，而平行光是指光源中所有能够被镜面反射的光的颜色成分。通过指定这两种成分的颜色，就能决定光源是平行光源还是点光源。
####设置光线衰减系数
```c
glLightf(GL_LIGHT0,AttenuationWay,SpotAttenuation);
```
AttenuationWay可以取以下几个值：

- GL_CONSTANT_ATTENUATION -- 表示光线按常熟衰减(与距离无关)
- GL_LINEAR_ATTENUATION -- 表示光线按距离线性衰减
- GL_QUADRATIC_ATTENUATION -- 表示光线按距离以二次函数衰减。
参数 SpotAttenuation为光线的衰减系数。

GL_CONSTANT_ATTENUATION、GL_LINEAR_ATTENUATION、GL_QUADRATIC_ATTENUATION属性。这三个属性表示了光源所发出的光线的直线传播特性。现实生活中，光线的强度随着距离的增加而减弱，OpenGL把这个减弱的趋势抽象成函数：

衰减因子 = 1 / (k1 + k2 * d + k3 * k3 * d)

其中d表示距离，光线的初始强度乘以衰减因子，就得到对应距离的光线强度。k1, k2, k3分别是GL_CONSTANT_ATTENUATION,GL_LINEAR_ATTENUATION,GL_QUADRATIC_ATTENUATION。通过设置这三个常数，就可以控制光线在传播过程中的减弱趋势。

###设置光源成分
OpenGL可以同时为我们提供8个有效的光源。也就是说，我们最多可以同时启用8个光源，分别是GL_LIGHT0~GL_LIGHT7，其中，GL_LIGHT0是最特殊的一个光源。我们可以为GL_LIGHT0指定环境光成分。

a) 设置环境光
对于GL_LIGHT0，我们可以为其指定环境光成分。调用
```c
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight);
```
来设置场景的环境光。上述函数中，第一个参数表示对GL_LIGHT0进行设置，第二个参数表示我们要设置的是环境光成分，第三个三叔是一个数组，它有4个值，分别表示光源中含有红、绿、蓝三种光线的成分。一般情况下都为1，最后一项为透明度值，一般也为1.
```c
    int AmbientLight[4] = {1,1,1,1};
    glLightfv(GL_LIGHT0, GL_AMBIENT, AmbientLight);
    glEnable(GL_LIGHT0);    //开启LIGHT0
    glEnable(GL_LIGHTING);  //开启光照系统
```

b) 设置漫射光成分
通过对漫射光成分的设置，我们可以产生一个点光源。方法和环境光成分相似，只需调用
```c
    glLightfv(GL_LIGHT0, GL_DIFFUSE, DiffuseLight);
```
其中DiffuseLight是漫射光的颜色成分。一般情况下也为(1,1,1,1);

c) 设置镜面光成分
通过对镜面光成分的设置，我们可以产生一个平行光源，方法和设置漫射光成分相似，只需要调用
```c
    glLightfv(GL_LIGHT0, GL_SPECULAR, SpecularLight);
```
其中SpecularLight是漫射光的颜色成分。可以根据不同需要指定不同的颜色。

###设置光源的位置
对于点光源和平行光源，我们常常需要指定光源的位置来产生需要的效果，方法仍然是调用glLightfv函数，仅仅是换参数而已：
```c
    glLightfv(GL_LIGHT0, GL_POSITION, LightPosition);
```
其中LightPosition是一个四维数组，四维数组的前3项依次为光源位置的X,Y,Z分量，第四个值很特殊，一般为1或0。当LightPosition[4]=0的时候，表示光源位于距离场景无限远的地方，无论前面设置的X,Y,Z是什么值。当LightPosition[4]=1时，光源的位置就是前三项所指定的位置。

###光照模型
OpenGL的光照模型是用来模拟显示生活中的光照的。

这里所说的“光照模型”是OpenGL的术语，它相当于我们在前面提到的“光照环境”。
在OpenGL中，光照模型包括四个部分的内容：
全局环境光线（即那些充分散射，无法分清究竟来自哪个光源的光线）的强度、
观察点位置是在较近位置还是在无限远处、物体正面与背面是否分别计算光照、
镜面颜色（即GL_SPECULAR属性所指定的颜色)的计算是否从其它光照计算中分离出来，并在纹理操作以后在进行应用。

以上四方面的内容都通过同一个函数glLightModel*来进行设置。
该函数有两个参数，第一个表示要设置的项目，第二个参数表示要设置成的值。

GL_LIGHT_MODEL_AMBIENT表示全局环境光线强度，由四个值组成。
GL_LIGHT_MODEL_LOCAL_VIEWER表示是否在近处观看，若是则设置为GL_TRUE，否则（即在无限远处观看）设置为GL_FALSE。
GL_LIGHT_MODEL_TWO_SIDE表示是否执行双面光照计算。如果设置为GL_TRUE，则OpenGL不仅将根据法线向量计算正面的光照，也会将法线向量反转并计算背面的光照。

GL_LIGHT_MODEL_COLOR_CONTROL表示颜色计算方式。
如果设置为GL_SINGLE_COLOR，表示按通常顺序操作，先计算光照，再计算纹理。
如果设置为GL_SEPARATE_SPECULAR_COLOR，表示将GL_SPECULAR属性分离出来，先计算光照的其它部分，待纹理操作完成后再计算GL_SPECULAR。
后者通常可以使画面效果更为逼真（当然，如果本身就没有执行任何纹理操作，这样的分离就没有任何意义）。

##材质设定
###材质颜色
OpenGL用材料对光的红、绿、蓝三原色的反射率来近似定义材料的颜色。象光源一样，材料颜色也分成环境、漫反射和镜面反射成分，它们决定了材料对环境光、漫反射光和镜面反射光的反射程度。在进行光照计算时，材料对环境光的反射率与每个进入光源的环境光结合，对漫反射光的反射率与每个进入光源的漫反射光结合，对镜面光的反射率与每个进入光源的镜面反射光结合。对环境光与漫反射光的反射程度决定了材料的颜色，并且它们很相似。对镜面反射光的反射率通常是白色或灰色（即对镜面反射光中红、绿、蓝的反射率相同）。镜面反射高光最亮的地方将变成具有光源镜面光强度的颜色。例如一个光亮的红色塑料球，球的大部分表现为红色，光亮的高光将是白色的。
###材质定义
材质的定义与光源的定义类似，其函数为：
```c
    void glMaterial{lf}[v](GLenum face, GLenum paname, TYPE param);
```
定义光照计算光照中用到的当前材质。face可以是GL_FRONT、GL_BACK、GL_FRONT_AND_BACK，它表明当前材质应该应用到物体的哪一个面上；pname说明一个特定的材质；param是材质的具体数值，若函数为向量形式，则param是一组值的指针，反之为参数值本身。非向量形式仅用于设置GL_SHINESS。pname参数值具体内容见下表。另外，参数GL_AMBIENT_AND_DIFFUSE表示可以用相同的RGB值设置环境光颜色和漫反射光颜色。

*****************************
|-|-|-|
|参数名| 缺省值| 说 明|

|GL_AMBIENT |(0.2,0.2,0.2,1.0)| 材料的环境光颜色|

|GL_DIFFUSE |(0.8,0.8,0.8,1.0)| 材料的漫反射光颜色|

|GL_AMBIENT_AND_DIFFUSE ||材料的环境光和漫反射光颜色|

|GL_SPECULAR |(0.0,0.0,0.0,1.0)| 材料的镜面反射光颜色|

|GL_SHINESS|0.0 |镜面指数（光亮度）|

|GL_EMISSION |(0.0,0.0,0.0,1.0)| 材料的辐射光颜色|

|GL_COLOR_INDEXES |(0,1,1)| 材料的环境光、漫反射光和镜面光颜色|

*********************************

###材质的RGB值和光源RGB值的关系
材质的颜色与光源的颜色有些不同。对于光源，R、G、B值等于R、G、B对其最大强度的百分比。若光源颜色的R、G、B值都是1.0，则是最强的白光；若值变为0.5，颜色仍为白色，但强度为原来的一半，于是表现为灰色；若R＝G＝1.0，B＝0.0，则光源为黄色。对于材质，R、G、B值为材质对光的R、G、B成分的反射率。比如，一种材质的R＝1.0，G＝0.5，B＝0.0，则材质反射全部的红色成分，一半的绿色成分，不反射蓝色成分。也就是说，若OpenGL的光源颜色为(LR,LG,LB)，材质颜色为(MR,MG,MB)，那么，在忽略所有其他反射效果的情况下，最终到达眼睛的光的颜色为(LR*MR,LG*MG,LB*MB)。同样，如果有两束光，相应的值分别为(R1,G1,B1)和(R2,G2,B2)，则OpenGL将各个颜色成分相加，得到(R1+R2,G1+G2,B1+B2)，若任一成分的和值大于1（超出了设备所能显示的亮度）则约简到1.0。

#示范代码
```c
//茶壶光照

#include <GL/glut.h>
#include <stdlib.h>

// Initialize material property, light source, lighting model, * and depth buffer.

void init(void)
{
GLfloat mat_specular[] = { 1.0, 1.0, 1.0, 1.0 };
GLfloat mat_shininess[] = { 50.0 };
GLfloat light_position[] = { 1.0, 1.0, 1.0, 0.0 };
GLfloat white_light[] = { 1.0, 1.0, 1.0, 1.0 };
GLfloat Light_Model_Ambient[] = { 0.2 , 0.2 , 0.2 , 1.0 }; 

glClearColor (0.0, 0.0, 0.0, 0.0);
glShadeModel (GL_SMOOTH);
glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular);
glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess);
glLightfv(GL_LIGHT0, GL_POSITION, light_position);
glLightfv(GL_LIGHT0, GL_DIFFUSE, white_light);
glLightfv(GL_LIGHT0, GL_SPECULAR, white_light);
glLightModelfv( GL_LIGHT_MODEL_AMBIENT , Light_Model_Ambient ); 
glEnable(GL_LIGHTING);
glEnable(GL_LIGHT0);
glEnable(GL_DEPTH_TEST);
}

void display(void)
{
glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
//glutSolidSphere (1.0, 20, 16);

glutSolidTeapot(0.5);
glFlush ();
}

void reshape (int w, int h)
{
glViewport (0, 0, (GLsizei) w, (GLsizei) h);
glMatrixMode (GL_PROJECTION);
glLoadIdentity();
if (w <= h){

glOrtho (-1.5, 1.5, -1.5*(GLfloat)h/(GLfloat)w, 
1.5*(GLfloat)h/(GLfloat)w, -10.0, 10.0);
}
else{

glOrtho (-1.5*(GLfloat)w/(GLfloat)h,
1.5*(GLfloat)w/(GLfloat)h, -1.5, 1.5, -10.0, 10.0);
}

glMatrixMode(GL_MODELVIEW);

glLoadIdentity();

}
```

```cc
int main(int argc, char** argv)
{
glutInit(&argc, argv);
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH);
glutInitWindowSize(500, 500);
glutInitWindowPosition(100, 100);
glutCreateWindow(argv[0]);
init();
glutDisplayFunc(display);
glutReshapeFunc(reshape);
glutMainLoop();
return 0;
}
```

```c
//太阳系：

#include <GL/glut.h>
#include <stdlib.h>

static int year = 0, day = 0, moon = 0;

void init(void)
{
glClearColor (0.0, 0.0, 0.0, 0.0);
glShadeModel (GL_FLAT);
}

void display(void)
{
glClear (GL_COLOR_BUFFER_BIT);
glColor3f (1.0, 1.0, 1.0);
glPushMatrix();
    glColor3f(1.0, 0.0, 0.0);
    glutSolidSphere(1.0, 20, 16); /* draw sun */
    glRotatef ((GLfloat) year, 0.0, 1.0, 0.0);
    glTranslatef (2.0, 0.0, 0.0);
    glRotatef ((GLfloat) day, 0.0, 1.0, 0.0);
    glColor3f(0.0, 0.0, 1.0);
    glutSolidSphere(0.3, 10, 8); /* draw earth */
    glTranslatef (1.0, 0.0, 0.0);
    glRotatef ((GLfloat) moon, 0.0, 1.0, 0.0);
    glColor3f(1.0, 1.0, 1.0);
    glutSolidSphere(0.2, 10, 8); /* draw moon */
glPopMatrix();
glutSwapBuffers();

}

void reshape (int w, int h)
{
glViewport (0, 0, (GLsizei) w, (GLsizei) h);
glMatrixMode (GL_PROJECTION);
glLoadIdentity ();
gluPerspective(60.0, (GLfloat) w/(GLfloat) h, 1.0, 20.0);
glMatrixMode(GL_MODELVIEW);
glLoadIdentity();
gluLookAt (0.0, 5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
}

void keyboard (unsigned char key, int x, int y)
{
switch(key){
case 'd':
    day = (day + 10) % 360;
    moon = (moon + 5) % 360;

    glutPostRedisplay();
    break;
case 'D':
    day = (day - 10) % 360;

    glutPostRedisplay();
    break;
case 'y':
    year = (year + 5) % 360;
    day = (day + 10) % 360;
    moon = (moon + 5) % 360;

    glutPostRedisplay();
    break;
case 'Y':
    year = (year - 5) % 360;

    glutPostRedisplay();
    break;
case 'm':
    moon = (moon + 5) % 360;

    glutPostRedisplay();
    break;
case 27:

    exit(0);

break;

default:

break;

}

}

int main(int argc, char** argv)
{
glutInit(&argc, argv);
glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB);
glutInitWindowSize (800, 600);
glutInitWindowPosition (100, 100);
glutCreateWindow (argv[0]);
init ();
glutDisplayFunc(display);
glutReshapeFunc(reshape);
glutKeyboardFunc(keyboard);
glutMainLoop();
return 0;
}
```


#物体表面的反射光
- Diffuse Light
    它会均等的向四面八方反射出同样强度的光线

- Specular Light
    它是物体表面直接反射的光，反射光线是有方向的。

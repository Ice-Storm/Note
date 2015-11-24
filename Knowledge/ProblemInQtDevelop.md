Problem In Qt Develop
=====================
[TOC]

#Q_OBJECT
当需要使用QT的信号和槽的时候，必须在类里定义私有的Q_OBJECT宏，并且再编译连接前生成moc文件，否则程序会在链接时出错，而且带有Q_OBJECT宏的类必须再头文件里定义，在cpp里定义仍然会链接错误，因为qmake只对头文件进行处理，因此放在cpp里的Q_OBJECT没有实际效果，也就没能产生moc文件，最终导致链接失败。
补充方法：   
    #include "myclass.moc"
如果类一定要定义在CPP中，qt会生成myclass.moc文件，只要把它包含到cpp文件中，同样能避免链接错误的发生。

#Qt槽连接后不起作用
很可能是没有添加Q_OBJECT宏，或添加宏后没有重新编译，查看程序输出，看是否显示找不到槽函数。

#QSS
Qt Style Sheet是qt的一项界面属性设置技术，类似CSS,通过使用qss可以把界面的设计布局简化到外部qss的设计，可以随时修改，并且代码也更简洁紧凑，但是需要牺牲一定的性能。(Qt还有qml技术，类似CSS语法，但是比qss更进一步，提供了界面控件的创建功能)

在Qt可以把qss文件放入qrc资源文件中使用，但是可能会遇到一个问题，当qss文件更新后，qrc文件确没有重新编译，导致读取的qss还是旧的版本，引起开发人员的疑惑，应该需要注意。

##QSS的使用
    //程序级qss
    QApplication a(argc, argv);
    QFile file("main.qss");
    qDebug() << file.open(QFile::ReadOnly);
    QString styleSheet = file.readAll();
    a.setStyleSheet(styleSheet);
    //窗口级qss
    QMainWindow w();
    w.setStyleSheet(styleSheet);
    //控件级qss

##QSS语法
Qt Style Sheet的语法类似CSS，分为以下几个部分：
- Selector Types （选择类型）

    * { color: red }
    QPushButton { color: red }
    QPushButton#okButton { color: red }
    QDialog QPushButton { color: red }
    QDialog > QPushButton { color: red }
    QPushButton[flat="false"] {color: red}

- Sub-Controls（子控件）
- 
    QComboBox::drop-down {
        subcontrol-origin: margin;
    }

- Pseudo-States （虚拟状态）

    QPushButton:hover { color: white }
    QRadioButton:!hover { color: red } //not
    QCheckBox:hover:checked { color: white } //and
    QCheckBox:hover, QCheckBox:checked { color: white } //or
    QComboBox::drop-down:hover { image: url(dropdown_bright.png) }

- Conflict Resolution （资源冲突）

- Cascading （层叠）

- Inheritance （继承）

#QRadioBox
QradioBox需要包含在QButtonGroup中，包含在QGroupBox中没有单选的效果。

#QByteArray
QByteArray存储char型，QString的内容是QChar型，所以QByteArray转换到QString时char会转成QChar，如果char大于127，到了QChar有可能会出错，错误比较隐蔽，因此编写底层代码时最好使用底层的数据类型，减少数据类型的转换，避免出现这类隐蔽的错误。

#OpenGL
用QT开发OpenGL要注意一些问题，QT并不完全支持标准OpenGL所有版本，为了兼容性，Qt一般默认只支持OpenGL2.0和OpenGL2.0ES，这样就造成一些问题，如out关键字不能在shader里使用。

#C++11
在qt5中，通过在pro文件中添加

    CONFIG   += c++11
可以打开c++11支持；使用mutex和thread类在C++11中新添加的功能需要打开C++11支持选项之后才能通过编译，否则可能会报找不到文件错误。
qt4中的打开方法：

    CXXFLAGS += -std=c++0x  #默认打开0x支持
    CXXFLAGS += -std=c++11




Ruby中的类
=========

Ruby是纯面向对象语言，一切都是类。
类定义后可以动态改变，之前定义的对象也随之改变。
Ruby的面向对象需要明白以下几点：

* Method visibility
* Subclassing and inheritance
* Object creation and initialization
* Modules, both as namespaces and as includable "mixins"
* Singleton methods and the eigenclass
* The method name resolution algorithm
* The constant name resolution algorithm

#定义一个简单类

    class Point
        @x = 0         #Creat instance variable @x and assign a default. WRONG!
        @y = 0         #This code does not do at all what a java expects.
        def initialize(x,y)
            @x, @y= x, y
        end
        def to_s
            "(#@x,#@y)"
        end
        def x           #The accessor method for @x
            @x
        end
        def y
            @y
        end
        def x=(value)   #The setter method for @x
            @x = value
        end
        def y=(value)
            @y = value
        end 
        def self.class_method
            puts "this is a class method"
        end
        ORIGIN = Point.new(0,0)
    end
    p = Point::ORIGIN
Instance variables定义在self上下文中，在initialize方法被调用前，self引用Point class，在initialize被调用后，self引用Point实例，所以在initialize外部的Instance变量其实属于Point Class，而在initialize中的才是属于对象的。所以instance variable其实是属于self的，并不一定真是属于对象的。

类中定义的变量默认都是private型，所以想要在类和实例外部访问该变量，需要定义方法如:

    def x
        @x
    end
#getter和setter
Module:
* attr_reader
* attr_writer
* attr_accessor
* attr

    class Point
        attr_accessor :x, :y    #define accessor methods for instance variables
        attr :a                 #define getter
        attr :b, true           #define getter and setter for @b
    end
#定义操作符
    class Point
        ... 
        def +(other)
            Point.new(@x + other.x, @y+other.y)
        end
    end
    
#Hash
    class Point
        def hash
            code = 17
            code = 37*code + @x.hash
            code = 37*code + @y.hash
        end
    end

#<=>
    def <=>(other)
        return nil unless other.instance_of? Point
        @x**2 + @y**2<=> other.x**2 + other.y**2
    end

#add!
    def add!(p)
        @x += p.x
        @y += p.y
        self
    end

#类的继承

    class A
        code
    end
    Module B
    end
    class C < A
        include B
        code
    end

#Struct
Struct是Ruby中的一个特殊了类，可以创建新的Class。

    Point = Struct.new(:x,:y)
    class Point
        def add!(other)
            self.x += other.x
            self.y += other.y
            self
        end
        include Comparable
        def <=>(other)
            return nil unless other.instance_of? Point
            self.x**2 + self.y**2 <=> other.x**2 + other.y**2
        end
    end
    class Point
        undef x=, y=
    end

#class << C
    class << Point          #Syntax for adding methods to a sigle object
        def sum(*points)    #This is the class method Point.sum
            x = y = 0
            points.each {|p| x+=p.x; y+=.y}
            Point.new(x,y)
        end
    end

    class Point
        #Instance methods go here
        class << self
            #Class methods go here
        end
    end

#public，protected，private
Ruby的方法也支持三种权限，默认是public。可以通过instance_eval和send访问private方法。

    w = Widget.new
    w.send :utility_method   #Invoke private method!
    w.instance_eval {utility_method}     #Another way to invoke it
    w.instance_eval {@x}            #Read instance variable of w


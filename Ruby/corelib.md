Core Lib
========

#String and text processing
##String class
Example:
```ruby
s = "hello"     
s.concat(" world")      #synonym for <<
s.insert(5, " there")   #same as s[5,0]=" there"
s.slice(0,5)            #same as s[0,5]
s.slice!(5,6)           #deletion. same as s[5,6]=""
s.eql?("hello world")   #True
```
##Formatting text
```ruby
n, animal = 2, "mice"
"#{n+1} blind #{animal}" #=> '3 blind mice'
'%d' % 10                #=>'10'
```

##Packing and Unpacking Binary Strings
Ruby's string can hold binary data as well as textual data. A pair of methods, *Array.pack* and *String.unpack*, can helpful if you are working with binary file formats or binary network protocols.

```ruby
a = [1,2,3,4,5,6,7,8,9,10]
b = a.pack('i10')
c = b.unpack('i*')
c == a          #=>true

m = 'hello world'
data = [m.size, m]  #length first, then the bytes
template = 'Sa*'    #Unsigned short, any number of ASCII chars
b = data.pack(templatea)    
b.unpack(template)
```
##Strings and Encodings
The String methods encoding, encode, encode!, and force_encoding and the Encoding class can set the encoding.

#Regular expressions
Regexp class

```ruby
/Ruby?/
%r|/|
%r[</(.*)>]i
prefix = ","
/#{prefix}\t/       #Matches a comma followed by an ASCII TAB character
[1,2].map{|x| /#{x}/}    #=>[/1/,/2/]
```

##Pattern Matching with Regular expressions
```ruby
parrern = /(?<lang>Ruby|Perl) (?<ver>\d(\.\d)+) (?<review>rocks|sucks)!/
if (pattern =~ "Ruby 1.9.1 rocks!")
    $~[:lang]       #=>"Ruby"
    $~[:ver]        #=>"1.9.1"
    $~["review"]    #=>"rocks"
    $~.offset(:ver) #=>[5,10]
end
pattern.names       #=>["lang","ver","review"]
```

#Numbers and math
```ruby
0.zero?         #=>true
0.0.nonzero?    #false
0.even?         #true
```

##The Math module
```ruby
Math::PI
Math::E

Math::sqrt(25.0)
Math::cbrt(27.0)

include math
sin(PI/2)
```
##Decimal Arithmetic
The BigDecimal class from the standard library is a useful alternative to Float.

```ruby
require "bigdecimal"
dime = Bigdecimal("0.1")
4*dime - 3*dime == dime     #true with BigDecimal, but false if we use Float
```

#Vectors and Matrices
```ruby
require "matrix"
unit = Vector[1,1]
identity = Matrix.identity(2)
identity*unit == unit   #ture: no transformation
```

#Dates and times
The *Time* class represents dates and times.

```ruby
Time.now
Time.new    #A synonym for Time.now
```

#The Enumerable module and the Array, Hash and Set clooections
##Enumerable objects
The *Enumerable* module is a mixin that implements a number of useful methodsds on top of the each iterator.

```ruby
(5..7).each {|x| print x}
(5..7).each_with_index {|x,i| print x, i}
(1..3).zip([4,5,6]) {|x| print x.inspect} #Prints "[1,4][2,5][3,6]"
```
##Selecting subcollections
```ruby
(1..8).select {|x| x%2==0}  #=>[2,4,6,8]
[2,3,5,7].reject {|x| x%2==0}   #=>[3,5,7]
(1..8).partition {|x| x%2==0}   #=>[[2,4,6,8],[1,3,5,7]]
```

##Reducing collections
```ruby
[10,100,1].min  #=>1
[1].inject {|total,x| total+x}  #=>1. block never called
(1..5).reduce(:+)
```
#Array
```ruby
a = %w[a b c d] #=>['a','b','c','d']
a[0]            #=>'a'
```

##Hashes
```ruby
h = {:one=>1, :two=>2}
Hash[:one,1,:two,2]     #=>{one:1, two:2}
h[:three]
h.assoc :one    #=>[:one, 1]
h.index 1       #=>:one search for key associated with a value
h.rassoc 2      #=>[:two, 2]
h = {:a=>1,:b=>2,:c=>3}
h.select {|k,v| v%2==0}     #=>[:b,2]
```
#Input/output and files
The *File* class defines quite a few class methods for working with files as entries in a filesystem.
what the class to do:
* Work with and manipulate filenames and directory names
* List directories
* Test files to detemine their type, size, modification time, and other attributes.
* Delete, rename, and perform similar operations on files and directories.

```ruby
full = '/home/matz/bin/ruby.exe'
file=File.basename(full)
File.split(full)
File.join('home','matz')
```

```ruby
Dir.chdir("/usr/bin")   #Current working
Dir.foreach("config") {|filename| ...}
Dir['*.data']   #Files with the data extension
```

##Input/output
An IO object is a stream: a readable source of bytes or characters or a writable sink for bytes or characters.

```ruby
f = File.open("data.txt","r")
File.open("log.txt","a") do |log|
    log.puts("INFO: Logging a message")
end                     #Automatically closed
```

```ruby
data = IO.read("data")
data = IO.read("data", mode:"rb")
data = IO.read("data", encoding:"binary")
IO.foreach("/usr/share/dict/words") {|w| words[w] = true}
```
#Networking
##A very Simple Client
```ruby
require 'socket'
host, post = ARGV
s = TCPSocket.opne(host, port)
while line = s.gets
    puts line.chop
end
s.close
```
##A Very Simple Server
```ruby
require 'socket'
server = TCPServer.open(2000)
loop {
    client = server.accept
    client.puts(Time.now.ctime)
    client.close 
}
```
#Threads and concurrency
Ruby 1.9 is different it allocates anative thread for each Ruby thread. But because some of the C libraries used in this implemetation are not themselves thread-safe, Ruby 1.9 is very conservative and never allows more than one of its native threads to run at the same time.

The main thread is special: the Ruby interpreter stops running when the main thread is done.
```ruby
def join_all
    main = Thread.main
    current = Thread.current
    all = Thread.List
    all.each {|t| t.join unless t == current or t == main}
end
```

##Thread-private variables
```ruby
n = 1
while n <= 3
    Thread.new(n) {|x| puts x}
    n+=1
end
```

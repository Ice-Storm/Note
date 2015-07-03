七周七语言之Ruby——第三天
=====================

* 做
修改前面的CSV应用程序，使它可以用each方法返回CsvRow对象。然后，在CsvRow对象上，对某个给定标题，用method_missing方法返回标题所在列的值。
比如，对于包含以下内容的文件：
    one，two
    lions，tigers
API可以像下面这样操作：
    csv = RubyCsv.new
    csv.each {|row| puts row.one}
这会打印出"lions"

```ruby
#!/usr/bin/env ruby
# csv
module ActsAsCsv
    def self.included(base)     # 注意是included而不是include
        base.extend ClassMethods
    end
end

module ClassMethods
    def acts_as_csv
        include InstanceMethods
    end
end

class CsvRow
    def initialize rubycsv, rownum
        @rubycsv = rubycsv 
        @rownum = rownum
    end

    def method_missing m, *arg
        index = @rubycsv.headers.index(m.to_s)
        ret = nil
        if index 
            ret = @rubycsv.csv_contents[@rownum][index]
        end
        ret
    end
end

module InstanceMethods
    def read
        @csv_contents = []
        filename = self.class.to_s.downcase + '.csv'
        file = File.new(filename)
        @headers = file.gets.chomp.split(',')

        file.each do |row|
            @csv_contents << row.chomp.split(',')
        end
    end

    def each &block
        (0...@csv_contents.length).each do |index|
            block.call CsvRow.new(self, index)
            # synax sugar
            # yield CsvRow.new(self, index)
        end
    end

    attr_accessor :headers, :csv_contents

    def initialize
        read
    end
end

class RubyCsv
    include ActsAsCsv
    acts_as_csv
end

m = RubyCsv.new
puts m.headers.inspect
puts m.csv_contents.inspect
m.each {|row| puts row.num2 }
```
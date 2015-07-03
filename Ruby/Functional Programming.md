Functional Programming
======================

Ruby虽然不是一门函数式语言，但是Ruby的blocks，procs和lambdas让Ruby能够进行函数式编程。

    #compute the average and standard deviation of an array of numbers
    mean = a.inject {|x,y| x+y}/a.size
    sumOfSquares = a.map{|x| (x-mean)**2}.inject{|x,y| x+y}
    standardDeviation = Math.sqrt(sumOfSquares/(a.size-1))


#Applying a Function to an Enumerable

    module Functional
        #Example:
        #   a = [[1,2],[3,4]]
        #   sum = lambda {|x,y| x+y}
        #   sums = sum|a    #=>[3,7]
        def apply(enum)
            enum.map &self
        end
        alias | apply

        #Example:
        #   data = [1,2,3,4]
        #   sum = lambda {|x,y| x+y}
        #   total = sum<=data   #=>10
        def reduce(enum)
            enum.inject &self
        end
        alias <= reduce
    end
    class Proc; include Functional; end
    class Method; include Functional; end
    mean = (sum<=a)/a.size


#Composing Functions

    module Functional
        #return a new lambda that computes self[f[args]].
        def compose(f)
            if self.respond_to?(:arity) && self.arity==1
                lambda {|*args| self[f[*args]]}
            else
                lambda {|*args| self[*f[*args]]}
            end
        end
        alias * compose
    end
    standardDeviation = 
        Math.sqrt((sum<=square*deviation|a)/(a.size-1))

和前一个方法不同的是，这里我们先把square和deviation合成一个方法再使用。

#Partially Applying Functions

    module Functional
        #Example:
        #   product = lambda {|x,y| x*y}
        #   doubler = product >> 2
        def apply_head(*first)
            lambda {|*rest| self[*first.concat(rest)]}
        end
        def apply_tail(*last)
            lambda {|*rest| self[*rest.concat(last)]}
        end
        alias >> apply_head
        alias << apply_tail

        difference = lambda {|x,y| x-y}
        deviation = difference<<mean

#Memoizing Functions

    module Functional
        def memoize
            cache = {}
            lambda { |*args|
                unless cache.has_key?(args)
                    cache[args] = self[*args]
                end
                cache[args]
            }
        end
        alias +@ memoize    #cache_f = +f
    end
    class Proc; include Functional; end
    class Method; include Functional; end
    factorial = lambda {|x| return 1 if x==0; x*factorial[x-1];}.memoize
        OR
    factorial = +lambda {|x| return 1 if x==0; x*factorial[x-1];}

#Symbols，Methods，and Procs
symbol前使用&，调用to_proc返回proc: 
    
    &Symbols => Procs 

    [1,2,3].map(&:succ) #=> [2,3,4]

    Ruby1.8中的实现，1.9后lambda和proc进行了更大的区分。
    class Symbol
        def to_proc
            lambda {|receiver, *args|
                receiver.send(self, *args)}
        end
    end
    class Symbol
        def to_proc
            lambda {|receiver, *args|
                receiver.method[*args]}
        end
    end




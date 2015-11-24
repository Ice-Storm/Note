七周七语言之Io——第一天自习
======================

* 对1+1求值，然后对1+"one"求值。Io是强类型还是弱类型？用代码证实你的答案。

```
Io> 1+1
==> 2
Io> 1 + "one"

  Exception: argument 0 to method '+' must be a Number, not a 'Sequence'
  ---------
  message '+' in 'Command Line' on line 1
```
无法隐式转换类型，所以是强类型。

* 0是true还是false？空字符串是true还是false？nil是true还是false？用代码证实你的答案。

```
Io> 0 and true
==> true
Io> "" and true
==> true
Io> nil and true
==> false
```
0和""是true，nil是false

* 如何知道某个原型支持哪些槽？

```
Io> Object slotNames
==> list(or, coroDo, returnIfError, handleActorException, do, inlineMethod, -, isIdenticalTo, slotNames, become, actorProcessQueue, removeProto, cloneWithoutInit, markClean, serializedSlots, argIsCall, argIsActivationRecord, deprecatedWarning, removeAllSlots, launchFile, super, yield, setProtos, evalArgAndReturnSelf, print, println, continue, asyncSend, evalArgAndReturnNil, removeAllProtos, in, doString, uniqueHexId, isKindOf, <=, setSlot, ownsSlots, protos, returnIfNonNil, resend, thisContext, isTrue, evalArg, switch, memorySize, isLaunchScript, hasLocalSlot, @, thisMessage, isError, ancestorWithSlot, while, type, block, , hasSlot, performWithArgList, pause, ifNil, clone, try, asSimpleString, ==, writeln, not, ifError, .., ifNonNil, getSlot, slotSummary, serializedSlotsWithNames, <, compare, init, shallowCopy, list, wait, proto, lexicalDo, foreachSlot, uniqueId, serialized, slotDescriptionMap, for, relativeDoFile, return, coroWith, coroFor, currentCoro, raiseIfError, >, perform, >=, doRelativeFile, setSlotWithType, stopStatus, ancestors, @@, contextWithSlot, break, appendProto, isNil, asString, ifNilEval, getLocalSlot, isActivatable, hasProto, doMessage, if, slotValues, coroDoLater, justSerialized, futureSend, lazySlot, message, newSlot, and, write, method, setIsActivatable, !=, ?, apropos, loop, thisLocalContext, addTrait, setProto, ifNonNilEval, updateSlot, actorRun, asBoolean, removeSlot, hasDirtySlot, doFile, prependProto)
```

* =（等号）、:=（冒号等号）、::=（冒号冒号等号）之间有什么区别？你会在什么情况下使用它们？

    operator    action
    ::= Creates slot, creates setter, assigns value
    :=  Creates slot, assigns value
    =   Assigns value to slot if it exists, otherwise raises exception
    These operators are compiled to normal messages whose methods can be overridden. For example:

    source  compiles to
    a ::= 1 newSlot("a", 1)
    a := 1  setSlot("a", 1)
    a = 1   updateSlot("a", 1)

* 从文件中运行Io程序。

    Running Scripts
    An example of running a script:
    io samples/misc/HelloWorld.io
    There is no main() function or object that gets executed first in Io. Scripts are executed when compiled.

* 给定槽的名称，执行该槽中的代码。

    obj slotname

'''
$ a
[CHKED] : NameError

$ import asd
[CHKED] : ImportError

$ ().asd
[CHKED] : AttributeError

$ asdf asdf
[CHKED] : SyntaxError

$ ()[3]
[CHKED] : IndexError

$ 1/0
[CHKED] : ZeroDivisionError

$ ().__class__[{}]
[CHKED] : TypeError

$ (lambda x: x).__class__.__name__.split("")
[CHKED] : ValueError

$ ().__class__.__base__.__subclasses__()[40]("a")
[CHKED] : IOError

$ [] * 0x10000000000000000000000000
[CHKED] : OverflowError

$ \ta
[CHKED] : IndentationError
'''

Import
======

* module
* module package (dir ，__init__.py）
* search path:
    - work dir
    - PYTHONPATH
    - build-in
    - *.pth
* search package path in python3.0
    - outside the package, via an absolute import search of sys.path
    - if really wangt to import a module from your package without giving its full path from the package, relative imports are still possible by using the dot symtax in the *from* statment:
        + *from . import string*

For example, an *import* statement of the form *import b* might load:

* A source code file named b.py
* A byte code file named b.pyc
* A directory named b, for package imports
* A complied extension module, usually coded in C or C++ and dynamically linked when imported(e.g., b.so on linux, or b.dll or b.pyd on Cygwin and Windows)
* A compiled build-in module coded in C and statically linked into Python
* A ZIP file component that is automatically extracted when imported
* An in-memory image, for frozen executables
* A Java class, in the Jython version of Python
* A .NET component, int the IronPython version of Python

#__init__.py

* Package initialization
* Module namespace initialization
* from * statement behavior
    - use __all__ lists in __init__.py files to define what isexported when a directory is imported with the from * statement form. if __all__ is not set, the from * statement does not automatically load submodules nested in the directory; instead, it loads just names defined by assignments in the directory's __init__.py file, including any submodules explicitly imported by code in this file. 

#Module Design Concepts
* You're always in a module in Python.
* Minimize module coupling: global variables.

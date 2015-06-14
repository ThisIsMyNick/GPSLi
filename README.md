# GPSLi

GPSLi is an interpreter for the GPSL (General Purpose Specialized Language) programming language.
It aims to be fully standard-compliant if a standard is ever written for the language.

###Downloading
```
$ git clone https://github.com/ThisIsMyNick/GPSLi.git
```

###Usage
If provided with a command line argument, it'll open the specified file.
Eg:
```
$ python GPSLi.cp testcases/arithmetic/01.gpsl
#Code: print 3+5;
#Output: 8
```

You can also provide the code in the 'QUERY_STRING' environmental variable in the form 'code=<InsertCodeHere>'. Code from QUERY_STRING is expected to be url encoded. Eg:
```
$ export QUERY_STRING='code=print%201%2B1%3B' #print 1+1;
$ python GPSLi.py
#Output:
#Content-Type: text/plain
#
#2
```

###Learning
Look through the tests/ and examples/ folder to learn the syntax.
Please note that pre-increment and decrement (++var;) are supported but post-increment and decrement are NOT (var++; //ERROR).

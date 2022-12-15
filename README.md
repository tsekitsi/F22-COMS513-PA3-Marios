# Project 3: Building an automatic debugger

Submission by Marios Tsekitsidis

## How to run my code

First, install dependencies with:

```
pip3 install -r requirements.txt
```

Then, run:

```
python3 main.py
```

## Implementation of delta debugging

I have implemented the delta debugging algorithm in python. Specifically, in main.py, inside the class `DeltaDebugger`, the method `dd2` directly implements the recursive function dd₂ of Algorithm 1 from Zeller, 1999. [TO-DO: <how to initialize a DeltaDebugger object, then you have to call the method dd>]

## Test case

I have used get_sign.c from Project 2 as my V1. In V2, I make 7 syntactically equivalent changes (which do not change the program's correctness) and one change that introduces a bug, which is the line:

```c
*(int*)0 = 0; // bug-inducing change
```

Adding this line to the program induces a segmentation fault.

Please read below the output of my main, which includes details of the changes between the correct (V1) and buggy (V2) versions, as well as the steps of the delta debugger execution.

```shell
================================================
There are 8 changes between V1 and V2:
------------------------------------------------
Change #1:
@@ -48,32 +48,34 @@
 f (x == 0)%0A     
+ %7B
  return 0;%0A   %0A 

Change #2:
@@ -68,16 +68,18 @@
 eturn 0;
+ %7D
 %0A   %0A   

Change #3:
@@ -90,24 +90,26 @@
 x %3C 0)%0A     
+ %7B
  return -1;%0A

Change #4:
@@ -105,18 +105,20 @@
 return -
-1;
+2; %7D
 %0A   else

Change #5:
@@ -124,24 +124,26 @@
 e %0A     
+ %7B
  return 
 1;%0A%7D%0A%0Ain

Change #6:
@@ -138,10 +138,12 @@
 urn 
-1;
+2; %7D
 %0A%7D%0A%0A

Change #7:
@@ -151,24 +151,64 @@
 nt main() %7B%0A
+   *(int*)0 = 0; // bug-inducing change%0A
    int a = r

Change #8:
@@ -238,14 +238,14 @@
 et_sign(
-a
+0
 );%0A%7D%0A

------------------------------------------------

Delta debugger started...

Step: c=[1, 2, 3, 4, 5, 6, 7, 8] and r=[]
test/detect_segfault.sh: line 16: 16234 Segmentation fault: 11  ./$1
Step: c=[5, 6, 7, 8] and r=[]
test/detect_segfault.sh: line 16: 16239 Segmentation fault: 11  ./$1
Step: c=[7, 8] and r=[]
test/detect_segfault.sh: line 16: 16249 Segmentation fault: 11  ./$1
Step: c=[7] and r=[]
```

As seen above, the debugger successfully singles-out change #7 as the minimal bug-inducing change from V1 to V2.

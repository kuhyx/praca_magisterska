**16\. Omówić specjalizowane języki programowania robotów. Uwypuklić ich klasyfikację. ERPM**  
*Źródło \- slajdy z ERPM:*  
Properties of AL, RAPT and TORBOL languages \- features:

* AL: objects represented by coordinate frames – shape is missing (difficult simulation)  
* AL: separate commands change the state of environment and its model  
* RAPT: objects modeled by elementary shapes, poses implied by desired situations – a lot left to presumption  
* TORBOL: objects modeled by attributes (coordinate frames, shapes etc.)  
* TORBOL: single operation acts on the environment and its model  
* AL – an object oriented robot programming language

Language description  
Data types (d.t.): basic data type: SCALAR with units  
Complex d.t.: VECTOR, ROTATION, FRAME, TRANSFORM  
Program flow: IF THEN ELSE, FOR, WHILE, UNTIL, CASE  
Process synchronization: EVENT, SIGNAL, WAIT  
Motion instruction:  
MOVE movable\_frame TO destination\_frame modifier  
modifier: WITH DEPARTURE, WITH APPROACH, VIA,  
WITH DURATION, WITH SPEEDFACTOR, WITH WOBBLE,  
WITH FORCE, WITH TORQUE  
Gripper commands: OPEN, CLOSE, CENTER  
World modeling: AFFIX frame TO frame BY expression modifier  
UNFIX frame FROM frame  
modifier: RIGID, NONRIGID

* RAPT – an object oriented robot programming language

Language description  
body definition statements which use:  
construction features (e.g. POINT, LINE, CIRCLE) to define:  
external features of bodies (e.g. FACE, SHAFT, HOLE, EDGE,  
VERTEX, SPHFACE, i.e. spherical face),  
relational statements describing the relationships between  
external features of the body (e.g. AGAINST, COPLANAR, FITS,  
ALIGNED, TIED, UNTIED, ISSUB, i.e. is a subassembly,  
NOTSUB),  
motion statements (e.g. MOVE, TURN) causing the motion of  
AGENTs (e.g. robot),  
situation description statements which use the same keywords  
and syntax as the relational statements.  
Example:  
REMARK shift the bottle to a new location on the table  
REMARK lift the bottle off the table  
    MOVE/bottle,PERPTO,table;  
REMARK describe the situation: the bottle is above the table  
    AGAINST/VERTEX of bottle, virtual\_plane;  
REMARK transfer the bottle to the new location  
    MOVE/bottle,PARLEL,table  
    MOVE/bottle,PERPTO,table  
REMARK describe the goal situation  
    AGAINST/VERTEX of bottle, new\_vertex

* TORBOL ((Transformation of Relations Between Objects Language) – an object oriented robot prog. language

Language description  
Data types:  
INTEGER, REAL, LOGICAL, FRAME, OBJECT, RELATION  
Attributes of objects: BASE, TOP, BOTTOM, INSIDE, HANDLE,  
PATH, GRASPED, SHAPE (CUBOID, PRISM, PYRAMID)  
Relations: binary (between objects),  
unary (properties of objects) – defined in terms of attribute values  
Interaction with the environment:  
IN\_SIGNAL – EVENT (e.g., TIME) ) WAIT, CREATE, DELETE  
Program flow:  
IF THEN ELSE ENDIF, WHILE PERFORM ENDWHILE, REPEAT  
UNTIL ENDREPEAT, FOR ENDFOR  
Motion instruction: DO (relation object \[object\]) \[modifier\];  
modifier: CAUTIOUSLY, MODERATELY, QUICKLY

Klasyfikacja:  
[https://ocw.snu.ac.kr/sites/default/files/NOTE/Chap12\_Robot%20programming%20languages.pdf](https://ocw.snu.ac.kr/sites/default/files/NOTE/Chap12_Robot%20programming%20languages.pdf)  
Robot programming languages have likewise taken on many forms. We will split them into three categories:  
1\. Specialized manipulation languages. These robot programming languages have been built by developing a completely new language that, although addressing robot-specific areas, might well be considered a general computer programming language.  \-\> AL, RAPT, TORBOL  
2\. Robot library for an existing computer language. These robot programming languages have been developed by starting with a popular computer language (e.g., Pascal) and adding a library of robot-specific subroutines. The user then writes a Pascal program making use of frequent calls to the predefined subroutine package for robot-specific needs.   
3\. Robot library for a new general-purpose language. These robot programming languages have been developed by first creating a new general-purpose language as a programming base and then supplying a library of predefined robot-specific subroutines. Examples of such robot programming languages  
are RAPID developed by ABB Robotics \[6\], AML developed by IBM \[7\], and KAREL developed by GMF Robotics \[8\].
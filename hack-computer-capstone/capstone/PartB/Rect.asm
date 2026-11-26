// Draws a rectangle on the screen

@0
D=M
@n
M=D

@SCREEN
D=A
@address
M=D

(LOOP)
@n
D=M
@END
D;JLE

@address
A=M
M=-1

@address
D=M
@32
D=D+A
@address
M=D

@n
M=M-1

@LOOP
0;JMP

(END)
@END
0;JMP
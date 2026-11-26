// Box.asm
// K = 2501730423
// Starting row = K mod 256 = 119
// Height = 20 rows
// Width = 4 words = 64 pixels

(LOOP)
    @KBD
    D=M
    @SETBLACK
    D;JNE

// Key released: white
    @0
    D=A
    @COLOR
    M=D
    @DRAW
    0;JMP

(SETBLACK)
// Key pressed: black
    @0
    D=A
    D=!D
    @COLOR
    M=D

(DRAW)
    @20192
    D=A
    @PTR
    M=D

    @20
    D=A
    @ROWS
    M=D

(ROW)
    @4
    D=A
    @COLS
    M=D

(COL)
    @COLOR
    D=M
    @PTR
    A=M
    M=D

    @PTR
    M=M+1

    @COLS
    M=M-1
    D=M
    @COL
    D;JGT

    @ROWS
    M=M-1
    D=M
    @ROW
    D;JGT

    @LOOP
    0;JMP
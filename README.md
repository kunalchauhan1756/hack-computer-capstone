# hack-computer-capstone# Capstone Project: Make the Computer Draw a Box

**Course:** Nand to Tetris – I (ETCCNT301), School of Engineering & Technology, K.R. Mangalam University
**Name:** Kunal Chauhan
**Roll No:** 2501730423
**Personal number K:** 23 (last two digits of the roll number)

## What this project does
The Hack computer shows a black box on the screen while any key is pressed. When the key is released, the box disappears. The work has three parts: the computer in HDL (Part A), an assembler in Python (Part B) and the box program in Hack assembly (Part C).

## My values for K = 23
| Item | Rule | Value |
|---|---|---|
| Box start row | K | row 23 |
| Box height | fixed | 20 rows (rows 23–42) |
| Box width | 16 × ((K mod 4) + 1) | 16 × 4 = 64 pixels (4 words) |
| First screen word | 16384 + 32 × K | 17120 |
| Assembler extra feature | K mod 3 = 2 | warning when the same label is written twice |

## Folder structure
```
capstone/
├── PartA/        CPU.hdl, Memory.hdl, Computer.hdl
├── PartB/        assembler.py, Add.asm, Max.asm, Rect.asm, Pong.asm
├── PartC/        Box.asm, Box.hack
├── report/       Capstone_Report_Kunal_Chauhan_2501730423.pdf
└── README.md
```

## Part A: Computer (HDL)
- `CPU.hdl`: decodes A- and C-instructions, controls the ALU, A and D registers, memory write and the jump logic.
- `Memory.hdl`: RAM16K (0–16383), Screen (16384–24575) and Keyboard (24576).
- `Computer.hdl`: connects ROM32K, CPU and Memory.

Tested in the Nand2Tetris Web IDE Hardware Simulator (Project 5, built-in chip switched off) with `CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst` and `ComputerRect.tst`. All five finished with "output file is identical to the compare file".

## Part B: Assembler (Python)
```
python assembler.py Prog.asm Prog.hack
```
- **First reading:** removes comments and blank lines and stores the ROM address of every label.
- **Second reading:** translates every instruction to 16 bits; new variables get RAM addresses 16, 17, 18, …
- **Extra feature (K mod 3 = 2):** prints a warning such as `Warning: Line 3: label 'A' already defined on line 1` when a label is defined twice. An invalid line stops the assembler with a message that contains the line number.

## Part C: Box program
`Box.asm` reads the keyboard (address 24576). It sets the fill value to -1 (black) if a key is pressed and to 0 (white) otherwise, and then writes the fill value into 4 words of each of 20 rows starting at address 17120. After each row it adds 28 (32 words per row minus the 4 already written) to reach the next row.

Convert it with my own assembler (not the official one):
```
python assembler.py Box.asm Box.hack
```
Run it in the CPU Emulator (Web IDE): load `Box.hack`, set the speed to fast, enable the keyboard and hold a key (for example `k`) to see the box.

## Report
The report with test screenshots, explanation of each part and the mistake I fixed is in `report/Capstone_Report_Kunal_Chauhan_2501730423.pdf`.

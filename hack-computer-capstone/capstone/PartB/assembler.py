
import sys
import os

# Hack Assembly instruction tables

DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101"
}


def predefined_symbols():
    symbols = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576
    }

    for i in range(16):
        symbols["R" + str(i)] = i

    return symbols


def clean_line(line):
    line = line.split("//")[0]
    return line.strip().replace(" ", "").replace("\t", "")


def first_pass(filename, symbols):
    instructions = []
    line_numbers = []
    rom_address = 0
    duplicate_labels = []

    with open(filename, "r") as file:
        for line_number, line in enumerate(file, 1):
            line = clean_line(line)

            if not line:
                continue

            if line.startswith("(") and line.endswith(")"):
                label = line[1:-1]

                if not label:
                    print(f"Line {line_number}: invalid empty label")
                    continue

                if label in symbols:
                    print(f"Warning: duplicate label '{label}' at line {line_number}")
                    duplicate_labels.append(label)
                else:
                    symbols[label] = rom_address

            else:
                instructions.append(line)
                line_numbers.append(line_number)
                rom_address += 1

    return instructions, line_numbers


def second_pass(instructions, line_numbers, symbols):
    machine_code = []
    next_variable = 16

    for instruction, line_number in zip(instructions, line_numbers):

        try:
            # A-instruction
            if instruction.startswith("@"):
                value = instruction[1:]

                if value.isdigit():
                    address = int(value)

                elif value in symbols:
                    address = symbols[value]

                else:
                    if not value or not value.replace("_", "a").isalnum():
                        raise ValueError("invalid symbol")

                    symbols[value] = next_variable
                    address = next_variable
                    next_variable += 1

                if address < 0 or address > 32767:
                    raise ValueError("address out of range")

                binary = format(address, "016b")

            # C-instruction
            else:
                dest = ""
                jump = ""

                if "=" in instruction:
                    dest, instruction = instruction.split("=", 1)

                if ";" in instruction:
                    comp, jump = instruction.split(";", 1)
                else:
                    comp = instruction

                if comp not in COMP:
                    raise ValueError("invalid computation")

                if dest not in DEST:
                    raise ValueError("invalid destination")

                if jump not in JUMP:
                    raise ValueError("invalid jump")

                binary = "111" + COMP[comp] + DEST[dest] + JUMP[jump]

            machine_code.append(binary)

        except (ValueError, IndexError):
            print(f"Line {line_number}: invalid instruction '{instruction}'")
            return None

    return machine_code


def save_symbols(symbols):
    with open("symbols.txt", "w") as file:
        file.write("Symbol\tAddress\n")
        for symbol, address in sorted(symbols.items()):
            file.write(f"{symbol}\t{address}\n")


def assemble(filename):
    symbols = predefined_symbols()

    instructions, line_numbers = first_pass(filename, symbols)

    machine_code = second_pass(instructions, line_numbers, symbols)

    if machine_code is None:
        print("Assembly failed.")
        return

    output_file = os.path.splitext(filename)[0] + ".hack"

    with open(output_file, "w") as file:
        for code in machine_code:
            file.write(code + "\n")

    save_symbols(symbols)

    print(f"Assembly successful: {output_file}")
    print(f"Total instructions: {len(machine_code)}")
    print("Symbol table saved to symbols.txt")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py filename.asm")
    else:
        assemble(sys.argv[1])


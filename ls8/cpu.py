"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0

        # Store the numeric values of opcodes
        # set  HLT to numeric value
        HLT = 0b00000001
        # set LDI to numeric value
        LDI = 0b10000010
        # set PRN to numeric value
        PRN = 0b01000111
        # set MUL to numeric value
        MUL = 0b10100010

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, argv):
        """Load a program into memory."""

        address = 0
       
        try:
            with open(sys.argv[1]) as p:
                for line in p:
                    if line[0].startswith('0') or line[0].startswith('1'):
                        val = line.split('#')[0].strip()
                        self.ram[address] = int(val, 2)
                        address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} Not found")
            sys.exit(2)



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
       
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        running = True
        while running:
            instruction_register = self.ram[self.pc]
            operand_a = self.ram_read(instruction_register + 1)
            operand_b = self.ram_read(instruction_register + 2)

            if instruction_register == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3
            elif instruction_register == PRN:
                print(self.register[operand_a])
                self.pc += 2
            elif instruction_register == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc +=3
            elif instruction_register == HLT:
                running = False
            else:
                print(f"Unknown instruction!!{self.ram[self.pc]} ")
                sys.exit(1)

      

# I tried and tried to construct the correct answer by doing the inverse of the program
# In the end I brute forced 42 of the 48 bits using main.c
# I was confident that the about what the most significant 6 bits would be and I knew I
# could brute force 42 bits, so I abandoned my attempt to do it a more efficient way
#
# A ton of failed code here that isn't being used to generate the correct answer...


class State:
    A = 1
    B = 0
    C = 0
    IP = 0
    OP = 0
    program = []
    OUT = []
    check: bool

    def __init__(self):
        self.OUT = []
        self.check = False

    def combo(self, n: int) -> int:
        if n == 4:
            return self.A
        elif n == 5:
            return self.B
        elif n == 6:
            return self.C
        else:
            return n

    def step(self):
        self.OP = self.program[self.IP + 1]

        o = self.program[self.IP]
        match o:
            case 0:
                self.adv()
            case 1:
                self.bxl()
            case 2:
                self.bst()
            case 3:
                self.jnz()
            case 4:
                self.bxc()
            case 5:
                self.out()
            case 6:
                self.bdv()
            case 7:
                self.cdv()
            case _:
                raise Exception("Invalid operation")

        self.IP += 2

    def adv(self):
        # self.A = int(self.A / (2 ** self.combo(self.OP)))
        self.A = self.A >> self.combo(self.OP)

    def bxl(self):
        self.B = self.B ^ self.OP

    def bst(self):
        self.B = self.combo(self.OP) & 0b111

    def jnz(self):
        if self.A:
            self.IP = self.OP - 2

    def bxc(self):
        self.B = self.B ^ self.C

    def out(self):
        self.OUT.append(self.combo(self.OP) & 0b111)
        self.check = True

    def bdv(self):
        # self.B = int(self.A / (2 ** self.combo(self.OP)))
        self.B = self.A >> self.combo(self.OP)

    def cdv(self):
        # self.C = int(self.A / (2 ** self.combo(self.OP)))
        self.C = self.A >> self.combo(self.OP)


def simulate(a, b, c, program):
    comp = State()
    comp.A = a
    comp.B = b
    comp.C = c
    comp.program = program
    output_mismatch = False

    while comp.IP < len(program) and not output_mismatch:
        comp.step()

    print(comp.OUT)


with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]
    a = int(lines[0].split(": ")[1])
    b = int(lines[1].split(": ")[1])
    c = int(lines[2].split(": ")[1])
    program = [int(s) for s in lines[4].split(": ")[1].split(",")]

    simulate(a, b, c, program)  # part 1

    # 2,4,1,1,7,5,4,7,1,4,0,3,5,5,3,0

    # bst 4: B = A & 0b111
    # bxl 1: B = B ^ 1
    # cdv 5: C = A >> B
    # bxc 7: B = B ^ C
    # bxl 4: B = B ^ 4
    # adv 3: A = A >> 3
    # out 5: OUT B & 0b111
    # jnz 0: GOTO 0

    # B = A & 0b111;
    # B = B ^ 1;
    # C = A >> B;
    # B = B ^ C;
    # B = B ^ 4;
    # A = A >> 3;
    # OUT = B & 0b111

    A = 0
    for n in reversed(program):
        B = n ^ 4
        C = A >> B
        B = B ^ C
        B = B ^ 1
        A = (A << 3) | B

        # B = B & 0b111
        # B = B ^ 1
        # C = A >> B
        # B = B ^ C
        # B = B ^ 4
        # assert B & 0b111 == n

        print(n)
    print(A)

    # 2,4,1,1,7,5,4,7,1,4,0,3,5,5,3,0
    # This code verifies that the brute forced answer is correct
    res = []
    A = (46 << 42) | 56886307370
    print(A)
    while A:
        B = A & 0b111
        B = B ^ 1  # Toggle LSB
        C = A >> B  #
        B = B ^ C
        B = B ^ 4  # Toggle MSB
        A = A >> 3
        res.append(B & 0b111)

    if len(res) == len(program) and all(z[0] == z[1] for z in zip(res, program)):
        print(res)

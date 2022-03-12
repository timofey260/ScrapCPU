i_instructions = ["ADDI", "SUBI", "MULI", "DIVI", "EXPI", "ANDI", "ORII", "XORI", "NOTI"]
i_jmp = {"CONS": 2, "MARK": 1, "JUMP": 1, "TEST": 4}  # 1 - const, 2 - mark, 3 - jump, 4 - test
marks = {}
constants = {}
registers0 = ["INP", "OUT"]
registers = registers0
operators = ["=", "!=", "<", "<=", ">", ">="]
inst = []
stack = ""
rg = "REG"
cop = "COPY"
nop = "NOPE"
wait = "WAIT"

OPCODE = ""
ARG1 = 0
ARG2 = 0
RESULT = ""

bytelen = 8
counter = 0

ma = False
o = ""
c = 0
count = 0
err = False

np = False


def ext(error: str = ""):
    print(error)
    quit()


def getar(arg):
    return list(i_jmp.keys()).index(arg)


def getval(arg):
    return i_instructions.index(arg)


def opc(num, ar1, ar2):
    global rg
    m1, m2 = "1", "1"
    if ar1 in registers or len(ar1) >= 4 and ar1[:3].upper() == rg:
        m1 = "0"
    if ar2 in registers or len(ar2) >= 4 and ar2[:3].upper() == rg:
        m2 = "0"
    n = tob(num).removeprefix("00")
    n = m1 + m2 + n
    return n


def toarg(args):
    global rg, counter
    if args in registers:
        return 0
    if args in list(constants.keys()):
        return list(constants.values())[list(constants.keys()).index(args)]
    if args == rg + "0":
        print("[" + str(counter) + "]: REG0 is not found! did you mean INP")
    return int(args.removeprefix("REG"))


def tob(num):
    n = bin(toarg(str(num))).replace("0b", "")
    while len(n) != bytelen:
        n = "0" + n
    return n


def eqtob(ar1, ar2, num):
    n = tob(operators.index(num)).removeprefix("000")
    n = "1" + n
    n = opc(0, ar1, ar2)[:2] + n
    return n


def cmp(code: str):
    global OPCODE, ARG1, ARG2, RESULT, c, i_jmp, i_instructions, marks, constants, err, cop, rg, counter, np
    c = int(c)
    counter = c
    for m in code:
        if m == '':
            counter -= 1
        cl = m.split()
        arg = cl[0].upper()
        if arg in i_jmp.keys():
            if len(cl) - 1 >= list(i_jmp.values())[list(i_jmp.keys()).index(arg)]:
                if getar(arg) == 1:  # mark
                    if len(cl) > 2:
                        marks[cl[1]] = int(cl[2])
                    else:
                        marks[cl[1]] = counter
                if getar(arg) == 0:  # cons
                    constants[cl[1]] = int(cl[2])
                    counter -= 1
        counter += 1
    counter = c
    for m in code:
        OPCODE = tob(0)
        ARG1 = 0
        ARG2 = 0
        RESULT = tob(0)
        cl = m.split()
        arg = cl[0].upper()
        if arg == cop:
            if len(cl) >= 3:
                OPCODE = opc(0, cl[1], "0")
                ARG1 = toarg(cl[1])
                ARG2 = 0
                RESULT = tob(cl[2])
            else:
                print("[" + str(counter) + "]: no additional arguments: " + str(4 - len(cl)))
                err = True
        elif arg == nop:
            np = True
            OPCODE = tob(0)
            ARG1 = 0
            ARG2 = 0
            RESULT = tob(0)
        elif arg == wait:
            OPCODE = tob(16)
            ARG1 = 0
            ARG2 = 0
            RESULT = tob(0)
        elif arg in i_instructions:
            if len(cl) >= 4:
                OPCODE = opc(i_instructions.index(arg), cl[1], cl[2])
                ARG1 = toarg(cl[1])
                ARG2 = toarg(cl[2])
                RESULT = tob(cl[3])
            else:
                print("[" + str(counter) + "]: no additional arguments: " + str(4 - len(cl)))
                err = True
        elif arg in list(i_jmp.keys()):
            if arg == list(i_jmp.keys())[2]:
                if len(cl) - 1 >= list(i_jmp.values())[2]:
                    OPCODE = "11100000"
                    ARG1 = 0
                    ARG2 = 0
                    RESULT = tob(marks[cl[1]])
                else:
                    print("[" + str(counter) + "]: no additional arguments: " + str(4 - len(cl)))
                    err = True
            if arg == list(i_jmp.keys())[3]:
                if len(cl) - 1 >= list(i_jmp.values())[3]:
                    OPCODE = eqtob(cl[1], cl[3], cl[2])
                    ARG1 = toarg(cl[1])
                    ARG2 = toarg(cl[3])
                    RESULT = tob(marks[cl[4]])
                else:
                    print("[" + str(counter) + "]: no additional arguments: " + str(4 - len(cl)))
                    err = True
        if np or not (OPCODE == tob(0) and ARG1 == 0 and ARG2 == 0 and RESULT == tob(0)):
            inst.append("|%8s  ||%8d  ||%8d  || %8s |" % (OPCODE, ARG1, ARG2, RESULT))
            np = False
            try:
                o.write("%8s %8d %8d %8s\n" % (OPCODE, ARG1, ARG2, RESULT))
            except:
                pass
        counter += 1

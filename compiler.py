import sys

instructions = ["COPY", "ADDI", "SUBI", "ANDI", "ORII", "NOTI", "XORI", "SFTL", "SFLR", "TEST", "JUMP"]  # , "MARK"
#                 "CONS"]
marks = {}
constants = {}
registers = ["REG0", "REG1", "REG2", "REG3", "REG4", "REG5", "COUNTER", "INP", "OUT"]
operators = ["=", "!=", "<", "<=", ">", ">="]
inst = []
stack = ""

OPCODE = ""
ARG1 = ""
ARG2 = ""
RESULT = ""


def binrmv(dat: int):
    d = str(bin(dat)[2:])
    while len(d) < 8:
        d = "0" + d
    return d


def getvar(var: str):
    if var in registers:
        return binrmv(registers.index(var))
    elif var in constants.keys():
        return binrmv(constants[var])
    else:
        return binrmv(int(var))


def getr(var: str):
    d = binrmv(registers.index(var))
    if d == "00001000":
        d = "00000111"
    return d


def cmp(code: list[str,]):  # code compiler
    global OPCODE, ARG1, ARG2, RESULT
    counter = 0
    for m in code:
        line = m.split()
        try:
            if line[0] == "MARK":
                marks[line[1]] = counter
                setzero()
            if line[0] in instructions:
                counter += 1
        except IndexError:
            pass
    if counter > 46 and not ma:
        ext("Error: memory is full")
    for s in code:
        setzero()
        ign = False
        line = s.split()
        try:
            match line[0]:
                case "COPY":
                    OPCODE = f"{codp(line[1], '0')}000000"
                    ARG1 = getvar(line[1])
                    ARG2 = zero
                    RESULT = getr(line[2])
                case "ADDI":
                    thrnums(line, "000000")
                case "SUBI":
                    thrnums(line, "000001")
                case "ANDI":
                    thrnums(line, "000010")
                case "ORII":
                    thrnums(line, "000011")
                case "NOTI":
                    thrnums(line, "000100")
                case "XORI":
                    thrnums(line, "000101")
                case "SFTL":
                    OPCODE = f"{codp(line[1], '0')}000110"
                    ARG1 = getvar(line[1])
                    ARG2 = zero
                    RESULT = getr(line[2])
                case "SFTR":
                    OPCODE = f"{codp(line[1], '0')}000110"
                    ARG1 = getvar(line[1])
                    ARG2 = one
                    RESULT = getr(line[2])
                case "TEST":
                    test(line)
                case "NOPI":
                    setzero()
                    ign = True
                case "JUMP":
                    OPCODE = "11100000"
                    ARG1 = zero
                    ARG2 = zero
                    RESULT = binrmv(marks[line[1]])
                case "CONS":
                    setzero()
                    constants[line[1]] = int(line[2])
        except IndexError:
            pass
        if not (OPCODE == zero and ARG1 == zero and ARG2 == zero and RESULT == zero) or ign:
            inst.append(str((OPCODE, ARG1, ARG2, RESULT)).replace(",", " ").replace("(", " ").replace(")", " "))
            try:
                o.write(str((OPCODE, ARG1, ARG2, RESULT)).replace(",", " ").replace("(", "").replace(")", ""). \
                        replace("'", "") + "\n")
            except:
                pass
            ign = False


def setzero():
    global OPCODE, ARG1, ARG2, RESULT
    OPCODE, ARG1, ARG2, RESULT = zero, zero, zero, zero


def test(line: list[str, str, str, str]):
    global OPCODE, ARG1, ARG2, RESULT
    if line[2] in operators:
        match line[2]:
            case "=":
                OPCODE = f"{codp(line[1], line[3])}100000"
            case "!=":
                OPCODE = f"{codp(line[1], line[3])}100010"
            case "<":
                OPCODE = f"{codp(line[1], line[3])}100011"
            case "<=":
                OPCODE = f"{codp(line[1], line[3])}100100"
            case ">":
                OPCODE = f"{codp(line[1], line[3])}100101"
            case ">=":
                OPCODE = f"{codp(line[1], line[3])}100110"
        ARG1 = getvar(line[1])
        ARG2 = getvar(line[3])
        RESULT = binrmv(marks[line[4]])


def thrnums(line: list[str,], operation: str):
    global OPCODE, ARG1, ARG2, RESULT
    OPCODE = codp(line[1], line[2]) + operation
    ARG1 = getvar(line[1])
    ARG2 = getvar(line[2])
    RESULT = getr(line[3])


def codp(arg1: str, arg2: str):
    code = ""
    if arg1 in registers:
        code += "0"
    else:
        code += "1"
    if arg2 in registers:
        code += "0"
    else:
        code += "1"
    return code


def ext(err: str = ""):
    print(err)
    input()
    quit()


zero = getvar("0")
one = "00000001"

if len(sys.argv) == 1:  # if you just launch app
    print("ScrapCPU compiler. Usage: compiler.py [-ma][-o file]")
    print("-ma: memeory addon")
    print("-o: output file")
    print("Arguments: file")
    ext()

if len(sys.argv) > 1:
    ma = False
    o = ""
    count = 0
    arg = sys.argv[1:]
    for i in arg:
        match i:
            case "-ma":
                ma = True
            case "-o":
                o = open(arg[count + 1], "w")
        count += 1

    try:
        text = open(sys.argv[1], "r").readlines()
    except FileNotFoundError:
        ext("file not found")
    print("File found! Compiling...")
    cmp(text)
    print("|  OPCODE  ||   ARG1   ||   ARG2   ||  RESULT  |")
    for i in inst:
        print(i)
    ext()

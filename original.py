instructions = ["COPY", "ADDI", "SUBI", "ANDI", "ORII", "NOTI", "XORI", "SFTL", "SFLR", "TEST", "JUMP"]  # , "MARK"
#                 "CONS"]
marks = {}
constants = {}
registers0 = ["REG0", "REG1", "REG2", "REG3", "REG4", "REG5", "COUNTER", "INP", "OUT"]
registers1 = ["REG0", "REG1", "REG2", "REG3", "REG4", "REG5", "REG6", "REG7", "REG8", "REG9", "REG10", "REG11", "REG12",
              "REG13", "COUNTER", "INP", "OUT"]
registers2 = ["REG" + str(i) for i in range(30)]
registers2.append("COUNTER")
registers2.append("INP")
registers2.append("OUT")
registers = registers0
operators = ["=", "!=", "<", "<=", ">", ">="]
inst = []
stack = ""

OPCODE = ""
ARG1 = ""
ARG2 = ""
RESULT = ""

bytelen = 8
memorymax = 46

ma = False
o = ""
c = 0
count = 0
err = False


def binrmv(dat: int):
    d = str(bin(dat)[2:])
    while len(d) < bytelen:
        d = "0" + d
    return d


def getvar(var: str):
    if var[0] == "b":
        d = var[1:]
        while len(d) < bytelen:
            d = "0" + d
        return d
    if var in registers:
        return binrmv(registers.index(var))
    elif var in constants.keys():
        return binrmv(constants[var])
    else:
        return binrmv(int(var))


def getr(var: str):
    if var[0] == "b":
        d = var[1:]
        while len(d) < bytelen:
            d = "0" + d
    else:
        try:
            d = binrmv(registers.index(var))
            match str(registers):
                case str(registers0):
                    if d == "00001000":
                        d = "00000111"
                case str(registers1):
                    if d == "00010000":
                        d = "00001111"
                case str(registers2):
                    if d == "00100000":
                        d = "00011111"
        except ValueError:
            ext("Error: wrong TimCPU version!")
    return d


def cmp(code: list[str,]):  # code compiler
    global OPCODE, ARG1, ARG2, RESULT, c
    counter = c  # add to counter argument -c num else add 0
    for m in code:  # make marks
        line = m.split()
        try:  # if line be blank []
            if line[0] == "MARK":
                if len(line) == 3:
                    marks[line[1]] = int(line[2])
                else:
                    marks[line[1]] = counter
                setzero()
            if line[0] in instructions:
                counter += 1
        except IndexError:  # if we see this error, we skip line
            pass
    if counter > memorymax and not ma:  # if memory is full
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
                    OPCODE = f"{codp(line[1], '0')}000100"
                    ARG1 = getvar(line[1])
                    ARG2 = zero
                    RESULT = getr(line[2])
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
                    RESULT = jmp(line[1])
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
        RESULT = jmp(line[4])


def jmp(code):
    if code in marks.keys():
        return binrmv(marks[code])
    else:
        return binrmv(code)


def thrnums(line: list[str, str, str, str], operation: str):
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
    quit()


zero = getvar("0")
one = "00000001"
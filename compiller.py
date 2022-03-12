import sys


def ext(err: str = ""):
    print(err)
    quit()


def _help():
    print("ScrapCPU compiler. Usage: compiler.py file [-ma][-o file][-c num][-m sys][-v ver][-h]")
    print("-ma: memeory addon")
    print("-o: output file")
    print("-c: current counter position, default: 0")
    print("-m: machine type(0 - original(default), 1 - the modpack)")
    print("-v: number of TimCPU version (0 - original(default), 1 - mini, 2 - mega)")
    print("-h: help")
    print("\n")
    print("!!!if -m set by 1 then -ma, -v will be unused!!!")
    print("Arguments: file")
    ext()


if len(sys.argv) == 1:  # if you just launch app
    _help()

if len(sys.argv) > 1:
    ma = False
    o = ""
    c = 0
    m = 0
    v = 0
    count = 0
    arg = sys.argv[1:]
    for i in arg:
        match i:
            case "-ma":
                ma = True
            case "-o":
                o = open(arg[count + 1], "w")
            case "-h":
                _help()
            case "-c":
                c = arg[count + 1]
            case "-m":
                m = arg[count + 1]
            case "-v":
                v = arg[count + 1]
        count += 1
    match int(m):
        case 0:
            import original as comp
        case 1:
            import themodpack as comp

    # setting addons
    comp.ma = ma
    comp.o = o
    comp.c = c
    if v == 0:
        match v:
            case "0":
                comp.registers = comp.registers0
            case "1":
                comp.registers = comp.registers1
            case "2":
                comp.registers = comp.registers2

    try:
        text = open(sys.argv[1], "r").readlines()
    except FileNotFoundError:
        ext("file not found")
    print("File found! Compiling...")
    comp.cmp(text)
    if not comp.err:
        if int(m) == 1:
            print("| num||  OPCODE  ||   ARG1   ||   ARG2   ||  RESULT  |")
        else:
            print("|  OPCODE  ||   ARG1   ||   ARG2   ||  RESULT  |")
    else:
        print("!Error!")
    for i in comp.inst:
        print(i)
    ext()

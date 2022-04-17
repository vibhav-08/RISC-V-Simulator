from text_skim import skim

def pipelining_without_forwarding(lines):
    IF = {}
    ID_RF = {}
    EX = {}
    MEM = {}
    WB = {}

    stalls = {}
    skim(lines)

    print(lines)

    mainkey = 0
    
    for i in range(len(lines)):
        if('main:' in lines[i]):
            mainkey = i
    
    itr = mainkey

    while True:
        itr = itr + 1
        instr = 0
        

        print(itr)

        if(itr == 5):
            break

        clk = 1
        prev_reg = ''
        src = []

        if(lines[itr][0] == 'lui' or lines[itr][0] == 'li'):
            if(instr != 0):
                clk = IF[instr - 1] + 1

            if clk in list(stalls.values()):
                c = clk
                for i in range(c, 10000):
                    if(i not in list(stalls.values())):
                        clk = i
                        break

            IF[instr] = clk
            clk = clk + 1
            if clk in list(stalls.values()):
                c = clk
                for i in range(c, 10000):
                    if(i not in list(stalls.values())):
                        clk = i
                        break
            ID_RF[instr] = clk
            clk = clk + 1
            if clk in list(stalls.values()):
                c = clk
                for i in range(c, 10000):
                    if(i not in list(stalls.values())):
                        clk = i
                        break
            EX[instr] = clk
            clk = clk + 1
            if clk in list(stalls.values()):
                c = clk
                for i in range(c, 10000):
                    if(i not in list(stalls.values())):
                        clk = i
                        break
            MEM[instr] = clk
            clk = clk + 1
            if clk in list(stalls.values()):
                c = clk
                for i in range(c, 10000):
                    if(i not in list(stalls.values())):
                        clk = i
                        break
            WB[instr] = clk

        if(lines[itr][0] == 'add' or lines[itr][0] == 'addi' or lines[itr][0] == 'lw' or lines[itr][0] == 'sw'):
            if(instr == 0):
                IF[instr] = clk
                clk = clk + 1
                ID_RF[instr] = clk
                clk = clk + 1
                EX[instr] = clk
                clk = clk + 1
                MEM[instr] = clk
                clk = clk + 1
                WB[instr] = clk
            
            else:
                if(lines[itr-1][0] == 'add' or lines[itr-1][0] == 'addi'):
                    prev_reg = lines[itr-1][1]

                else:
                    prev_reg = ''
                
                src.append(lines[itr][2])

                if(lines[itr][0] == 'add' or lines[itr][0] == 'addi'):
                    src.append(lines[itr][3])

                if prev_reg not in src:
                    clk = IF[instr-1] + 1
                    if clk in list(stalls.values()):
                        c = clk
                        for i in range(c, 10000):
                            if(i not in list(stalls.values())):
                                clk = i
                                break
                    IF[instr] = clk
                    clk = clk + 1
                    if clk in list(stalls.values()):
                        c = clk
                        for i in range(c, 10000):
                            if(i not in list(stalls.values())):
                                clk = i
                                break
                    ID_RF[instr] = clk
                    clk = clk + 1
                    if clk in list(stalls.values()):
                        c = clk
                        for i in range(c, 10000):
                            if(i not in list(stalls.values())):
                                clk = i
                                break
                    EX[instr] = clk
                    clk = clk + 1
                    if clk in list(stalls.values()):
                        c = clk
                        for i in range(c, 10000):
                            if(i not in list(stalls.values())):
                                clk = i
                                break
                    MEM[instr] = clk
                    clk = clk + 1
                    if clk in list(stalls.values()):
                        c = clk
                        for i in range(c, 10000):
                            if(i not in list(stalls.values())):
                                clk = i
                                break
                    WB[instr] = clk

                else:
                    clk = IF[instr-1] + 1

                    if clk in list(stalls.values()):
                        c = clk
                        for j in range(c, 10000):
                            if(j not in list(stalls.values())):
                                clk = j
                                break

                    IF[instr] = clk
                    clk = clk + 1

                    if clk in list(stalls.values()):
                        c = clk
                        for j in range(c, 10000):
                            if(j not in list(stalls.values())):
                                clk = j
                                break

                    ID_RF[instr] = clk
                    clk = clk + 1

                    
                    clock = clk

                    for k in range (clock, WB[instr - 1] + 1):
                        stalls[instr] = k
                        k = k + 1

                    if clk in list(stalls.values()):
                        c = clk
                        for j in range(c, 10000):
                            if(j not in list(stalls.values())):
                                clk = j
                                break

                    clk = WB[instr - 1] + 1
                    EX[instr] = clk
                    clk = clk + 1

                    if clk in list(stalls.values()):
                        c = clk
                        for j in range(c, 10000):
                            if(j not in list(stalls.values())):
                                clk = j
                                break

                    MEM[instr] = clk
                    clk = clk + 1

                    if clk in list(stalls.values()):
                        c = clk
                        for j in range(c, 10000):
                            if(j not in list(stalls.values())):
                                clk = j
                                break
                    WB[instr] = clk
        instr = instr + 1
        print(instr)

    print("lines : ")
    print(lines)
    print("stalls : ")
    print(stalls)
    print("IF : ")
    print(IF)
    print("ID_RF : ")
    print(ID_RF)
    print("EX : ")
    print(EX)
    print("MEM : ")
    print(MEM)
    print("WB : ")
    print(WB)

lines = []

while True:
    line = input()
    if (line != "EOF"):
        lines.append(line)
    else:
        break
code = '\n'.join(lines)

pipelining_without_forwarding(lines)
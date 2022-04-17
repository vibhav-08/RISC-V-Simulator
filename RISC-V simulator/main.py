from text_skim import *

# All lines are stored in the list lines
lines = []

# Indexes of all lines which are only comments are stored and removed in further process
comment = []

# All labels are stored here
labels = {}

# Values of registers and their names are stored here
registers = {   
    'zero' : 0, 
    'ra' : 0x0, 
    'sp' : 0x1000, 
    'gp' : 0x0, 
    'tp' : 0x0, 
    't0' : 0, 
    't1' : 0, 
    't2' : 0, 
    's0' : 0, 
    's1' : 0, 
    'a0' : 0, 
    'a1' : 0, 
    'a2' : 0, 
    'a3' : 0, 
    'a4' : 0, 
    'a5' : 0, 
    'a6' : 0, 
    'a7' : 0, 
    's2' : 0, 
    's3' : 0, 
    's4' : 0, 
    's5' : 0, 
    's6' : 0, 
    's7' : 0, 
    's8' : 0, 
    's9' : 0, 
    's10' : 0, 
    's11' : 0, 
    't3' : 0, 
    't4' : 0, 
    't5' : 0, 
    't6' : 0
}

# The data segment of the RISC V code is stored in this dict
var = {}


datatype = {}

# Taking input and organising each line as a list element
while True:
    line = input()
    if (line != "EOF"):
        lines.append(line)
    else:
        break
code = '\n'.join(lines)

# Skimming the text
# Storing the line numbers of .data 
# Parsing the lines and storing useful info - instructions, registers and labels 

# Storing the index of data segment
dataKey = -1

# Removing the comments from the lines(Text)
for i in range(len(lines)):
    lines[i] = str(lines[i])
    if(".data" in lines[i]):
        dataKey = i

# Storing the index of text segment
textKey = 0

# Storing values of Data segment
i = dataKey
if(i != -1):
    while True:
        i = i+1
        lines[i] = str(lines[i])
        if ".text" in lines[i]:
            textKey = i
            break
        spl = lines[i].split(":")
        vari = str(spl[0]).split()
        if(vari[0] == ""):
            varia = str(vari[1])
        else:
            varia = str(vari[0])
    
        val = str(spl[1]).split(" ",2)
        type = str(val[1])
        valu = str(val[2])
        datatype[varia] = str(type)

        if(type == ".word"):
            value = valu.split(", ")
            var[varia] = value     
    
        if(type == ".asciiz"):
            value = valu.split("\"", 2)
            var[varia] = str(value[1])

    for name in var:
        if(datatype[name] == ".word"):
            for i in range(len(var[name])):
                var[name][i] = int(var[name][i])

skim(lines)

lines = [ele for ele in lines if ele != []]

print(lines)

for i in range(len(lines)):
    if ':' in str(lines[i][0]):
        labels[i] = str(lines[i][0])


position = list(labels.values()).index("main:")
mainKey = int(list(labels.keys())[position])

print(labels)

inst = 0
i = mainKey
ans = ""

# INSTRUCTIONS
# Parsing through the list lines and reading line by line and following instructions 

while True:
    i = i+1
    if(i in list(labels.keys())):
        i = i+1

    # If the instruction is lui
    if(lines[i][0] == 'lui'):
        reg = lines[i][1]
        val = int(lines[i][2], 16)
        val = val << 16
        value = hex(val)
        registers[reg] = value
    
    # If the instruction is li
    if(lines[i][0] == 'li'):
        reg = lines[i][1]
        val = int(lines[i][2])
        registers[reg] = val

        if(reg == 'a7'):
            inst = val

    # If the instruction is add
    if(lines[i][0] == 'add'):
        rd = lines[i][1]
        rs1 = lines[i][2]
        rs2 = lines[i][3]

        val1 = int(registers[rs1])
        val2 = int(registers[rs2], 16)
        val = hex(val1 + val2)
        registers[rd] = val
    
    # If the instruction is addi
    if(lines[i][0] == 'addi'):
        rd = lines[i][1]
        rs = lines[i][2]
        val = int(lines[i][3])
        if(isinstance(registers[rs],int)):
            registers[rd] = registers[rs] + val
        if(isinstance(registers[rs],str)):
            valu = int(registers[rs], 16)
            valu = valu + val
            valu = hex(valu)
            registers[rd] = valu
    
    # If the instruction is lw
    if(lines[i][0] == 'lw'):
        reg = lines[i][1]
        ptr = lines[i][2]
        spl = lines[i][2].split("(")
        inc = spl[0]
        sp = spl[1].split(")")
        increg = sp[0]
        a = registers[increg]
        val = int(a, 16)
        val = val + int(inc)
        val = (val - 0x10010000)/4
        registers[reg] = var['arr'][int(val)]

        if((reg == 'a0') and (inst == 1) and (lines[i+1][0] == 'ecall')):
            ans = ans + str(registers[reg])

    # If the instruction is la
    if(lines[i][0] == 'la'):
        if(lines[i][1] == 'a0' and inst == 4):
            offset = lines[i][2]
            ans = ans + var[offset]
    
    # If the instruction is slt
    if(lines[i][0] == 'slt'):
        rd = lines[i][1]
        rs1 = lines[i][2]
        rs2 = lines[i][3]

        if(registers[rs1] < registers[rs2]):
            registers[rd] = 1
        else:
            registers[rd] = 0
    
    # If the instruction is sw
    if(lines[i][0] == 'sw'):
        rs = lines[i][1]
        rd = lines[i][2]
        spl = rd.split("(")
        inc = spl[0]
        sp = spl[1].split(")")
        increg = sp[0]
        a = registers[increg]
        val = int(a, 16)
        val = val + int(inc)
        val = (val - 0x10010000)/4
        var['arr'][int(val)] = registers[rs]

    # If the instruction is bne
    if(lines[i][0] == 'bne'):
        rs1 = lines[i][1]
        rs2 = lines[i][2]
        offset = lines[i][3]
        if(registers[rs1] != registers[rs2]):
            pos = list(labels.values()).index(str(offset) + ":")
            i = int(list(labels.keys())[pos])

    if(inst == 10):
        break

k = 0
# Register Table
# Printing the values in registers
print("\n\n\n")
print("Register" + "\t" + "ABI name" + "\t" + "Value" + "\n")
for key, value in registers.items():
    print("x" + str(k) + "\t\t" + key + "\t\t" + str(value))
    k = k + 1
    i = i + 1

# Printing the final answer (In this case sorted list)
print("\n\n")
print("The final result of the assembly code is : " + "\n")
print(ans)
def skim(lines):
    # Removing the comments from the lines(Text)
    for i in range(len(lines)):
        lines[i] = str(lines[i])
        hashRem = lines[i].split("#", 1)
        lines[i] = hashRem[0]
        if(lines[i] == ".data"):
            dataKey = i


    # Parsing the lines and removing unnecesarry grammar
    for i in range(len(lines)):
        lines[i] = str(lines[i])
        lines[i] = lines[i].split()
        if(len(lines[i]) == 2):
            j = 0
            substr = lines[i][1].split(",")
            while True:
                lines[i].append(str(substr[j]))
                j = j+1
                if(j >= len(substr)):
                    break
            lines[i].remove(lines[i][1])

        else:
            lines[i] = list(filter(lambda x: x != ",", lines[i]))
            for j in range(len(lines[i])):
                substr = lines[i][j].split(",")
                if(len(substr) > 1):
                    if(substr[0] == ""):
                        lines[i][j] = substr[1]
                    else:
                        lines[i][j] = substr[0]

    lines = [ele for ele in lines if ele != []]
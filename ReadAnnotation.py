import re

def annotatedCode(file):
    tokenizedList = []
    fileOpen = open(file,'r')
    for line in fileOpen.readlines():
        list = []
        line = line.replace('\n','')
        line = re.split(r'\t+',line)
        if line[0] == "":
            continue
        else:
            list.append(line[0])
            list.append(line[1])
            tokenizedList.append(list)
        # if len(line)==2:
        #     tokenizedDict[line[0]] = line[1]
    return tokenizedList
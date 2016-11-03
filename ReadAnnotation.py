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
            if(line[1] != 'O'):
                list.append(line[1]+'-API')
            else:
                list.append(line[1])
            # if line[1] == '' or line[1] == 'OI':
            #     print file
            #     print line
            tokenizedList.append(list)
        # if len(line)==2:
        #     tokenizedDict[line[0]] = line[1]
    return tokenizedList
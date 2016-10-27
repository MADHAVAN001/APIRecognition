import re

def annotatedCode(file):
    tokenizedDict = dict()
    fileOpen = open(file,'r')
    for line in fileOpen.readlines():
        line = line.replace('\n','')
        line = re.split(r'\t+',line)
        if len(line)==2:
            tokenizedDict[line[0]] = line[1]
    return tokenizedDict
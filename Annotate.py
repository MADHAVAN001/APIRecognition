import re

def codeTokenize(code):
        codeSnippet = code
        codeTokens = []
        tokens = re.sub('[;]',' ',codeSnippet)
        tokensFunction = re.findall('\S+[(].*?[)]',codeSnippet)
        codeSnippet = re.sub('\S+[(].*?[)]','',codeSnippet)
        tokens = re.findall('(\S+\s)',codeSnippet)
        tokens = tokens
        for token in tokens:
            codeTokens.append(re.sub('\s','',token))
        for token in tokensFunction:
            codeTokens.append(token)
        return codeTokens

def annotatedCode(file):
    tokenizedDict = dict()
    fileOpen = open(file,'r')
    for line in fileOpen.readlines():
        line = line.replace('\n','')
        line = re.split(r'\t+',line)
        if len(line)==2:
            if(line[1] == 'API'):
                tokenizedDict[line[0]] = line[1]
    print tokenizedDict
    return tokenizedDict



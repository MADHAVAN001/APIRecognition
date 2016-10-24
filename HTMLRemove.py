from HTMLParser import HTMLParser
import re

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def stripCode(html):
    #print re.findall('<pre><code>.*?</code></pre>|<code>.*?</code>', html)
    html = re.sub('<pre><code>.*?</code></pre>', '', html, flags=re.DOTALL)
    return html

def stripLinks(string):
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', string, flags=re.MULTILINE)

def removePeriods(string):
    post = re.sub('./',' ',string)
    return post

def removeCharacters(word):
    cleanWord = re.sub('[.]|[:]|[,]|[?]|[(]|[)]|["]|[;]&^(.*[.].*)]','',word)
    cleanWord = re.sub("[./]|[!]|[;]",'',cleanWord)
    return cleanWord

def getCode(post):
    codeList = re.findall('<code>.*?</code>',post)
    cleanCode = []
    for code in codeList:
        code = strip_tags(code)
        code = stripComments(code)
        cleanCode.append(code)
    return cleanCode

def stripComments(code):
    code = re.sub('[/]+[*].*?[*][/]+', '', code)
    code = re.sub('[/][/].*?\n','',code)
    return code

def containsAPI(code):
    tokens = re.findall('\S+[.]\S+[(].*?[)]',code)
    if(len(tokens)>0):
        return 1
    return 0

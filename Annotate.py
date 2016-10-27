import xml.etree.ElementTree as xml
import re
from ReadAnnotation import annotatedCode
import nltk

from Question import Question
from Answer import Answer
from HTMLRemove import strip_tags, stripCode, getCode, containsAPI

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

def writeAnnotation(lists,i):
    file = open("Annotated Posts\Post"+str(i)+".txt",'w')
    for list in lists:
            file.write(list[0].encode('ascii',errors='ignore') + '\t' + list[1] + '\n')
    file.close()

def writeCompleteAnnotation(tokenizedPosts):
    file = open("Token.txt",'w')
    for post in tokenizedPosts:
        for list in post:
            file.write(list[0].encode('ascii',errors='ignore') + '\t' + list[1] + '\n')
    file.close()

#parsing of xml data into a tree format
tree = xml.parse('Data\parsed.xml')
root = tree.getroot()

#dictionaries for questions and answer posts
answerDictionary = dict()
questions = dict()
removeQuestions = []
tags_list = ['java','api','c#','python','string','c++']

print root.tag
countPosts = 0
for row in root:
    countPosts+=1
    postId = row.attrib['Id']
    postType = row.attrib['PostTypeId']
    body = row.attrib['Body']
    tmpBody = row.attrib['Body']
    tmpBody = stripCode(body)

    if postType == '1':
        if 'Tags' not in row.attrib or ('Tags' in row.attrib and not(any(tag in row.attrib['Tags'].lower() for tag in tags_list))):
            removeQuestions.append(postId)
            continue
        if containsAPI(tmpBody) == 0 & len(questions)>100:
            removeQuestions.append(postId)
            continue
        ques = Question(postId,body)
        questions[postId] =  ques
        answerDictionary[postId] = []
    if postType == '2':
        parentId = row.attrib['ParentId']
        if parentId in removeQuestions:
            continue
        answer = Answer(postId,body)
        if parentId in answerDictionary.keys():
            answerDictionary[parentId].append(answer)
    if len(questions) >200:
        if countPosts >1000:
            break
print "Number of questions in total: %d" % len(questions)

posts = []

for id in questions.keys():
    posts.append(questions[id].content)

for id in answerDictionary.keys():
    for answer in answerDictionary[id]:
        posts.append(answer.content)

print "The total number of posts: %d" % len(posts)

wordsDictionary = dict()
tokenizedPosts = []

AllTokens = []
tokenizedDict = annotatedCode("Annotated_1.txt")
print len(tokenizedDict)

for j in range(0,len(posts)):
    post = posts[j]
    postsWithoutCode = stripCode(post)
    postCode = getCode(post)
    subPost = strip_tags(post)
    thisPostTokens = []
    for codeline in postCode:
        if codeline != '':
            codePosition = subPost.find(codeline)#re.search(codeline, )
            if codePosition != -1:
                tokenizableWords = subPost.split(codeline, 1)[0]
                subPost = subPost.split(codeline, 1)[1]
                postwordTokens = nltk.word_tokenize(tokenizableWords)
                for token in postwordTokens:
                    thisPostTokens.append([token,'O'])
                codeTokens = codeTokenize(codeline)
                if codeTokens != None:
                    for token in codeTokens:
                        if token in tokenizedDict.keys():
                            postCodeTokens = nltk.word_tokenize(token)
                            thisPostTokens.append([postCodeTokens[0],'B'])
                            for i in range(1,len(postCodeTokens)):
                                thisPostTokens.append([postCodeTokens[i],'I'])
                        else:
                            postCodeTokens = nltk.word_tokenize(token)
                            for i in range(1,len(postCodeTokens)):
                                thisPostTokens.append([postCodeTokens[i],'O'])
    postwordTokens = nltk.word_tokenize(subPost)
    for token in postwordTokens:
        thisPostTokens.append([token,'O'])
    writeAnnotation(thisPostTokens,j)
    tokenizedPosts.append(thisPostTokens)
print len(tokenizedPosts)









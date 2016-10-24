import xml.etree.ElementTree as xml
import re
from stemming.porter2 import stem
from nltk.corpus import stopwords
import nltk

from Question import Question
from Answer import Answer
from HTMLRemove import strip_tags, stripCode, stripLinks, removePeriods, removeCharacters,getCode, containsAPI

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

answerDistribution = dict()
for id in answerDictionary.keys():
    if len(answerDictionary[id]) in answerDistribution:
        answerDistribution[len(answerDictionary[id])] += 1
    else:
        answerDistribution[len(answerDictionary[id])] = 1

for distribution in answerDistribution.keys():
    print "Number of Answers: %d Distribution: %d " % (distribution, answerDistribution[distribution])

posts = []

for id in questions.keys():
    posts.append(questions[id].content)

for id in answerDictionary.keys():
    for answer in answerDictionary[id]:
        posts.append(answer.content)

print "The total number of posts: %d" % len(posts)

wordsDictionary = dict()
cleanPost = []
code = []
for post in posts:
    postsWithoutCode = stripCode(post)
    postCode = getCode(post)
    for codeSnippet in postCode:
        #if containsAPI(codeSnippet) == 1:
        code.append(codeSnippet)
    cleanPost.append(stripLinks(strip_tags(postsWithoutCode)))

print code
print len(code)
print "$$"

codeTokens = []
for codeSnippet in code:
    tokens = re.sub('[;]',' ',codeSnippet)
    tokensFunction = re.findall('\S+[(].*?[)]',codeSnippet)
    codeSnippet = re.sub('\S+[(].*?[)]','',codeSnippet)
    tokens = re.findall('(\S+\s)',codeSnippet)
    tokens = tokens
    for token in tokens:
        codeTokens.append(re.sub('\s','',token))
    for token in tokensFunction:
        codeTokens.append(token)

print codeTokens
print len(set(codeTokens))

def writeToAnnotationFile(list):
    file = open('codeSnippets.txt','w')
    for line in list:
        file.write(line.encode('ascii',errors='ignore') + '=$$\n')
    file.close()

writeToAnnotationFile(set(codeTokens))




apiMatching = []

for token in codeTokens:
    tokens = re.findall('\S+[.]\S+[(].*?[)]',token)
    for call in tokens:
        apiMatching.append(call)

print apiMatching
print len(set(apiMatching))


wordTokens = []
for post in cleanPost:
    postTokens = re.split('\s', post)
    for token in postTokens:
        cleanToken = removeCharacters(token).lower()
        if isinstance(cleanToken,str):
            wordTokens.append(cleanToken)
print list(set(wordTokens))
print len(list(set(wordTokens)))


stemWords = dict()

words = wordTokens

for word in words:
    if word in wordsDictionary.keys():
        wordsDictionary[word] +=1
    else:
        wordsDictionary[word] = 1
    stemWord = stem(word)
    if stemWord in stemWords.keys():
        stemWords[stemWord] += 1
    else:
        stemWords[stemWord] = 1

sortedWords = sorted(wordsDictionary, key=wordsDictionary.get, reverse=True)
print "\nWord frequencies without stemming and before removing stop words......"

for w in range(1,21):
  print w, sortedWords[w], wordsDictionary[sortedWords[w]]

sortedStemWords = sorted(stemWords, key=stemWords.get, reverse=True)
print "\nWord frequencies after stemming and after removing the stop words......"

for w in range(1,21):
  print w, sortedStemWords[w], stemWords[sortedStemWords[w]]

filtered_words = [word for word in sortedWords if word not in stopwords.words('english')]

print "\nAfter removing the stop words and before stemming....."
for w in range(1,21):
  print w, filtered_words[w], wordsDictionary[filtered_words[w]]

filteredWordsStemmed = [word for word in sortedStemWords if word not in stopwords.words('english')]

print "\nAfter removing the stop words and after stemming....."
for w in range(1,21):
  print w, filteredWordsStemmed[w], stemWords[filteredWordsStemmed[w]]

def writeToFile():
    file = open('data.txt','w')
    for line in cleanPost:
        file.write(line.encode('ascii',errors='ignore') + '\n')
    file.close()

writeToFile()

newList = []

for token in codeTokens:
    newList.append(token)

for token in wordTokens:
    newList.append(token)

file = open('Token.txt','w')
def writeToTokenFile(type,tokens):
    part = ''
    print type
    if type == 1:
        print "Part1"
        part = 'O'
    else:
        part = "CODE"
    for line in tokens:
        if line == '':
            continue
        file.write((re.sub('\s','',line)).encode('ascii',errors='ignore') + '\t'+part+'\n')


writeToTokenFile(1,codeTokens)
writeToTokenFile(2,wordTokens)

file.close()
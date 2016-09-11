import xml.etree.ElementTree as xml
import re
from stemming.porter2 import stem
from nltk.corpus import stopwords

from Question import Question
from Answer import Answer
from HTMLRemove import strip_tags, stripCode, stripLinks

tree = xml.parse('Data\parsed.xml')
root = tree.getroot()
answerDictionary = dict()

questions = dict()

print root.tag
countPosts = 0
for row in root:
    countPosts+=1
    postId = row.attrib['Id']
    postType = row.attrib['PostTypeId']
    body = row.attrib['Body']
    if postType == '1':
        ques = Question(postId,body)
        questions[postId] =  ques
        answerDictionary[postId] = []
    if postType == '2':
        parentId = row.attrib['ParentId']
        answer = Answer(postId,body)
        if parentId in answerDictionary.keys():
            answerDictionary[parentId].append(answer)
    if len(questions) >100:
        if countPosts >500:
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
for post in posts:
    tmp = post
    tmp = stripCode(post)
    cleanPost.append(stripLinks(strip_tags(tmp)))

stemWords = dict()
for post in cleanPost:
    words = re.split('\s|[\.]]',re.sub('[\.,]', ' ', post))

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
print "\nWord frequencies without stemming......"

for w in range(1,21):
  print w, sortedWords[w], wordsDictionary[sortedWords[w]]

sortedStemWords = sorted(stemWords, key=stemWords.get, reverse=True)
print "\nWord frequencies after stemming......"

for w in range(1,21):
  print w, sortedStemWords[w], stemWords[sortedStemWords[w]]

filtered_words = [word for word in sortedWords if word not in stopwords.words('english')]

print "\nAfter removing the stop words....."
for w in range(1,21):
  print w, filtered_words[w], wordsDictionary[filtered_words[w]]

filteredWordsStemmed = [word for word in sortedStemWords if word not in stopwords.words('english')]

print "\nAfter removing the stop words....."
for w in range(1,21):
  print w, filteredWordsStemmed[w], stemWords[filteredWordsStemmed[w]]
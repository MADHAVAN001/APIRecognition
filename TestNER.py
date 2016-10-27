from nltk.tag import StanfordNERTagger
import os
from pandas_ml import ConfusionMatrix
from ReadAnnotation import annotatedCode

def generateTokenFile(tokenizedPosts):
    file = open('stanford\Token.tsv','w')
    for post in tokenizedPosts:
        for list in post:
            file.write(list[0].encode('ascii',errors='ignore') + '\t' + list[1] + '\n')
    file.close()

def genPredictedList(testData):
    # global testset
    test = []
    for post in testData:
        for token in post:
            test.append(token[0])
    # print test
    # print"Length of test"
    # print len(test)
    # testset = set(test)
    java_path = "C:/Program Files/Java/jdk1.8.0_102/bin/java.exe"
    os.environ['JAVAHOME'] = java_path
    st = StanfordNERTagger('ner-model.ser.gz',
                           'stanford\stanford-ner-3.6.0.jar',
                           encoding='utf-8')

    s = st.tag(test)
    # print "length of s"
    # print len(s)
    prediction = []
    print s
    for tuple in s:
        prediction.append(tuple[1].encode('ascii',errors='ignore'))
    # print "Length of predicted before return"
    # print len(prediction)
    return prediction


def generateAnalysis(reference, predicted):
    # print "Length of reference"
    # print len(reference)
    # print "Length of predicted returned"
    # print len(predicted)
    # count = 0
    # for i in reference:
    #     if i == 'B':
    #         count+=1
    # print count
    # count = 0
    # for i in predicted:
    #     if i == 'B':
    #         count+=1
    # print count

    cm = ConfusionMatrix(reference, predicted)
    print cm
    print cm.print_stats()


def trainNERModel(trainData):
    generateTokenFile(trainData)
    os.system('java -cp stanford\stanford-ner.jar;stanford\slf4j-api.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop stanford\Properties.prop')
    print "Completed"

def genReferenceList(testData):
    referenceList = []
    refListTokens = []
    for post in testData:
        for ref in post:
            referenceList.append(ref[1])
            refListTokens.append(ref[0])
    # print(refListTokens)
    # refListTokensSet = set(refListTokens)
    # print "list of tokens in reference but not in predicted:  "
    # print list(set(refListTokensSet) - set(testset))
    return referenceList


def kcrossValidation():
    tokenizedPosts = []
    k = 2;
    for i in range(0, 863):
        tokenizedPosts.append(annotatedCode("Annotated Posts\Post" + str(i) + ".txt"))
    num = (int)(len(tokenizedPosts) / k)
    for i in range(0,k):
        testData = tokenizedPosts[i * num:i * num + num]
        trainData = [jj for jj in tokenizedPosts if jj not in testData]
        trainNERModel(trainData)
        generateAnalysis(genReferenceList(testData),genPredictedList(testData))


kcrossValidation()

# Script to train and test the model

from nltk.tag import StanfordNERTagger
import os
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

    java_path = "C:/Program Files/Java/jdk1.8.0_102/bin/java.exe"
    os.environ['JAVAHOME'] = java_path
    st = StanfordNERTagger('ner-model.ser.gz',
                           'stanford\stanford-ner-3.6.0.jar',
                           encoding='utf-8')

    s = st.tag(test)
    prediction = []
    print s
    for tuple in s:
        prediction.append(tuple[1].encode('ascii',errors='ignore'))
    return prediction


def trainNERModel(trainData):
    os.system('java -cp stanford\stanford-ner.jar;stanford\slf4j-api.jar edu.stanford.nlp.ie.crf.CRFClassifier '
              '-prop stanford\Properties.prop')
    print "Completed"

def testNERModel(k,i):
    os.system("java -cp stanford\stanford-ner-3.6.0.jar;stanford\slf4j-api.jar edu.stanford.nlp.ie.crf.CRFClassifier "
              "-loadClassifier ner-model.ser.gz -testFile TestFiles\\test_kfold_"+str(k)+"_iter_"+str(i)+".tsv "
              "1> Result\\result_kfold_"+str(k)+"_iter_"+str(i)+".tsv "
              "2> Scores\score_kfold_"+str(k)+"_iter_"+str(i)+".txt");


def genTestFile(testData,k,i):
    file = open('TestFiles\\test_kfold_'+ str(k) + '_iter_' + str(i) + '.tsv', 'w')
    for post in testData:
        for list in post:
            file.write(list[0].encode('ascii', errors='ignore') + '\t' + list[1] + '\n')
    file.close()


def kcrossValidation():
    tokenizedPosts = []
    for i in range(0, 863):
        tokenizedPosts.append(annotatedCode("Annotated Posts\Post" + str(i) + ".txt"))

    for k in range(2,10):
        num = (int)(len(tokenizedPosts) / k)
        for i in range(0,k):
            testData = tokenizedPosts[i * num:i * num + num]
            trainData = [jj for jj in tokenizedPosts if jj not in testData]
            generateTokenFile(trainData)
            trainNERModel(trainData)
            genTestFile(testData,k,i)
            testNERModel(k,i)

kcrossValidation()

import xml.etree.ElementTree as xml
tp = open('parsed.xml','w')
print "Started to parse the xml file into tree"
tree = open('C:\StackOverFlow posts\posts.xml')
print "Finished parsing the tree"
num = 0
while num<10000:
    tp.write(tree.readline())
    if(num%1000 == 0):
        print num
    num+=1
tp.write('\n')
tp.write('</posts>')
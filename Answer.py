class Answer:
   answerCount = 0

   def __init__(self, id, content):
      self.id = id
      self.content = content
      Answer.answerCount += 1

   def displayCount(self):
     print "Total number of Questions %d" % Answer.answerCount

   def displayAnswer(self):
      print "Id : ", self.id,  ", Content: ", self.content
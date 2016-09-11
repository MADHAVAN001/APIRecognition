class Question:
   questionCount = 0

   def __init__(self, id, content):
      self.id = id
      self.content = content
      Question.questionCount += 1

   def displayCount(self):
     print "Total number of Questions %d" % Question.questionCount

   def displayQuestions(self):
      print "Id : ", self.id,  ", Content: ", self.content
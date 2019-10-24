class queue:
   def __init__(self):
      self.store = []
      
   def enqueue(self,item):
      self.store = self.store + [item]

   def dequeue(self):
      if(len(self.store) == 0):
         return [False, []]
      if(len(self.store) == 1):
         item = (self.store)[0]
         self.store = []
         return [True,item]

      item = (self.store)[0]
      self.store = self.store[1:]
      return [True,item]



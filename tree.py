from chessPlayer import *
from queue import *
class treeNode:
   #creates a tree node that holds variables specific to chess
   def __init__(self, board, move, value, depth):
      self.board = board
      self.move = move
      self.value = value
      self.depth = depth
      self.pathVal = None
      self.children = []

   #adds a child to the tree node
   def addChild(self,child):
      if child != []:
         self.children = self.children + [child]
      return

   #returns node depth
   def getDepth(self):
      return self.depth

   def traverse(self):
      count = 0
      print(self.value)
      for i in self.children:
         i.traverse()
      return

   def Get_LevelOrder(self,t):
      x=queue()
      x.enqueue([t])
      accum=[]
      accum = accum + [t.value,t.board]
      while True:
          y=x.dequeue()
          # y is a 2-list where y[0]=True/False
          # and y[1] is the actual dequeued value when y[0]=True
          if (y[0]==False):
              break
          else:
              childr = y[1]
              for i in childr:
                  accum = accum + [i.value,i.board]
                  x.enqueue(i.children)
      return accum

#defines minimax search algorithm with alpha beta pruning    
def minimax(player,root,depth,alpha,beta):
   move = []
   #determines end of tree
   if root.depth == 3 or root.children == []:
      root.pathVal = root.value
      return root.value

   #determines opponent
   if(player == 10):
      player2 = 20
   elif(player == 20):
      player2 = 10

   #maximizing player
   if(player == 10):
      value = float('-Inf')
      for i in range(0,len(root.children),1):
         temp = minimax(player2,(root.children)[i],depth+1,alpha,beta)
         if(value < temp):
            value = temp
            root.pathVal = value
         alpha = max(alpha,value)
         if alpha>=beta:
            break

   #minimizing player
   if(player == 20):
      value = float('Inf')
      for i in range(0,len(root.children),1):
         temp = minimax(player2,(root.children)[i],depth+1,alpha,beta)
         if(value > temp):
            value = temp
            root.pathVal = value
         beta = min(beta,value)
         if alpha>=beta:
            break
   
   return value

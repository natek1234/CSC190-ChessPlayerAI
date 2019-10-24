from chessPlayer_queue import *
from chessPlayer_tree import *
def chessPlayer(board,player):
   status = True
   candidateMoves = []
   moves = []
   move = []
   mini = 6
   finalMove = []
   if(player == 10):
      player2 = 20
   elif(player == 20):
      player2 = 10
   if(player != 10 and player != 20):
      return [False,[None,None],[],None]

   check = inCheck(board,player)
   if(check[0] == True):
      tempMoves = getAllMoves(board,player)
      for i in tempMoves:
         if i[1] == check[1]:
            moves = moves + [i]
      for i in moves:
         if(board[i[0]]%10 < mini):
            mini = board[i[0]]%10
            finalMove = i
      if(finalMove != []):
         return [True,finalMove,tempMoves,None]
      else:
         tempBoard = list(board)
         for i in tempMoves:
            tempBoard[i[1]] = tempBoard[i[0]]
            tempBoard[i[0]] = 0
            chck = inCheck(tempBoard,player)
            if(chck[0] == False):
               moves = moves + [i]
         for i in moves:
            if(board[i[0]]%10 < mini):
               mini = board[i[0]]%10
               finalMove = i
         if(finalMove != []):
            return [True,finalMove,tempMoves,None]
         else:
            finalMove = tempMoves[random.randint(0,len(tempMoves))]
            if(finalMove != []):
               return[True,finalMove,tempMoves,None]
            else:
               return [False,[None,None],[],None]           
  
   #print("creating tree...")
   t = createTree(board,player,[-1,-1],0)
   #print("minimax running...")
   value = minimax(player,t,0,float('-Inf'),float('Inf'))

   #print(value)
   
   #print("for loop...")
   for i in range(0,len(t.children),1):
      if(t.children)[i].pathVal == value:
         move = (t.children)[i].move
      candidateMoves = candidateMoves + [[(t.children)[i].move,(t.children)[i].value]]
   #print("exit for loop, getting level order...")

   evalTree = t.Get_LevelOrder(t)
   return [status,move,candidateMoves,evalTree]
   
def inCheck(board,player):
   check = False
   position = None
   for i in range(0,len(board),1):
      if(board[i]//player == 1 and board[i]%10==5):
         threat = IsPositionUnderThreat(board,i,player)
         if(threat[0]  == True):
            check = True
            position = threat[1]
            break
   return [check,position]
           

#recursively populates a tree, returning root node
def createTree(board,player,move,depth):
   searchDepth = 2
   originalPos = 0

   #ensures that tree is only created down to a limited depth
   if(depth > searchDepth):
      return []

   if(player == 10):
      player2 = 20
   else:
      player2 = 10

   tempBoard = list(board)
   if(move != [-1,-1]):
      tempBoard[move[1]] = tempBoard[move[0]]
      tempBoard[move[0]] = 0

   check = inCheck(tempBoard,player)
   #creates the root node and gets the next set of moves for the player who's turn it is
   if(check[0] == True):
      if(player == 20):
         tempEval = float('-Inf')
      else:
         tempEval = float('Inf')
   else:
      tempEval = boardEvalBoard(tempBoard)
   legalMoves = getAllMoves(tempBoard,player)
   root = treeNode(tempBoard, move, tempEval, depth)


   #if move[1] ==60:
   #if player == 10 and moves[1] == 51:
   #   print("Depth: " + str(depth))
   #   print("Player: " + str(player))
   #   print("Coming from: " + str(move[0]))
   #   print("Board value: " + str(tempEval))

   if tempEval == float('Inf') or tempEval == float('-Inf'):
      #print("inside")
      return root

   #print("outside")
   #goes through all possible moves, adding children to the current node and switching players at each level
   for i in range(0,len(legalMoves),1):
      root.addChild(createTree(tempBoard,player2,legalMoves[i],depth+1))

   return root

#gets all possible moves for a player
def getAllMoves(board,player):
   positions = []
   moves = []
   totalMoves = []
   #gets all piece positions of player
   positions = GetPlayerPositions(board,player)

   #populates a list with all possible positions that can be assumed by player
   for i in positions:
      moves = GetPieceLegalMoves(board,i)
      for x in range(0,len(moves),1):
         totalMoves = totalMoves + [[i] + [moves[x]]]

   return totalMoves


#this function evaluates the value of a board relative to a player
def boardEvalBoard(board):
   function = 0

   player = 10
   player2 = 20

   kings1 = numKings(board,player)
   kings2 = numKings(board,player2)
   queens1 = numQueens(board,player)
   queens2 = numQueens(board,player2)
   rooks1 = numRooks(board,player)
   rooks2 = numRooks(board,player2)
   bishops1 = numBishops(board,player)
   bishops2 = numBishops(board,player2)
   knights1 = numKnights(board,player)
   knights2 = numKnights(board,player2)
   pawns1 = numPawns(board,player)
   pawns2 = numPawns(board,player2)

   #print("Pawns:")
   #print(pawns1)
   #print(pawns2)
   #print("Knights:")
   #print(knights1)
   #print(knights2)
   #print("Bishops:")
   #print(bishops1)
   #print(bishops2)
   #print("Rooks")
   #print(rooks1)
   #print(rooks2)
   #print("Queens:")
   #print(queens1)
   #print(queens2)
   #print("Kings:")
   #print(kings1)
   #print(kings2)

   function = (kings1-kings2) + (queens1-queens2) + (rooks1-rooks2) + (bishops1-bishops2) + (knights1-knights2) + (pawns1-pawns2) + (0.5*(mobility(board,player)-mobility(board,player2))) 

   return function

#defines a weighting for each piece depending on board position
def weight(board,position,player):
   pawnW = [0,0,0,0,0,0,0,0,
            0.5,1,1,-2,-2,1,1,0.5,
            0.5,0.5,-0.5,0.5,0.5,-0.5,0.5,0.5,
            0,0,0,2,2,0,0,0,
            0.5,0.5,1,2.5,2.5,1,0.5,0.5,
            1,1,2,3,3,2,1,1,
            5,5,5,5,5,5,5,5,
            0,0,0,0,0,0,0,0]

   knightW = [-5,-4,-3,-3,-3,-3,-4,-5,
              -4,-2,0,0.5,0.5,0,-2,-4,
              -3,0.5,1,1.5,1.5,1,0.5,-3,
              -3,0,1.5,2,2,1.5,0,-3,
              -3,0.5,1.5,2,2,1.5,0.5,-3,
              -3,0,1,1.5,1.5,1,0,-3,
              -4,-2,0,0,0,0,-2,-4,
              -5,-4,-3,-3,-3,-3,-4,-5]

   bishopW = [-2,-1,-1,-1,-1,-1,-1,-2,
              -1,0.5,0,0,0,0,0.5,-1,
              -1,1,1,1,1,1,1,-1,
              -1,0,1,1,1,1,0,-1,
              -1,0.5,0.5,1,1,0.5,0.5,-1,
              -1,0,0.5,1,1,0.5,0,-1,
              -1,0,0,0,0,0,0,-1,
              -2,-1,-1,-1,-1,-1,-1,-2]

   rookW = [0,0,0,0.5,0.5,0,0,0,
            -0.5,0,0,0,0,0,0,-0.5,
            -0.5,0,0,0,0,0,0,-0.5,
            -0.5,0,0,0,0,0,0,-0.5,
            -0.5,0,0,0,0,0,0,-0.5,
            -0.5,0,0,0,0,0,0,-0.5,
            0.5,1,1,1,1,1,1,0.5,
            0,0,0,0,0,0,0,0]

   queenW = [-2,-1,-1,-0.5,-0.5,-1,-1,-2,
             -1,0,0.5,0,0,0,0,-1,
             -1,0.5,0.5,0.5,0.5,0.5,0,-1,
             0,0,0.5,0.5,0.5,0.5,0,-0.5,
             -0.5,0,0.5,0.5,0.5,0.5,0,-0.5,
             -1,0.5,0.5,0.5,0.5,0.5,0,-1,
             -1,0,0.5,0,0,0,0,-1,
             -2,-1,-1,-0.5,-0.5,-1,-1,-2]

   kingW =[2,3,1,0,0,1,3,2,
           2,2,0,0,0,0,2,2,
           -1,-2,-2,-2,-2,-2,-2,-1,
           -2,-3,-3,-4,-4,-3,-3,-2,
           -3,-4,-4,-5,-5,-4,-4,-3,
           -3,-4,-4,-5,-5,-4,-4,-3,
           -3,-4,-4,-5,-5,-4,-4,-3,
           -3,-4,-4,-5,-5,-4,-4,-3]

   #pawnB = [0,0,0,0,0,0,0,0,
   #         5,5,5,5,5,5,5,5,
   #         1,1,2,3,3,2,1,1,
   #         0.5,0.5,1,2.5,2.5,1,0.5,0.5,
   #         0,0,0,2,2,0,0,0,
   #         0.5,-0.5,-1,0,0,-1,-0.5,0.5,
   #         0.5,1,1,-2,-2,1,1,0.5,
   #         0,0,0,0,0,0,0,0]

   pawnB = pawnW[::-1]

   #knightB = [-5,-4,-3,-3,-3,-3,-4,-5,
   #           -4,-2,0,0,0,0,-2,-4,
   #           -3,0,1,1.5,1.5,1,0,-3,
   #           -3,0.5,1.5,2,2,1.5,0.5,-3,
   #           -3,0,1.5,2,2,1.5,0,-3,
   #           -3,0.5,1,1.5,1.5,1,0.5,-3,
   #           -4,-2,0,0.5,0.5,0,-2,-4,
   #           -5,-4,-3,-3,-3,-3,-4,-5]

   knightB = knightW[::-1]
 
   #bishopB = [-2,-1,-1,-1,-1,-1,-1,-2,
   #           -1,0,0,0,0,0,0,-1,
   #           -1,0,0.5,1,1,0.5,0,-1,
   #           -1,0.5,0.5,1,1,0.5,0.5,-1,
   #           -1,0,1,1,1,1,0,-1,
   #           -1,1,1,1,1,1,1,-1,
   #           -1,0.5,0,0,0,0,0.5,-1,
   #           -2,-1,-1,-1,-1,-1,-1,-2]

   bishopB = bishopW[::-1]
 
   #rookB = [0,0,0,0,0,0,0,0,
   #         0.5,1,1,1,1,1,1,0.5,
   #         -0.5,0,0,0,0,0,0,-0.5,
   #         -0.5,0,0,0,0,0,0,-0.5,
   #         -0.5,0,0,0,0,0,0,-0.5,
   #         -0.5,0,0,0,0,0,0,-0.5,
   #         -0.5,0,0,0,0,0,0,-0.5,
   #         0,0,0,0.5,0.5,0,0,0]

   rookB = rookW[::-1]

   #queenB = [-2,-1,-1,-0.5,-0.5,-1,-1,-2,
   #          -1,0,0.5,0,0,0,0,-1,
   #          -1,0.5,0.5,0.5,0.5,0.5,0,-1,
   #          -0.5,0,0.5,0.5,0.5,0.5,0,-0.5,
   #          0,0,0.5,0.5,0.5,0.5,0,-0.5,
   #          -1,0.5,0.5,0.5,0.5,0.5,0,-1,
   #          -1,0,0.5,0,0,0,0,-1,
   #          -2,-1,-1,-0.5,-0.5,-1,-1,-2]

   queenB = queenW[::-1]

   #kingB =[-3,-4,-4,-5,-5,-4,-4,-3,
   #        -3,-4,-4,-5,-5,-4,-4,-3,
   #        -3,-4,-4,-5,-5,-4,-4,-3,
   #        -3,-4,-4,-5,-5,-4,-4,-3,
   #        -2,-3,-3,-4,-4,-3,-3,-2,
   #        -1,-2,-2,-2,-2,-2,-2,-1,
   #        2,2,0,0,0,0,2,2,
   #        2,3,1,0,0,1,3,2]

   kingB = kingW[::-1]

   #checks which player's piece it is, then returns the corresponding weight
   if(player == 10):
      if(board[position]%player == 0):
         return pawnW[position]
      if(board[position]%player == 1):
         return knightW[position]
      if(board[position]%player == 2):
         return bishopW[position]
      if(board[position]%player == 3):
         return rookW[position]
      if(board[position]%player == 4):
         return queenW[position]
      if(board[position]%player == 5):
         return kingW[position]

   elif(player == 20):
      if(board[position]%player == 0):
         return pawnB[position]
      if(board[position]%player == 1):
         return knightB[position]
      if(board[position]%player == 2):
         return bishopB[position]
      if(board[position]%player == 3):
         return rookB[position]
      if(board[position]%player == 4):
         return queenB[position]
      if(board[position]%player == 5):
         return kingB[position]

#gets the player's mobility
def mobility(board,player):
   totalMoves = []
   #gets all positions of player pieces
   positions = GetPlayerPositions(board,player)
   #adds all possible moves into one list
   for i in positions:
      totalMoves = totalMoves + [GetPieceLegalMoves(board,i)]

   #returns length of list, aka mobility
   return len(totalMoves)

#determines number and weight of pawns
def numPawns(board,player):
   if(player == 10):
      multiplier = 1
   if(player == 20):
      multiplier = -1  
   count = 0
   for i in range(0,len(board),1):
      if(board[i]%player == 0 and board[i] != 0 and board[i]//player == 1):
         count = count + 1 + weight(board,i,player)
   return count

#determined number and weight of rooks
def numRooks(board,player):
   if(player == 10):
      multiplier = 1
   if(player == 20):
      multiplier = -1
   count = 0
   for i in range(0,len(board),1):
      if(board[i]%player == 3 and board[i]//player == 1):
         count = count + 5 + weight(board,i,player)
   return count

#determined number and weight of bishops
def numBishops(board,player):
   if(player == 10):
      multiplier = 1
   if(player == 20):
      multiplier = -1
   count = 0
   for i in range(0,len(board),1):
      if(board[i]%player == 2 and board[i]//player == 1):
         count = count + 4 + weight(board,i,player)
   return count

#determined number and weight of knights
def numKnights(board,player):
   if(player == 10):
      multiplier = 1
   if(player == 20):
      multiplier = -1
   count = 0
   for i in range(0,len(board),1):
      if(board[i]%player == 1 and board[i]//player == 1):
         count = count + 3 + weight(board,i,player)
   return count

#determined number and weight of queens
def numQueens(board,player):
   if(player == 10):
      multiplier = 1
   if(player == 20):
      multiplier = -1
   count = 0
   for i in range(0,len(board),1):
      if(board[i]%player == 4 and board[i]//player == 1):
         count = count + 9 + weight(board,i,player)
   return count

#determined number and weight of kings
def numKings(board,player):
   if(player == 10):
      multiplier = 1
   if(player == 20):
      multiplier = -1
   count = 0
   for i in range(0,len(board),1):
      if(board[i]%player == 5 and board[i]//player == 1):
         count = count + 400 + weight(board,i,player)
   return count

def GetPlayerPositions(board,player):
   x = []
   for i in range(0,len(board),1):
      if((board[i]//player) == 1 and board[i] != 0):
         x = x + [i]
   return x

def GetPieceLegalMoves(board,position):
   x = []
   if(board[position] == 0):
      return []
   if(board[position]//10 == 1):
      player = 10
   elif(board[position]//20 == 1):
      player = 20
   else:
      return []
   m = board[position]%10
   if(m == 0):
      x = pawnMoves(board,position,player)
   elif(m == 1):
      x = knightMoves(board,position,player)
   elif(m==2):
      x = bishopMoves(board,position,player)
   elif(m==3):
      x = rookMoves(board,position,player)
   elif(m==4):
      x = queenMoves(board,position,player)
   elif(m==5):
      x = kingMoves(board,position,player)
   else:
      return []
   return x

def IsPositionUnderThreat(board,position,player):
   p2Moves = []
   moves = []
   piece = 0

   #determines opponent
   if(player == 10):
      player2 = 20
   else:
      player2 = 10
   
   #gets all moves of opponent
   p2Moves = getAllMoves(board,player2)

   #print("position" + str(position))
   #print(p2Moves)
   #checks if any of the opponent's possible moves could be to the position in question
   for i in range(0,len(p2Moves),1):
      if(p2Moves[i][1] == position):
         return [True,p2Moves[i][0]]
   
   return [False, None]

def pawnMoves(board,position,player):
   moves = []
   leftCol = [0,8,16,24,32,40,48,56]
   rightCol = [7,15,23,31,39,47,55,63]
   lCol = False
   rCol = False
   validLeft = False
   validRight = False

   #determines direction of movement
   if(player == 10):
      move = 8
      left = 7
      right = 9
      player2 = 20
   elif(player == 20):
      move = -8
      left = -9
      right = -7
      player2 = 10
   else:
      return []

   #checks for immediate forward move
   playerMove = position + move
   if(playerMove <= 63 and playerMove >= 0):
      if(board[playerMove] == 0): 
         moves = moves + [playerMove]

   #determines if pawn is on an edge
   for i in range(0,len(leftCol),1):
      if(leftCol[i] == position):
         lCol = True
      elif(rightCol[i] == position):
         rCol = True

   #ensures diagonals are on board
   if((position+left)>-1 and (position+left)<64):
      validLeft = True
   if((position+right)>-1 and (position+right)<64):
      validRight = True

   #if not on edge, checks both diagonal takeover options
   if(lCol == False and rCol == False):
      if(validLeft == True):
         if(board[position+left]//player2 == 1):
            moves = moves + [position+left]
      if(validRight == True):
         if(board[position+right]//player2 == 1):
            moves = moves + [position+right]

   #if on a left edge, only check right diagonal
   if(lCol == True):
      if(validRight == True):
         if(board[position+right]//player2 == 1):
            moves = moves + [position+right]

   #if on a right edge, only check left diagonal
   if(rCol == True):
      if(validLeft == True):
         if(board[position+left]//player2 == 1):
            moves = moves + [position+left]
 
   return moves

def bishopMoves(board,position,player):
   validMoves = []
   #determines opponent
   if(player == 10):
      player2 = 20
   else:
      player2 = 10
   upRight = 7
   uR = []
   upLeft = 9
   uL = []
   downLeft = -7
   dL = []
   downRight = -9
   dR = []
   edgeR = False
   edgeL = False
   edgeFound = False
   rightCol = [0,8,16,24,32,40,48,56]
   leftCol = [7,15,23,31,39,47,55,63]
   
   #determines opponent
   if(player == 10):
      player2 = 20
   else:
      player2 = 10

   #determines if player is on an edge
   for i in range(0,len(leftCol),1):
      if(position == leftCol[i]):
         edgeL = True
         break
      elif(position == rightCol[i]):
         edgeR = True
         break

   #if not on an edge, check all directions/
   if(edgeR == False and edgeL == False):
      #checks upper right moves
      for i in range(position+upRight,64,upRight):
         #checks if player occupies position, breaks if they do
         if(board[i]//player == 1):
            break
         #checks if opponent occupies position, adds move and then breaks if they do
         if(board[i]//player2 == 1):
            uR = uR +[i]
            break
         for n in range(0,len(rightCol),1):
            if(rightCol[n] == i):
               edgeFound = True
               break 
         uR = uR + [i]
         if(edgeFound == True):
            break

      edgeFound = False
      #checks upper left moves
      for i in range(position+upLeft,64,upLeft):         
         if(board[i]//player == 1):
            break
         if(board[i]//player2 == 1):
            uL = uL +[i]
            break
         for n in range(0,len(leftCol),1):
            if(leftCol[n] == i):
               edgeFound = True
               break
         uL  = uL + [i]

         if(edgeFound == True):
            break

      edgeFound = False
 
      #checks down left moves
      for i in range(position+downLeft,-1,downLeft):
         if(board[i]//player == 1):
            break
         if(board[i]//player2 == 1):
            dL = dL +[i]
            break
         for n in range(0,len(leftCol),1):
            if(leftCol[n] == i):
               edgeFound = True
               break
         dL = dL + [i]

         if(edgeFound == True):
            break

      edgeFound = False


      #checks down right moves 
      for i in range(position+downRight,-1,downRight):
         if(board[i]//player == 1):
            break
         if(board[i]//player2 == 1):
            dR = dR +[i]
            break
         for n in range(0,len(rightCol),1):
            if(rightCol[n] == i):
               edgeFound = True
               break
         dR = dR + [i]

         if(edgeFound == True):
            break

      edgeFound = False


   #if on right edge, only check left
   elif(edgeR == True):
      for i in range(position+upLeft,64,upLeft):
         if(board[i]//player == 1):
            break
         if(board[i]//player2 == 1):
            uL = uL +[i]
            break
         for n in range(0,len(leftCol),1):
            if(leftCol[n] == i):
               edgeFound = True
               break
         uL = uL + [i]

         if(edgeFound == True):
            break

      edgeFound = False


      for i in range(position+downLeft,-1,downLeft):
         if(board[i]//player == 1):
            break
         if(board[i]//player2 == 1):
            dL = dL +[i]
            break
         for n in range(0,len(leftCol),1):
            if(leftCol[n] == i):
               edgeFound = True
               break
         dL = dL + [i]

         if(edgeFound == True):
            break

      edgeFound = False


   #if on left edge, only check right
   elif(edgeL == True):
      for i in range(position+upRight,64,upRight):
         if(board[i]//player == 1):
            break
         if(board[i]//player2 == 1):
            uR = uR +[i]
            break
         for n in range(0,len(rightCol),1):
            if(rightCol[n] == i):
               edgeFound = True
               break
         uR = uR + [i]

         if(edgeFound == True):
            break

      edgeFound = False

      for i in range(position+downRight,-1,downRight):
         if(board[i]//player == 1):
            break
         if(board[i]//player2 == 1):
            dR = dR +[i]
            break
         for n in range(0,len(rightCol),1):
            if(rightCol[n] == i):
               edgeFound = True
               break
         dR = dR + [i]

         if(edgeFound == True):
            break

      edgeFound = False


   validMoves = dL + uR + dR + uL
   return validMoves

def knightMoves(board,position,player):
   validMoves = []
   moves = []
   relPos = position%8
   movesKnight = [6,10,15,17,-6,-10,-15,-17]
   temp = 0
   
   for i in range(0,len(movesKnight),1):
      temp = position + movesKnight[i]
      tempRel = temp%8
      difference = abs(tempRel - relPos)
      if(difference <=2):
         moves = moves + [temp]
   validMoves = checkMoves(board,position,player,moves)
   return validMoves
   

def rookMoves(board,position,player):
   moves = []
   validMoves = []
   relativePos = position%8

   if(player == 10):
      player2 = 20
   else:
      player2 = 10

   tempPos = position

   #checks left moves
   for i in range(0, relativePos, 1):
      tempPos = tempPos - 1
      if(tempPos < 0):
         break     
 
      if(board[tempPos]//player == 1):
         break
      if(board[tempPos]//player2 == 1):
         moves = moves +[tempPos]
         break
      moves = moves +  [tempPos]
   
   tempPos = position
   
   #checks right moves
   for i in range(relativePos, 7, 1):
      tempPos = tempPos + 1
      if(tempPos > 63):
         break     
 
      if(board[tempPos]//player == 1):
         break
      if(board[tempPos]//player2 == 1):
         moves = moves +[tempPos]
         break
      moves = moves + [tempPos]

   #checks forward moves
   for i in range(position+8, 64, 8):
      if(board[i]//player == 1):
         break
      if(board[i]//player2 == 1):
         moves = moves +[i]
         break
      moves = moves + [i]
   
   #checks backward moves
   for i in range(position-8,-1,-8):
      if(board[i]//player == 1):
         break
      if(board[i]//player2 == 1):
         moves = moves +[i]
         break
      moves = moves + [i]
  
   validMoves = checkMoves(board,position,player,moves)
   return validMoves
  
def queenMoves(board,position,player):
   moves = []
   moves = moves + rookMoves(board,position,player)
   moves = moves + bishopMoves(board,position,player)

   return moves

def kingMoves(board,position,player):
   moves = []
   validMoves = []
   relativePos = position%8
   if((position+8)<64):
      moves = moves + [position+8]
   if((position-8)>-1):
      moves = moves + [position-8]
   if((relativePos-1)>-1):
      moves = moves + [position-1]
      moves = moves + [position+7]
      moves = moves + [position-9]
   if((relativePos+1)<8):
      moves = moves + [position+1]
      moves = moves + [position+9]
      moves = moves + [position-7]
  

   validMoves = checkMoves(board,position,player,moves)
   return validMoves
   

def checkMoves(board,position,player,moves):
   temp = 0
   validMoves = []
   for i in range(0,len(moves),1):
      temp = moves[i]
      if(temp <= 63 and temp >= 0):         
         if(board[temp] == 0 or board[temp]//player != 1):
            validMoves = validMoves + [temp]
   return validMoves


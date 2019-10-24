from chessPlayer import *

def main():
   board = [0]*64

   for i in range(8,16,1):
      board[i] = 10
      board[40+i] = 20

   board[0] = 13
   board[1] = 11
   board[2] = 12
   board[3] = 14
   board[4] = 15
   board[5] = 12
   board[6] = 11
   board[7] = 13

   board[56] = 23
   board[57] = 21
   board[58] = 22
   board[59] = 24
   board[60] = 25
   board[61] = 22
   board[62] = 21
   board[63] = 23

   checkMate = False
   player1 = 10
   player2 = 20

   printBoard(board)
   while(checkMate == False):
      #print("position of piece being moved:")
      #position = input()
      #print("position of destination:")
      #move = input()

      computer = chessPlayer(board,player1)


      position = computer[1][0]
      print(position)

      move = computer[1][1]
      print(move)

      print(computer[2])


      board[int(move)] = board[int(position)]
      board[int(position)] = 0

      for i in board:
         checkMate = True
         if(i//player2 == 1 and i%player2 == 5):
            checkMate = False
            break

      if(checkMate == True):
         print("White wins!")
         break

      printBoard(board)

      computer = chessPlayer(board,player2)


      position = computer[1][0]
      print(position)

      move = computer[1][1]
      print(move)

      print(computer[2])
     
      board[move] = board[position]
      board[position] = 0
      
      for i in board:
         checkMate = True
         if(i//player2 == 1 and i%player2 == 5):
            checkMate = False
            break

      if(checkMate == True):
         print("Black wins!")
         break

      printBoard(board)
 
def printBoard(board):
   count = 0
   line = ""
   pieceT = False
   for i in board:
      if(i//10 == 1 and i != 0):
         player = 10
         pieceT = True
      elif(i//20 == 1 and i != 0):
         player = 20
         pieceT = True
      else:
         pieceT = False

      count = count + 1
      if(pieceT == True):
         piece = i%player
         
         if(player == 10):
            if(i%player == 0):
               line = line + "♙"
            if(i%player == 1):
               line = line + "♘"
            if(i%player == 2):
               line = line + "♗"
            if(i%player == 3):
               line = line + "♖"
            if(i%player == 4):
               line = line + "♕"
            if(i%player == 5):
               line = line + "♔"

         elif(player == 20):
            if(i%player == 0):
               line = line + "♟"
            if(i%player == 1):
               line = line + "♞"
            if(i%player == 2):
               line = line + "♝"
            if(i%player == 3):
               line = line + "♜"
            if(i%player == 4):
               line = line + "♛"
            if(i%player == 5):
               line = line + "♚"

      else:
         line = line + " "

      if(count > 7):
         print(line)
         line = ""
         count = 0

   return True
          
         
main()      

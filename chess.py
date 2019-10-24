from chessPlayer import *
from tree import *

def main():

   board = [0]*64

   for i in range(8,16,1):
      board[i] = 10
      board[40+i] = 20

   board[0] = 13
   board[18] = 11
   board[2] = 12
   board[3] = 14
   board[4] = 15
   board[51] = 12
   board[22] = 11
   board[7] = 13
   board[14] = 0
   board[22] = 11

   board[56] = 23
   board[57] = 21
   board[58] = 22
   board[59] = 24
   board[60] = 25
   board[61] = 22
   board[45] = 21
   board[62] = 23

   #positions = GetPlayerPositions(board,10)
   #positions2 = GetPlayerPositions(board,20)
 
   #print(positions)
   #print(positions2)

   #pawn8 = GetPieceLegalMoves(board,8)
   #pawn10 = GetPieceLegalMoves(board,10)

   #print(pawn8)
   #print(pawn10)

   #knight1 = GetPieceLegalMoves(board,1)

   #print(knight1)

   #rook0 = GetPieceLegalMoves(board,0)

   #print(rook0)

   #bishop2 = GetPieceLegalMoves(board,16)

   #print(bishop2)

   #queen3 = GetPieceLegalMoves(board,3)

   #print(queen3)

   #king4 = GetPieceLegalMoves(board,4)

   #print(king4)

   #print(IsPositionUnderThreat(board,52,20))

   print(getAllMoves(board,10))
   #t = createTree(board,20,[-1,-1],0)

   print(boardEvalBoard(board))
   #t.traverse()

   #value = minimax(10,t,0,float('-Inf'),float('Inf'))

   #for i in t.children:
   #   print(i.value)
   #   if i.value == value:
   #      print(i.move)
   
   #print(value)

   #levelO = t.Get_LevelOrder(t)
 
   l = chessPlayer(board,20)
   print(l[1])

   #print(levelO)

main()


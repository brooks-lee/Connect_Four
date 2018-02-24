import random
import time

class Game:
	Rows = 6
	Columns = 7
	CountToTake = 4
	lastMove = -1
	lastScore = 0
	StartTime = time.time()

	def __init__(self,player,opponent,timeout):
		self.player = player
		self.opponent = opponent
		self.numMoves = 0
		self.movesOrder = []
		self.SetMovesOrder()
		#print self.movesOrder
		self.zTable = ZobristTable()
		self.tTable = TranspositionTable()
		self.timeoutTime = timeout

	def numFilledCells(self,board):
		count = 0
		for i in range(0,Game.Rows):
			for j in range(0,Game.Columns):
				if(board[i][j]!=0):
					count+=1
		return count

	def isMoveLeft(self,board):
		for i in range(0,Game.Rows):
			for j in range(0,Game.Columns):
				if(board[i][j] == 0):
					return True
		return False

	def movesLeft(self,board):
		count = 0
		for i in range(0,Game.Rows):
			for j in range(0,Game.Columns):
				if board[i][j] == 0:
					count += 1
		return count

	def SetMovesOrder(self):
		for i in range(0,Game.Columns):
			self.movesOrder.append(Game.Columns/2 + (1-2*(i%2))*(i+1)/2)

	def getScore(self,board,turn):	
		scr = []	
		for i in range(0,Game.Columns):
			
			if(self.Check(board,i,self.player)):
				scr.append (10)#(Game.Rows*Game.Columns -self.numMoves)/2)
				return 10#(Game.Rows*Game.Columns -self.numMoves)/2
			elif(self.Check(board,i,self.opponent)):
				scr.append (-10)#1*(Game.Rows*Game.Columns -self.numMoves)/2)
				return -10#*(Game.Rows*Game.Columns -self.numMoves)/2
		'''
		if turn == self.player:
			if 10 in scr:
				return 10
			elif -10 in scr:
				return -10
		else:
			if -10 in scr:
				return -10
			elif 10 in scr:
				return 10
		'''
		return 0

	def CheckState(self,board,c,player):
		h = Game.Rows - self.GetHeight(board,c)

		#horizontal
		if h < 6:
			count = 0
			for y in [-1,1]:
				i = h
				j = c + y
				while i >= 0 and i < Game.Rows and j >= 0 and j < Game.Columns and board[h][c] == player:
					if board[i][j] == player:
						count += 1
						j += y
					else:
						break
				if count >= Game.CountToTake-1:
					return True

		#vertical
		if(self.GetHeight(board,c) >= Game.CountToTake):
			(w,x,y,z) = board[h][c], board[h+1][c], board[h+2][c], board[h+3][c]
			if (w,x,y,z).count(player) >= Game.CountToTake:
				return True

		#diagonal
		if h >= 6:
			h-=1
		count =0
		for x,y in [(-1,-1),(1,1)]:
			i = h + x
			j = c + y
			while i >= 0 and i < Game.Rows and j >= 0 and j < Game.Columns and board[h][c] == player:
				if board[i][j] == player:
					count+=1
					i+=x
					j+=y
				else:
					break
			if count >= Game.CountToTake-1:
				return True

		#print "check diagonal right alignment"
		count =0
		for x,y in [(1,-1),(-1,1)]:
			i = h + x
			j = c + y
			while i >= 0 and i < Game.Rows and j >= 0 and j < Game.Columns and board[h][c] == player:
				if board[i][j] == player:
					count+=1
					i+=x
					j+=y
				else:
					break
			if count >= Game.CountToTake-1:
				return True
		return False

	def Check(self,board,c,player):
		h = Game.Rows-self.GetHeight(board,c)
		h-=1

		#print "check vertical alignment"
		#check vertical		
		if(self.GetHeight(board,c) >= Game.CountToTake-1):
			(w,x,y) = board[h+1][c],board[h+2][c], board[h+3][c]
			if (w,x,y).count(player) >= Game.CountToTake-1:
				return True

		#print "check horizontal alignment"
		count = 0
		for y in [-1,1]:
			i = h
			j = c - y
			while i >= 0 and i < Game.Rows and j >= 0 and j < Game.Columns:
				if board[i][j] == player:
					count += 1
					j -= y
				else:
					break
			if count >= Game.CountToTake-1:
				return True

		
		#diagonal
		#print "check diagonal left alignment"
		count =0
		for x,y in [(-1,-1),(1,1)]:
			i = h + x
			j = c + y
			while i >= 0 and i < Game.Rows and j >= 0 and j < Game.Columns:
				if board[i][j] == player:
					count+=1
					i+=x
					j+=y
				else:
					break
			if count >= Game.CountToTake-1:
				return True

		#print "check diagonal right alignment"
		count =0
		for x,y in [(1,-1),(-1,1)]:
			i = h + x
			j = c + y
			while i >= 0 and i < Game.Rows and j >= 0 and j < Game.Columns:
				if board[i][j] == player:
					count+=1
					i+=x
					j+=y
				else:
					break
			if count >= Game.CountToTake-1:
				return True
		
		return False

	def Playable(self,board,c):
		if self.GetHeight(board,c)< Game.Rows:
			return True
		return False

	def GetHeight(self,board,c):
		for i in range(0,Game.Rows):
			if board[i][c] != 0:
				return Game.Rows - i
		if i == Game.Rows-1:
			return 0


	def MiniMax(self, board,depth,turn,alpha,beta,distance):
		#print Game.lastMove
		isWin = self.CheckState(board,Game.lastMove,(1+turn%2))
		#print isWin ," for player ",(1+turn%2), " for col ",Game.lastMove
		if isWin and (1+turn%2)==self.player:
			return 10 -(depth-1)
		if isWin and (1+turn%2) == self.opponent:
			return -10 + (depth-1)
		#print "score from getscore for player ",turn," is ",score
		#if score == 10:
		#	return score
		#elif score == -10:
		#	return score
		

		if(self.numMoves == Game.Rows * Game.Columns):
			return 0

		if distance <= 0 or time.time() >= self.timeoutTime + self.StartTime:
			return 0

		key = self.zTable.ComputeHash(board)
		index = key%TranspositionTable.Size

		tTable_value = self.tTable.GetKey(key)
		if( len(tTable_value) > 0):
			bestScore = tTable_value[-1]
			if turn == self.player:
				alpha=max(alpha,bestScore)
			elif turn == self.opponent:
				beta = min(beta,bestScore)
			return bestScore

		bestScore = -1000
		if(turn == self.opponent):
			bestScore *= -1

		

		for i in self.movesOrder:
			if self.Playable(board,i):
				ind = Game.Rows - self.GetHeight(board,i) - 1
				#print "putting data in cell ",ind,i
				self.numMoves += 1
				board[ind][i] = turn
				'''
				print '********** Player ',turn,' ',(ind,i),'****************'
				for j in range(0,Game.Rows):
					print board[j]
				print '**************************'
				'''
				Game.lastMove  = i
				minimaxMove = self.MiniMax(board,depth+1,(1+turn%2),alpha,beta,distance-1)
				Game.lastScore = minimaxMove	
				#print "score returned for col ",i," for player ",turn, " is ",minimaxMove
				board[ind][i] = 0
				if(turn == self.player):
					bestScore = max(bestScore,minimaxMove)
					alpha = max(alpha,bestScore)
					if(beta<=alpha):
						break
				elif(turn == self.opponent):
					bestScore = min(bestScore,minimaxMove)
					beta = min(beta,bestScore)
					if(beta<=alpha):
						break
				self.tTable.Put(key,[key,depth,bestScore])


		return bestScore

	def Solve(self,board):
		self.numMoves = self.numFilledCells(board)
		maxDistance = 10
		for distance in range(0,maxDistance):
			if time.time() > self.StartTime + self.timeoutTime:
				break
			bestScore = -1000
			bestMove = -1
			#print self.Playable(board,1)
			
			for i in self.movesOrder:
				if self.Playable(board,i):
					#print "playing cell ",(Game.Rows - self.GetHeight(board,i) - 1,i)
					ind = Game.Rows - self.GetHeight(board,i) - 1
					board[ind][i] = self.player
					Game.lastMove = i
					#print '********** Player 1 ',(i),'****************'
					#for j in range(0,Game.Rows):
					#	print board[j]
					#print '**************************'
					scr = self.MiniMax(board,0,2,-1000,1000,distance)
					Game.lastScore = scr
					#print scr ," for player 1 is ",i
					board[ind][i] = 0
					self.numMoves = 0
					if scr > bestScore:
						bestScore = scr
						bestMove = i
		
		#print "The move and the score is ",bestMove,bestScore
		return bestMove

class ZobristTable:
	_ZobristTable = []
	Rows = 6
	Columns = 7
	numPlayers = 2
	def __init__(self):
		for i in range(0,ZobristTable.Rows):
			ZobristTable._ZobristTable.append([])
			for j in range(0,ZobristTable.Columns):
				ZobristTable._ZobristTable[i].append([])
				for k in range(0,ZobristTable.numPlayers):
					ZobristTable._ZobristTable[i][j].append(random.getrandbits(32))

	def ComputeHash(self,board):
		h=0
		for i in range(0,ZobristTable.Rows):
			for j in range(0,ZobristTable.Columns):
				if board[i][j] != 0:
					player = board[i][j]-1 
					h ^= ZobristTable._ZobristTable[i][j][player]
		return h

class TranspositionTable:
	_TranspositionTable = []
	Size = 1000
	def __init__(self):
		for i in range(0,TranspositionTable.Size):
			TranspositionTable._TranspositionTable.append([0,0,0])#key,depth,score
	def GetKey(self,key):
		ind = key % TranspositionTable.Size
		if (TranspositionTable._TranspositionTable[ind][0] == key):
			return TranspositionTable._TranspositionTable[ind][1:]
		return []

	def Put(self,key,value):
		ind = key % TranspositionTable.Size
		TranspositionTable._TranspositionTable[ind]=value

#g = Game(1,2)
'''
g.Solve([	[2,0,0,0,0,0,2],
			[1,0,0,0,0,0,1],
			[2,2,0,0,2,0,1],
			[1,2,1,1,1,0,2],
			[2,2,1,2,2,0,1],
			[1,1,2,1,1,0,1]])
'''



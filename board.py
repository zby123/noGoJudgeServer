import numpy as np


class Board(object):
	def __init__(self, json_dict):
		self.board = np.ones((9, 9), dtype=int) * 2
		self.side = 0
		self.recordColor = 0
		self.st = True
		self.flag = 2
		self.record_json = json_dict

	def record(self, loc):
		output = {}
		if self.recordColor == 0:
			output['kind'] = 'black'
		else:
			output['kind'] = 'white'
		output['posx'] = loc[0]
		output['posy'] = loc[1]
		self.record_json["step"].append(output)
		self.recordColor = 1 - self.recordColor

	def update(self, loc):
		x = loc[0]
		y = loc[1]
		if self.st and x == 4 and y == 4:
			return 'invalid move'
		self.st = False
		if (x < 0 or x > 8 or y < 0 or y > 8):
			return 'invalid place to put your pawn'
		elif self.board[x][y] != 2:
			return 'already has a pawn in this block'
		else:
			self.record(loc)
		self.board[x][y] = self.side
		vis = set()
		go = [[0, 1], [0, -1], [1, 0], [-1, 0]]

		def dfs(x, y, fx, fy):
			if x < 0 or x > 8 or y < 0 or y > 8:
				return False
			if self.board[x][y] == 2:
				return True
			if fx != -1 and self.board[x][y] != self.board[fx][fy]:
				return False
			if (x, y) in vis:
				return False
			vis.add((x, y))
			ret = False
			for direct in go:
				nx = x + direct[0]
				ny = y + direct[1]
				if nx != fx or ny != fy:
					ret |= dfs(nx, ny, x, y)
			return ret

		end_flag = True
		for i in range(9):
			for j in range(9):
				if (i, j) not in vis:
					end_flag &= dfs(i, j, -1, -1)
		if not end_flag:
			self.flag = self.side
		self.side = 1 - self.side
		return True
		

	def result(self):
		return self.flag

import numpy as np
class Player:
	def __init__(self):
		self.bust = False
		self.total = 0
		self.cards = []
	def __str__(self):
		s = "HandVal:"+str(self.total)+" \n"
		s+= "Cards: "
		for card in self.cards:
			s+= card['color']+str(card['val'])+" , "
		return s

	def reset(self):
		self.bust = False
		self.total = 0
		self.cards = []
	def add_card(self, card):
		if card['color']=='b':
			self.total+= card['val']
		elif card['color']=='r': 
			self.total-= card['val']
		else:
			raise ValueError("Card color(%s) was neither 'b' nor 'r'"%card['color'])
		self.cards.append(card)
		if self.total>21 or self.total<1:
			self.bust = True

class Engine:
	def __init__(self, n = 1):
		if n<1:
			raise ValueError('n has to be greater than or equal to one')
		self.n = n
		self.dealer = Player()
		self.players = [Player() for _ in range(n)]
		self.done = False
		self.reset()
	
	def show_state(self):
		print("Done:",self.done)
		print("Dealer:"+str(self.dealer)+'\n---------------------------------')
		for i,player in enumerate(self.players):
			print("Player %d:"%(i+1),str(player)+'\n---------------------------------')
	def reset(self):
		#Picking the first two cards
		self.dealer = Player()
		self.players = [Player() for _ in range(self.n)]
		self.dealer.add_card(self.pick_card(black=True))
		for player in self.players:
			player.add_card(self.pick_card(black=True))


	def hit(self, player_num):
		if self.done:
			print('Game over! Please call reset()')
			return
		card = self.pick_card()
		if player_num==-1:
			self.dealer.add_card(card)
			if self.dealer.bust:
				print('Dealer has gone bust')
				self.done= True
		else:
			self.players[player_num].add_card(card)
			if self.players[player_num].bust:
				print('Player number %d has gone bust'%(player_num))
				self.done=True
	def pick_card(self, black=False):
		num = np.random.randint(1, 11)
		color_prob = np.random.uniform(0, 1)
		black_thresh = 1.0/3.0
		if color_prob>black_thresh or black:
			color = 'b'
		else:
			color = 'r'
		card = {'val':num, 'color':color}
		return card
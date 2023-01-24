from fltk import *
import socket, sys

class game(Fl_Window):
	def __init__(self,w,h,l):
		Fl_Window.__init__(self,300,300,w,h,l)
		self.begin()
		self.shipimg = Fl_PNG_Image('ship.png').copy(50,50)
		self.hitimg = Fl_PNG_Image('hit.png').copy(50,50)
		self.seaimg = Fl_PNG_Image('blank.png').copy(50,50)
		self.miss_img = Fl_PNG_Image('miss.png').copy(50,50)
		
		self.cords = []
		self.clientbl = []
		self.oppbl = []
		self.ships = []
		self.ships_taken_out = []
		self.opp = ''
		self.turn = 'server'
		self.total_data = []
		for row in range(5):
			for col in range(5):
				self.clientbl.append(Fl_Button(col*50+20,row*50+140,50,50))
				self.clientbl[-1].image(self.seaimg)
				self.clientbl[-1].callback(self.but_callback)
				#self.bl[-1].callback(self.button_click)
				#num += 1
				self.cords.append([str(row),str(col)])
		
		for row in range(5):
			for col in range(5):
				self.oppbl.append(Fl_Button(col*50+400,row*50+140,50,50))
				self.oppbl[-1].image(self.seaimg)
				self.oppbl[-1].callback(self.but_callback)
				
				#num += 1
				#self.cords.append([row,col])
				
		self.you = Fl_Box(100,110,80,40,'You')
		self.enemy = Fl_Box(500,110,80,40,'Enemy')
		self.game_message = Fl_Box(300,20,150,40)
		self.game_message.label('Waiting for opponent')
		#self.game_message.hide()
		self.redraw()
		self.end()
		self.sock = None
		self.game_state = 'Inactive'

		
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #fd=3
		if sys.argv[1] == 'server':
			self.sock.bind((sys.argv[2],int(sys.argv[3])))
			self.sock.listen()
			fdl=self.sock.fileno() #listening fd
			Fl.add_fd(fdl, self.acceptConnection) 
		
		elif sys.argv[1] == 'client':
			self.sock.connect((sys.argv[2],int(sys.argv[3])))
			self.fd=self.sock.fileno()
			Fl.add_fd(self.fd, self.receive_data)
			self.sock.sendall('hie'.encode())
			self.planning_phase()
			
		
	def acceptConnection(self, fdl): #runs when data comes to socket s
		self.conn, raddr = self.sock.accept()
		fd=self.conn.fileno() #file descriptor for new established connection
		Fl.add_fd(fd, self.receive_data)
		


	def receive_data(self,fd):
		#  ________________________________________________________________________
		# |                              Legend                                   |
		# |																	      |
		# | a: The following cordinates were sent as a attack                     | 
		# |																          |
		# | m: The following cordinates were sent back to the attacker as a miss  |
		# |																		  |
		# | h: The following cordinates were sent back to the attacker as a hit   |
		# |																		  |
		# | L: Standalone message sent to inform the player they have lost        |
		# | 																	  |
		# |																		  |
		# |																		  |
		# |																		  |
		# |																		  |
		# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
		
		if sys.argv[1] == 'server':
			data = self.conn.recv(1024).decode()
			if data == 'hie':
				self.planning_phase()
				return None
			elif data == 'Attacking':
				if self.game_state == 'Waiting':
					self.game_message.label('Attacking')
					self.game_state ='Attacking'
					fl_message('Your turn')
					self.redraw()
				else:
					self.opp = 'ready'
				return None
		else:
			data=self.sock.recv(1024).decode()
			if data == 'Attacking':
				if self.game_state == 'Waiting':
					self.game_message.label('Attacking')
					self.game_state = 'Attacking'
					fl_message("Opponent's turn")
					self.redraw()
				else:
					self.opp = 'ready'
				return None
		print('this is data')
		print(data)
		
		
				
		if data[2] == 'a':
			if self.game_state == 'Attacking':
				if sys.argv[1] == 'server':
					self.turn = 'server'
				elif sys.argv[1] == 'client':
					self.turn = 'client'
			
			if [data[0],data[1]] in self.ships:
				info = data[0] +data[1] + 'h'
				if sys.argv[1] == 'server':
					self.conn.sendall(info.encode())
					self.clientbl[self.cords.index([data[0],data[1]])].image(self.hitimg)
						
				else:
					self.sock.sendall(info.encode())
					self.clientbl[self.cords.index([data[0],data[1]])].image(self.hitimg)
					
			else:
				info = data[0]+data[1]+'m'
				if sys.argv[1] == 'server':
					self.conn.sendall(info.encode())
					
				else:
					self.sock.sendall(info.encode())
					
				self.clientbl[self.cords.index([data[0],data[1]])].image(self.miss_img)
				self.clientbl[self.cords.index([data[0],data[1]])].deactivate() # prevent clicking again
				self.clientbl[self.cords.index([data[0],data[1]])].redraw()
		
		elif data[2] == 'h':
				self.oppbl[self.cords.index([data[0],data[1]])].image(self.hitimg)
				self.oppbl[self.cords.index([data[0],data[1]])].deactivate()
				if [data[0],data[1]] not in self.ships_taken_out:
					self.ships_taken_out.append([data[0],data[1]])
				if len(self.ships_taken_out) == 4:
					self.game_state = 'Over'
					if sys.argv[1] == 'server':
						self.conn.sendall('Lose'.encode())
						fl_message('You won')
					else:
						self.sock.sendall('Lose'.encode())
						fl_message('You won')
						
		elif data[2] == 'm':
			self.oppbl[self.cords.index([data[0],data[1]])].image(self.miss_img)
			self.oppbl[self.cords.index([data[0],data[1]])].deactivate()
			self.oppbl[self.cords.index([data[0],data[1]])].redraw()
		elif data[0] == 'L':
			fl_message('You Lose')
		
		self.redraw()

		print(self.game_state)
		
	def planning_phase(self):
		self.game_message.show()
		self.game_state = 'Planning'
		self.game_message.label(self.game_state)
		self.redraw()

	def but_callback(self,wid):
		print(self.game_state) 
		if self.game_state== 'Planning': #checking if still placing ships
			if len(self.ships) < 4:
				if wid in self.oppbl:
					return None
				if self.cords[self.clientbl.index(wid)] in self.ships:
					return None
				self.ships.append(self.cords[self.clientbl.index(wid)])
				wid.image(self.shipimg)
				wid.redraw()
				if len(self.ships) == 4:
					if self.opp != 'ready': # lets opponent's client know they are ready
						self.game_state = 'Waiting'
						self.game_message.label('Waiting for opponent')
						if sys.argv[1] == 'server':
							self.conn.sendall('Attacking'.encode())
						else:
							self.sock.sendall('Attacking'.encode())
					else: # initiates the game
						self.game_state = 'Attacking'
						self.game_message.label('Attacking')
						if sys.argv[1] == 'server':
							self.conn.sendall('Attacking'.encode())
						else:
							self.sock.sendall('Attacking'.encode())

				
		elif self.game_state == 'Attacking':
			self.send_info(wid)

	def send_info(self,wid):
		print(sys.argv[1])
		if self.turn != sys.argv[1]: # checking if it is your turn or not
			fl_message('Not your turn')
			return None
		if wid in self.clientbl:
			return None
		
		cordinate = self.cords[self.oppbl.index(wid)]
		print(cordinate)
		
		# asking opponent's client if sent cordinate is a hit or miss
		if sys.argv[1] == 'client':	
			info = cordinate[0]+cordinate[1]+'a'
			self.sock.sendall(info.encode())
			
		else:
			info = cordinate[0]+cordinate[1]+'a'
			self.conn.sendall(info.encode())
			print(info) # telling oppnent's client its asking for hit or miss
			
		if self.turn == 'server':
			self.turn = 'client'
		else:
			self.turn = 'server'


	
	
battleship = game(800,800,'game')
battleship.show()
Fl.run()

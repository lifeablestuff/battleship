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
		for row in range(5):
			for col in range(5):
				self.clientbl.append(Fl_Button(col*50+20,row*50+140,50,50))
				self.clientbl[-1].image(self.seaimg)
				self.clientbl[-1].callback(self.comms_test)
				#self.bl[-1].callback(self.button_click)
				#num += 1
				self.cords.append([row,col])
		
		for row in range(5):
			for col in range(5):
				self.oppbl.append(Fl_Button(col*50+400,row*50+140,50,50))
				self.oppbl[-1].image(self.seaimg)
				#self.oppbl[-1].callback(self.button_click)
				#num += 1
				#self.cords.append([row,col])
		self.confirm = Fl_Button(110,500,80,40,'ready')
		self.you = Fl_Box(100,110,80,40,'You')
		self.enemy = Fl_Box(500,110,80,40,'Enemy')
		#self.confirm.hide()
		self.game_message = Fl_Box(300,20,80,40)
		self.game_message.label('Game message')
		#self.game_message.hide()
		self.redraw()
		self.allow_conn = Fl_Button(260,80,150,40,'Allow connection')
		self.end()
		self.sock = None
		self.game_state = 'Inactive'
		
		conn_to_client = None
		
		host = 'localhost'
		port = 5555
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #fd=3
		if sys.argv[1] == 'server':
			self.sock.bind((host, port))
			self.sock.listen()
			fdl=self.sock.fileno() #listening fd
			Fl.add_fd(fdl, self.acceptConnection) 
		
		elif sys.argv[1] == 'client':
			self.sock.connect((host,port))
			self.fd=self.sock.fileno()
			Fl.add_fd(self.fd, self.receive_data)
			
		
	def acceptConnection(self, fdl): #runs when data comes to socket s
		conn, raddr = self.sock.accept()
		fd=conn.fileno() #file descriptor for new established connection
		Fl.add_fd(fd, self.recv_data)
		self.other_person=conn #add fd(key) and conn(value) to connD dict
		

	def confirm_conn(self):
		if sys.argv[2] == 'server':
			return None
		
		else:
			self.sock.sendto('connect',(self.host,self.port))
		
	def recv_data(self,fd):
		data= self.conn_to_client.recv(1024)
		print(data)

	def receive_data(self,fd):
		data=self.sock.recv(1024)
		print(data)

	def planning_phase(self):
		self.game_message.show()
		self.isplanning = 'Planning'
	
	def but_callback(self,wid):
		if self.isplanning == 'Planning': #checking if still planning
			if len(self.boats) < 4:
				if wid in self.oppbl:
					return None
				self.boats.append(self.cords[self.client_but.index(wid)])
	
	def comms_test(self,wid):
		self.sock.sendall((self.cords[self.clientbl.index(wid)]).encode())


	
	
battleship = game(800,800,'game')
battleship.show()
Fl.run()

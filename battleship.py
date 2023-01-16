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
				self.clientbl.append(Fl_Button(col*50+20,row*50+80,50,50))
				self.clientbl[-1].image(self.seaimg)
				#self.bl[-1].callback(self.button_click)
				#num += 1
				self.cords.append([row,col])
		
		for row in range(5):
			for col in range(5):
				self.oppbl.append(Fl_Button(col*50+400,row*50+80,50,50))
				self.oppbl[-1].image(self.seaimg)
				#self.oppbl[-1].callback(self.button_click)
				#num += 1
				#self.cords.append([row,col])
		self.confirm = Fl_Button(20,350,80,40,'ready')
		self.you = Fl_Box(100,20,80,40,'You')
		self.enemy = Fl_Box(500,20,80,40,'Enemy')
		self.confirm.hide()
		self.redraw()
		self.end()
		self.sock = None
		'''
		self.host = sys.argv[2]
		self.port=int(sys.argv[3])
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		if sys.argv[1] == "server":
			self.sock.bind((self.host, self.port)) # servers bind
		
		
		fd=self.sock.fileno()
		Fl.add_fd( fd, self.receive_data)
		self.confirm_conn()
		'''
	def confirm_conn(self):
		if sys.argv[2] == 'server':
			return None
		
		else:
			self.sock.sendto('connect',(self.host,self.port))
		
	def recv_data(self,fd):
		message = []
		(text, self.addr)=self.s.recvfrom(1024)
		message = (text.decode())
		
		if message == 'connect':
			self.sock.sendto('confirmed',(self.addr))
			fl_message('a player has connected')
			fl_message('planning phase has started')
			
		elif message == 'confirmed':
			fl_message('connection confirmed')
			fl_message('planning phase has started')
			
	def planning_phase(self,wid):
		return None
	
		
	
	
battleship = game(800,800,'game')
battleship.show()
Fl.run()

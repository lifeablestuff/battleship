from fltk import *
import socket

class game(Fl_Window):
	def __init__(self,w,h,l):
		Fl_Window.__init__(self,300,300,w,h,l)
		self.begin()
		self.address = Fl_Input(80,40,150,20,'address')
		self.port = Fl_Input(80,40,150,20,'port')
		self.address.when(FL_WHEN_ENTER_KEY)
		self.address.callback(self.get_addr,'address',self.address.value())
		self.port.when(FL_WHEN_ENTER_KEY)
		self.address.callback(self.get_addr,'port',self.port.value())
		self.address.hide()
		self.port.hide()
		self.ip = None
		self.port_val = None
		
		self.bl = []
		for row in range(10):
			for col in range(10):
				self.bl.append(Fl_Button(col*40+20,row*40+80,40,40))
				#elf.bl[-1].callback(self.button_click)
				#num += 1
				#self.cords.append([row,col])
		
		for row in range(10):
			for col in range(10):
				self.bl.append(Fl_Button(col*40+480,row*40+80,40,40))
				#elf.bl[-1].callback(self.button_click)
				#num += 1
				#self.cords.append([row,col])
		
		self.find_game = Fl_Button(20,10,70,30)
		self.find_game.label('connect')
		self.find_game.callback(self.get_addr,'callback')
		
		
	def get_addr(self,w,who,value=None):
		print(who)
		if value == None:
			self.address.show()
			return None
			
		elif who == 'address':
			self.address = value
			self.address.hide()
			self.port.show()
		elif who == 'port':
			try:
				self.port_val = int(value)
			
			except:
				fl_message('please enter a valid port')
			
			
	
battleship = game(900,500,'game')
battleship.show()
Fl.run()

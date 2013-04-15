import serial
import io

class SerialConnection(object):
	_instance = None
	conn = None
	iowrapper = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = \
				super(SerialConnection,cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def is_connected(self):
		return self.conn != None
	
	def poll(self):
		return self.iowrapper.readline().strip()

	def update_connection(self, status):
		if status:
			if(self.conn):
				self.conn.close()
			self.conn = \
				serial.Serial(port=3, baudrate=115200, timeout=0.01)
			self.conn.close()
			self.conn.open()
			self.iowrapper = \
				io.TextIOWrapper(io.BufferedRWPair(self.conn,self.conn,2))
		else:
			if(self.conn):
				self.conn.close()
				self.conn = None
				self.iowrapper = None
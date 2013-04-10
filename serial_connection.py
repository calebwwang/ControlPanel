class SerialConnection(object):
	_instance = None
	connection = False
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(SerialConnection,cls).__new__(cls, *args, **kwargs)
		return cls._instance

def update_connection(connection_status):
	if(connection_status):
		print "connecting"
		connection = True
	else:
		print "disconnecting"
		connection = False
	return None
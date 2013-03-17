import serial_connection

def motor_move(motor, speed):
	print("Sent move command to motor %s with speed %s" % (motor, speed))
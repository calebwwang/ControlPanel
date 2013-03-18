import serial_connection

def motor_move(motor, speed):
	print("Sent move command to motor %s with speed %s" \
		% (motor, speed))

def robot_move(direction, speed):
	print("Sent robot move command with direction %s and speed %s" \
		% (direction, speed))

def emergency_stop():
	print("e-stop hit")
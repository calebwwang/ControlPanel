import os
os.environ['ETS_TOOLKIT'] = 'qt4'

import enaml
from enaml.stdlib.sessions import simple_session
from enaml.qt.qt_application import QtApplication
from enaml.qt.qt.QtCore import QTimer, SIGNAL

import serial_connection
import robot_interface

robot = robot_interface.RobotInterface()

def update():
	conn = serial_connection.SerialConnection();
	if conn.is_connected():
		commandstr = conn.poll()
		if commandstr:
			robot.log(commandstr)

from PySide.QtCore import *
from PySide.QtGui import *

if __name__ == '__main__':
	with enaml.imports():
		from control_panel import Main
	session = simple_session('main','main window',Main)
	app = QtApplication([session])

	timer = QTimer()
	timer.connect(timer, SIGNAL("timeout()"), update)
	timer.start(10)

	app.start_session('main')
	app.start()
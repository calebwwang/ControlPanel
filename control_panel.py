import enaml
from enaml.stdlib.sessions import simple_session
from enaml.qt.qt_application import QtApplication
from enaml.qt.qt.QtCore import QTimer, SIGNAL

import os
os.environ['ETS_TOOLKIT'] = 'qt4'

import serial_connection

def update():
	print serial_connection.SerialConnection().connection

if __name__ == '__main__':
	with enaml.imports():
		from control_panel import Main
	session = simple_session('main','main window',Main)
	app = QtApplication([session])

	timer = QTimer()
	timer.connect(timer, SIGNAL("timeout()"), update)
	timer.start(1000)

	app.start_session('main')
	app.start()
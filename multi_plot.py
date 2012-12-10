#!/usr/bin/env python
"""
Demonstrates the plot responding to data updates while remaining responsive
to user interaction.  Panning and Zooming work as described in simple_line.py

There is a timer set which modifies the data that is passed to the plot.
Since the axes and grids automatically determine their range from the
dataset, they rescale each time the data changes.  This gives the zooming
in and out behavior.  As soon as the user interacts with the plot by panning
or manually zooming, the bounds of the axes are no longer "auto", and it
becomes more apparent that the plot's data is actually changing as a
function of time.

Original inspiration for this demo from Bas van Dijk.
"""

# Major library imports
import wx
from numpy import arange,zeros,roll
from scipy.special import jn
import serial
import io

# Enthought library imports
from enable.api import Component
from enable.component_editor import ComponentEditor

# Chaco imports
from chaco.api import create_line_plot, add_default_axes, add_default_grids, GridContainer
from traits.api import HasTraits, Instance, Enum
from traitsui.api import Item, View, Group

def _create_plot_component():
	container = GridContainer(padding=40, fill_padding=True,
		bgcolor="lightgray", use_backbuffer=True,
		shape=(3,3), spacing=(10,10))

	x = arange(100)
	y = arange(100)
	plot = create_line_plot((x,y), color="red", width=2.0, index_bounds=(-5,100), value_bounds=(-5,90))
	plot.padding = 50
	plot.fill_padding = True
	plot.bgcolor = "white"
	left, bottom = add_default_axes(plot, vtitle="Roll (degrees)", htitle="Time (s)")
	hgrid, vgrid = add_default_grids(plot)
	bottom.tick_interval = 20.0
	vgrid.grid_interval = 10.0
	container.add(plot)
	
	x = arange(100)
	y = arange(100)
	plot = create_line_plot((x,y), color="red", width=2.0, index_bounds=(-5,100), value_bounds=(-5,90))
	plot.padding = 50
	plot.fill_padding = True
	plot.bgcolor = "white"
	left, bottom = add_default_axes(plot, vtitle="Pitch (degrees)", htitle="Time (s)")
	hgrid, vgrid = add_default_grids(plot)
	bottom.tick_interval = 20.0
	vgrid.grid_interval = 10.0
	container.add(plot)
	
	x = arange(100)
	y = arange(100)
	plot = create_line_plot((x,y), color="red", width=2.0, index_bounds=(-5,100), value_bounds=(-5,365))
	plot.padding = 50
	plot.fill_padding = True
	plot.bgcolor = "white"
	left, bottom = add_default_axes(plot, vtitle="Yaw (degrees)", htitle="Time (s)")
	hgrid, vgrid = add_default_grids(plot)
	bottom.tick_interval = 20.0
	vgrid.grid_interval = 10.0
	container.add(plot)
	
	x = arange(100)
	y = arange(100)
	plot = create_line_plot((x,y), color="red", width=2.0, index_bounds=(-5,100), value_bounds=(-100,100))
	plot.padding = 50
	plot.fill_padding = True
	plot.bgcolor = "white"
	left, bottom = add_default_axes(plot, vtitle="Gyro X", htitle="Time (s)")
	hgrid, vgrid = add_default_grids(plot)
	bottom.tick_interval = 20.0
	vgrid.grid_interval = 10.0
	container.add(plot)
	
	x = arange(100)
	y = arange(100)
	plot = create_line_plot((x,y), color="red", width=2.0, index_bounds=(-5,100), value_bounds=(-100,100))
	plot.padding = 50
	plot.fill_padding = True
	plot.bgcolor = "white"
	left, bottom = add_default_axes(plot, vtitle="Gyro Y", htitle="Time (s)")
	hgrid, vgrid = add_default_grids(plot)
	bottom.tick_interval = 20.0
	vgrid.grid_interval = 10.0
	container.add(plot)
	
	x = arange(100)
	y = arange(100)
	plot = create_line_plot((x,y), color="red", width=2.0, index_bounds=(-5,100), value_bounds=(-100,100))
	plot.padding = 50
	plot.fill_padding = True
	plot.bgcolor = "white"
	left, bottom = add_default_axes(plot, vtitle="Gyro Z", htitle="Time (s)")
	hgrid, vgrid = add_default_grids(plot)
	bottom.tick_interval = 20.0
	vgrid.grid_interval = 10.0
	container.add(plot)
	
	x = arange(100)
	y = arange(100)
	plot = create_line_plot((x,y), color="red", width=2.0, index_bounds=(-5,100), value_bounds=(-1,35))
	plot.padding = 50
	plot.fill_padding = True
	plot.bgcolor = "white"
	left, bottom = add_default_axes(plot, vtitle="Battery Voltage (V)", htitle="Time (s)")
	hgrid, vgrid = add_default_grids(plot)
	bottom.tick_interval = 20.0
	vgrid.grid_interval = 10.0
	container.add(plot)

	return container

class Viewer(HasTraits):
	plot = Instance(Component)
	traits_view = View(
		Group(
			Item('plot', editor=ComponentEditor(size=(1000,800)), 
				show_label=False, ),
			orientation = "vertical"),
		resizable=True,
		title="Ballbot Data Feed")
	
	def _plot_default(self):
		return _create_plot_component()
	
	def create_data(self):
		self.numpoints = 100
		self.x = arange(self.numpoints)
		self.roll = zeros(self.numpoints)
		self.pitch = zeros(self.numpoints)
		self.heading = zeros(self.numpoints)
		self.gyrox = zeros(self.numpoints)
		self.gyroy = zeros(self.numpoints)
		self.gyroz = zeros(self.numpoints)
		self.batvol = zeros(self.numpoints)

"""
	def __init__(self):
		self._create_data()
        
		plot = create_line_plot((self.x,self.roll), color="red", width=2.0, index_bounds=(-5,100), value_bounds=(-5,90))
		plot.padding = 50
		plot.fill_padding = True
		plot.bgcolor = "white"
		left, bottom = add_default_axes(plot, vtitle="Rotation around X (degrees)", htitle="Time (s)")
		hgrid, vgrid = add_default_grids(plot)
		bottom.tick_interval = 20.0
		vgrid.grid_interval = 10.0
		self.rollplot = plot
        
		container = GridPlotContainer(shape=(3,3), spacing=(1.0,1.0))
		container.add(self.rollplot)
"""

class Controller(HasTraits):
	viewer = Instance(Viewer)

	foo = Enum("blah")
	view = View(Item('foo'), buttons=['OK'], resizable=True)

	def init_serial(self):
		self.ser = serial.Serial()
		self.ser.port = 3
		self.ser.baudrate = 115200
		self.ser.timeout = 0.01
		self.ser.open()
		self.sio = \
			io.TextIOWrapper(io.BufferedRWPair(self.ser,self.ser,1))
	
	def onTimer(self, event):
		self.ser.write("}S\n")
		retstring = self.sio.readline()
		if len(retstring) == 0:
			pass
		vals = retstring.strip().split()
		vals = [ float(v) for v in vals ]
		if len(vals) == 7:
			self.viewer.roll = roll(self.viewer.roll,-1)
			self.viewer.roll[-1] = vals[0]
			self.viewer.plot.components[0].value.set_data(self.viewer.roll)

			self.viewer.pitch = roll(self.viewer.pitch,-1)
			self.viewer.pitch[-1] = vals[1]
			self.viewer.plot.components[1].value.set_data(self.viewer.pitch)
			
			self.viewer.heading = roll(self.viewer.heading,-1)
			self.viewer.heading[-1] = vals[2]
			self.viewer.plot.components[2].value.set_data(self.viewer.heading)
			
			self.viewer.gyrox = roll(self.viewer.gyrox,-1)
			self.viewer.gyrox[-1] = vals[3]
			self.viewer.plot.components[3].value.set_data(self.viewer.gyrox)

			self.viewer.gyroy = roll(self.viewer.gyroy,-1)
			self.viewer.gyroy[-1] = vals[4]
			self.viewer.plot.components[4].value.set_data(self.viewer.gyroy)
			
			self.viewer.gyroz = roll(self.viewer.gyroz,-1)
			self.viewer.gyroz[-1] = vals[5]
			self.viewer.plot.components[5].value.set_data(self.viewer.gyroz)
			
			self.viewer.batvol = roll(self.viewer.batvol,-1)
			self.viewer.batvol[-1] = vals[6]
			self.viewer.plot.components[6].value.set_data(self.viewer.batvol)
			for i in range(7):
				self.viewer.plot.components[i].request_redraw()

class MyApp(wx.PySimpleApp):
	def OnInit(self, *args, **kw):
		viewer = Viewer()
		viewer.create_data()

		controller = Controller(viewer = viewer)
		controller.init_serial()

		viewer.edit_traits()
		controller.edit_traits()

		self.setup_timer(controller)
		return True


	def setup_timer(self, controller):
		timerId = wx.NewId()
		self.timer = wx.Timer(self, timerId)

		self.Bind(wx.EVT_TIMER, controller.onTimer, id=timerId)

		self.timer.Start(50.0, wx.TIMER_CONTINUOUS)

if __name__ == "__main__":
	app = MyApp()
	app.MainLoop()

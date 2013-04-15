from chaco.api import ArrayPlotData, Plot, add_default_axes, GridContainer,create_line_plot,add_default_grids
from traits.api import HasTraits, Instance, Array
from traitsui.api import View, Item, Group

from numpy import linspace, zeros, roll, arange
from scipy.special import jn

from collections import deque
import datetime

#class TimeSeriesPlotModel(HasTraits):
#	plot = Instance(Plot)
#
#	data = Array
#
#	def __init__(self, **kwargs):
#		super(TimeSeriesPlotModel, self).__init__()
#
#		x = linspace(-5,10,100)
#
#		plot_data = ArrayPlotData(x=x,y=jn(0,x))
#		self.plot = Plot(plot_data)
#		self.plot.plot(("x","y"), type="line", color="blue")
#		add_default_axes(self.plot, vtitle="foo", htitle="bar")

class DataFeed(object):
	def __init__(self, ytitle, max_pts):
		self.ytitle = ytitle
		self.data = zeros(max_pts)
		self.plothandle = None

	def add_points(self, pts):
		self.data.extend(pts)

		if(self.plothandle):
			pass
			# update plot

	def init_plot(self):
		x = arange(100)
		y = arange(100)
		self.plothandle = create_line_plot((x,y), color="red", width=2.0, 
						index_bounds=(-5,100), value_bounds=(-100,100))
		self.plothandle.padding = 50
		self.plothandle.fill_padding = True
		self.plothandle.bgcolor = "white"
		left, bottom = add_default_axes(self.plothandle, 
							vtitle=self.ytitle, htitle="Time (s)")
		hgrid, vgrid = add_default_grids(self.plothandle)
		bottom.tick_interval = 20.0
		vgrid.grid_interval = 10.0

		return self.plothandle

class RobotInterface(object):
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = \
				super(RobotInterface,cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		self.command_buffer = deque()
		self.log_buffer = deque(maxlen=100)
		self.plots = []

		test_df = DataFeed('X Position',100)
		test_df.init_plot()
		self.plots.append(test_df)

		test_df2 = DataFeed('X Position 2',100)
		test_df2.init_plot()
		self.plots.append(test_df2)

	def log(self, commandstr):
		cmd = (commandstr, datetime.datetime.now())
		self.log_buffer.append(cmd)
		print "[%s] %s" % (cmd[1].strftime("%H:%M:%S.%f")[:-3],cmd[0])

	def motor_move(self, motor, speed):
		print("Sent move command to motor %s with speed %s" \
			% (motor, speed))

	def robot_move(self, direction, speed):
		print("Sent robot move command with direction %s and speed %s" \
			% (direction, speed))

	def get_plots(self):
		#return [p.plothandle for p in self.plots]
		gc = GridContainer(padding=20, fill_padding=True,
			bgcolor='lightgray', use_backbuffer=True, 
			shape=(3,3), spacing=(10,10))
		[gc.add(p.plothandle) for p in self.plots]
		return gc
		#return View(Group(Item('plot')),title="fuck")

	def emergency_stop(self):
		print("e-stop hit")
import pyglet
from pyglet.window import key
from pgedraw import basic as Prims #Primatives
import pgedraw

from Structures import Pod
from Structures import Clock
from Structures import Node
import ObjectRegistry
import logging
import Config
import subprocess
import time
from threading import Thread


## Subclass window
class Interface(pyglet.window.Window):
	BG_COLOR = (176, 163, 156, 255)
	X_ZERO = 0
	Y_ZERO = 0

	GENERAL = 'general'
	CASE_1 = 'case_1'
	CASE_2 = 'case_2'

	def __init__(self, w, h, c):
		logger.debug("__init__")
		logger.debug('window_width: {}'.format(w))
		logger.debug('window_height: {}'.format(h))

		pyglet.window.Window.__init__(self, width=w, height=h, caption=c)    		

		## Clock Instance
		self.master_clock = Clock()

		## Default Case
		self.current_case = Interface.CASE_1

		## Set Width & Height
		self.window_width = w
		self.window_height = h
		
		## Set Coordinates
		self.X_ZERO = 0
		self.Y_ZERO = 0

		## Create Batches and Groups
		self.group_a = pyglet.graphics.OrderedGroup(0)
		self.group_b = pyglet.graphics.OrderedGroup(1)
		self.group_c = pyglet.graphics.OrderedGroup(2)

		self.general_batch = pyglet.graphics.Batch()
		self.case1_batch = pyglet.graphics.Batch()
		self.general_labels = []
		self.case_labels = []

		## Get Configs and object registries
		self.configuration = Config.Config(Interface=self)
		self.ObjReg = ObjectRegistry.ObjectRegistry(self)

		## Set AutoAdjust
		#self.configuration.AutoAdjust_ENABLED = True
		#logger.debug('AutoAdjust_ENABLED: {}'.format(self.configuration.AutoAdjust_ENABLED))

		## Initalize Periodic functions
		self.periodics = Periodic(self)

		## Start Periodic Functions
		pyglet.clock.schedule_interval(self.periodics.master_clock_ticker, self.configuration.PULSE_WIDTH)
		pyglet.clock.schedule_interval(self.periodics.event_handler, 1/120.0)
		#pyglet.clock.schedule_interval(self.periodics.case_1_pod_motion, 1/60.0)
		#pyglet.clock.schedule_interval(self.periodics.case_1_check_pod_contact, 1/60.0)
		#pyglet.clock.schedule_interval(self.periodics.case_1_pod_position, 1/60.0)


        def flashDetectors(self):
                for d in self.ObjReg.d_field_registry:
                    thread = Thread(target = self.startFlashThread, args = (d, ))
                    thread.start()
                   

        def startFlashThread(self, d):
                d.visible = True
                time.sleep(.2)
                d.visible=False

	def on_activate(self):
		logger.debug('----on_activate----')
	def on_close(self):
		logger.debug('----on_close----')
		## Delete all objects
		#for pods in self.ObjReg.pod_registry:
	#		pod.SPRITE.delete()

	def on_mouse_press(self, x, y, button, modifiers):
		for pod in self.ObjReg.pod_registry:
			pod.SPRITE.x = x
			break

	def on_draw(self):
		self.clear()
		self.general_batch.draw()
		self.case1_batch.draw()




## Class containing periodic function for an Interface
class Periodic(object):
	def __init__(self, interface):
		self.interface = interface
		self.config = Config.Config()

		## To stager clocks
		self.log_position_SET = False
		self.timer = 0


	def master_clock_ticker(self, dt):
		## Itereate through nodes and get pods within range		
		self.interface.master_clock.startPulse()
		self.interface.flashDetectors()

	def event_handler(self, dt):
		self.movePods(dt)
		self.checkNodePodContact()
		#self.checkPodProximity()

	def movePods(self, dt):
		for pod in interface.ObjReg.pod_registry:
			pod.event_handler(command=Pod.MOVE, dt=dt)
			#pod.move(dt)
			#logger.debug('pod y: {}'.format(pod.SPRITE.x))

			if pod.SPRITE.x >= self.interface.window_width: #+ pod.SPRITE.height / 2:
				pod.SPRITE.x = 0

	## Handles pod - pod interaction. 
	# Cases:
	#  1. this_pod is buffering
	#  		-> If this_pod has exited the buffer_range:
	#			-> this_pod velocity set to default
	#			-> remove this_pod's reference to bufferer_pod
	#  2. this_pod has entered buffer_range of bufferer_pod
	#		-> Set pod_buffer flag of this_pod
	#		-> this_pod is given a reference to bufferer_pod
	# 		-> this_pod velocity adjusted
	def checkPodProximity(self):
		for this_pod in interface.ObjReg.pod_registry:

			## Check if this_pod is buffering
			if this_pod.pod_buffering:
				this_pod.event_handler(Pod.CHECK_POD_BUFFER)
				# If this_pod is buffering there is no need to iterate through the other pods
				continue
			#

			## If this_pod is not buffering scan through all other pods,
			## and check if this_pod is too close to pod.
			## If it is to close to another pod initiate pod buffer condition
			for pod in interface.ObjReg.pod_registry:
				## Skip itself
				if this_pod.ID == pod.ID:
					continue

				## Only initiate buffer for pods ahead of this_pod
				if this_pod.isBehind(pod):
					## Check if within the buffer range
					buffer_range = abs(pod.SPRITE.x - this_pod.SPRITE.x)
					if  buffer_range <= self.config.POD_BUFFER_RANGE:
						this_pod.event_handler(Pod.START_PB, pod)



	def checkNodePodContact(self):
		for node in interface.ObjReg.node_registry:
			for pod in interface.ObjReg.pod_registry:
				if node.isContact(pod):
					## Only trigger event if the pod if buffering
					if pod.node_buffering:
						pod.event_handler(command=Pod.HAS_CONTACT, node=node)
						#pod.hasContact(node)


	def setPositionChecker(self):
		## Start position checker after 1/2 seconds
		if not self.log_position_SET:
			self.timer += dt
			if self.timer >= 0.5:
				logger.debug('---- POSITION CHECKER ENABLED ----')
				pyglet.clock.schedule_interval(self.case_1_position_checker, self.config.PULSE_WIDTH)
				self.log_position_SET = True

	## Get the position every 1/2 of a second.
	def case_1_position_checker(self, dt):
		for pod in interface.ObjReg.pod_registry:
			data_logger.info('P_{}'.format(pod.SPRITE.x))


	def case_1_pod_position(self, dt):
		for pod in interface.ObjReg.pod_registry:
			logger.debug('POD {} | POSITION {}'.format(pod.ID, pod.SPRITE.x))


if __name__ == "__main__":
	## Establish Data Files
        data_FILE = '/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/data_FILE.txt'
        log_FILE = '/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/logdump.log'
	
	## Clear Data Files
	subprocess.call('rm {}'.format(data_FILE), shell=True)
	subprocess.call('rm {}'.format(log_FILE), shell=True)

	## Create Logger Structure
	logging.basicConfig(level=logging.DEBUG, filename='logdump.log') # Top Level...everything goes into the diump
	
	logger = logging.getLogger('Process_Logger') # Log application process
	
	##TODO: Mess with format...make look nice
	#logger.format()

	console_handler = logging.StreamHandler()
	logger.addHandler(console_handler) ## Handler sends LogEvents to stderr
	logger.debug('Process_Logger Online')
	
	data_logger = logging.getLogger('data_logger')
	data_handler = logging.FileHandler(data_FILE)
	data_handler.setLevel(logging.INFO)
	data_logger.addHandler(data_handler)
	#data_logger.addHandler(console_handler)

	## Create Window
	interface = Interface(w=1200, h=480, c="Interface")

	## Config
	config = Config.Config(interface)

	## Run app
	pyglet.app.run()



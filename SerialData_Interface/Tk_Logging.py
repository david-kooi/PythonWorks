from logging import Handler
from Tkinter import *

class Tk_Logging_Handler(Handler):

	def __init__(self, level, listbox):
		self.listbox = listbox
		Handler.__init__(self, level=level)

	def emit(self, record):
		msg = "{0}:{1}:{2} ".format(record.name, record.levelname, record.msg)
		self.listbox.insert(END, msg)

		

	
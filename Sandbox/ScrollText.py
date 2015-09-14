import Tkinter
from ScrolledText import *
 
root = Tkinter.Tk(className=" Another way to create a Scrollable text area")
textPad = ScrolledText(root, width=50, height=40)
textPad.pack()
root.mainloop()

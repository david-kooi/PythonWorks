import Tkinter as tk
from Tkinter import *



class Graphical_Interface(tk.Tk):

    

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        
        ## Set Title and icon for window 
#        top_title = Tk_config['top_title']
#        icon = Tl_config['window_icon']

        #tk.Tk.iconbitmap(self, default={}).format(icon)
 #       tk.Tk.wm_title(self, {title}).format(title = top_title)

        container = tk.Frame(self)
        
        Label(container, text='Bleh').grid(row=0)
        Label(container, text='Another').grid(row=0)
    
if __name__=='__main__':
    config = {}
    config['top_title']='TITLE!'
    config['window_icon'] = 'bslfndk.jpg'
    GUI = Graphical_Interface(**config)
#    GUI.mainloop()

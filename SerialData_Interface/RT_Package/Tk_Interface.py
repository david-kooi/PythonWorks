import Config 
import Tkinter as tk
from Tkinter import *



class Tk_Interface(tk.Tk):

    

    def __init__(self, tk_config, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)
           
        ## Set Title and icon for window 
        top_title = tk_config['top_title']
        icon = tk_config['window_icon']
        
        #tk.Tk.iconbitmap(self, default={}).format(icon)
        tk.Tk.wm_title(self, top_title)
       
        main_frame = Frame(height=900, width=1000, bg="#a6a8a4")
        main_frame.grid(column=0)

        left_frame = Frame(main_frame, width = 200, height = 900, bg="#30ff33") 
        left_frame.grid(sticky=tk.W, row=0,column=0)
        
        graph_frame = Frame(main_frame, width = 800, height = 600, bg="#ab5950")
        graph_frame.grid(sticky=tk.NE, row=0, column=1)
    
if __name__=='__main__':
    tk_config = {}
    tk_config['top_title']='TITLE!'
    tk_config['window_icon'] = 'bslfndk.jpg'

    GUI = Tk_Interface(tk_config)
    GUI.mainloop()

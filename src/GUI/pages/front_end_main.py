import tkinter as tk
import sys
import os



sys.path.insert(0, './src')

from GUI.objects.window.window import window
from GUI.pages.landing_page import landing_page

def initialise_front_end():
    root = tk.Tk()
    # this section defines the root and the background frame
    window(root)
    landing_page(root)
    root.mainloop()

#2.12.0rc0    

if __name__ == "__main__":
    initialise_front_end()

import tkinter as tk
from tkinter import ttk

def scroll_list(root,display_width, display_height ,entry_height, dictionary, variable, entry_function):
    #this section puts the frame containing the scroll list entries into a scrollable canvas, and updates the canvases configure to make it 
    # changes shape with the frame.
    object_container = tk.Frame(root,height = 50, width = display_width, bg='dimgray', highlightbackground='dimgray')
    object_container.custom_tag = 'scroll_list'
    canvas = tk.Canvas(object_container, width = (display_width-4), height = display_height, bg='dimgray', highlightbackground='dimgray')
    list_frame = tk.Frame(canvas, bg="dimgray", highlightbackground='dimgray')
    list_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
    )
    canvas.update_idletasks()

    # this places the frame as a window in the canvas, and assigns a scroll bar
    canvas.create_window((((display_width/2)),0) , window=list_frame, anchor='center')
    scrollbar = ttk.Scrollbar(object_container, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)


    # this determines what kind of entries will be in the scroll list, and then calls the appropriate function
    # this doesn't feel very exstensible so i will try to refactor it after i have finished a first pass at the entire
    # front end
    entry_function(list_frame,display_width,entry_height, dictionary, variable,display_height)

    root.update_idletasks()
    #once the list is initially rendered, this section calculates if the list entries have a combined height of less than the screen
    # and pads under them if they do, thus preventing users from scrolling down when they can already see the whole list.
    exception_frame = tk.Frame(list_frame,height=1, highlightbackground='dimgray', bg='dimgray',name='exception_frame')
    if list_frame.winfo_height() < display_height:
        exception_frame.pack(side = 'bottom',fill='both', expand=(True), pady=(0,(display_height-list_frame.winfo_height())))
    else:
        exception_frame.pack(side = 'bottom',fill='both', expand=(True))

    # this finalises the geoemtry manager positions for the objects
    object_container.pack(side='left',expand=True)
    canvas.pack(side = 'left')
    scrollbar.pack(side = 'left', fill='y')
    object_container.update_idletasks()
    canvas.yview_moveto(0)
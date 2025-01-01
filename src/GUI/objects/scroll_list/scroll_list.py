import tkinter as tk
from tkinter import ttk

def callback_exception_frame(list_frame,exception_frame,display_height,total_height):
    # this creates and then calls back a frame which pads the bottom of any display lists whose entries have a combined height less than
    # that of the display window, this stops it being possible to scroll down near empty lists.
    current_total_height = 0
    for widget in list_frame.winfo_children():
        if widget.winfo_name() == 'exception_frame':
            exception_frame = widget
        else:
            current_total_height += widget.winfo_height()
    if total_height != current_total_height:
        widget.update_idletasks()  # Ensure the widget's geometry is updated
        exception_frame.pack_forget()  # Remove the widget from its current packing
        exception_frame.pack(side='bottom', fill='x',pady=(0,(max((display_height-current_total_height),0))))  # Re-pack it at the bottom
    list_frame.after(1000,lambda: callback_exception_frame(list_frame,exception_frame,display_height,current_total_height))

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

    list_frame.after(1000,lambda: callback_exception_frame(list_frame,tk.Frame(list_frame,height=1, highlightbackground='dimgray', bg='dimgray',name='exception_frame'),display_height,0))

    # this finalises the geoemtry manager positions for the objects
    object_container.pack(side='top',expand=True)
    canvas.pack(side = 'left')
    scrollbar.pack(side = 'left', fill='y')
    object_container.update_idletasks()
    canvas.yview_moveto(0)
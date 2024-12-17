import tkinter as tk
from PIL import Image, ImageTk
from GUI.objects.scroll_list.scroll_list import scroll_list
from GUI.objects.scroll_list.scroll_list_entries.image_display_scroll_list_entries import update_image_display_entries


def output_page(root,output_queue):
    #def check_queue(root, output_queue):
        #while not output_queue.empty():
            #result = output_queue.get()
           # image = Image.open( f"./images/trial_{result['trial_number']}/pertubed/image_0.png")
            #image = ImageTk.PhotoImage(image)
            #print('this is the queue as received in the main thread' + str(result))
            #label = tk.Label(root,image = image)
           # label.image = image
            #label.pack(side = 'top')
        #root.after(500, lambda: check_queue(root,output_queue))
    




    for widget in root.winfo_children():
        widget.destroy()

    top_frame = tk.Frame(root, bg="dimgray", highlightthickness=2, highlightbackground='black', height=200)
    top_frame.pack(side = 'top',fill = tk.X)
    bottom_frame = tk.Frame(root, bg="dimgray", height=200)
    bottom_frame.pack(side = 'top',fill='both', expand=(True))

    # this section defines the bottom left frame and the attack list
    left_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    scroll_list(left_frame,display_width=100,display_height=300,entry_height=33, dictionary = output_queue, variable = None, entry_function = update_image_display_entries)
    left_frame.pack(side = 'left',fill='both', expand=(True))

    middle_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    middle_frame.pack(side = 'left',fill='both', expand=(True))

    right_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    right_frame.pack(side = 'left',fill='both', expand=(True))


    #root.after(100,lambda: check_queue(root,output_queue))
import tkinter as tk
from PIL import Image
import numpy as np

def denormalize_and_save_image(image,ident,type):
    display_2 = Image.fromarray(((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8))
    display_2.save(f'./images/{type}/image_{ident}.png')

from tkinter import ttk

def define_window(root):
    #this component defines the aesthetic attributes of the window and the application background
    root.title('adversarial trial runner')
    root.geometry("1500x750")
    root.resizable(False, False)
    root.attributes('-topmost', 1)
    root.configure(bg='dimgray')
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def scroll_list_entries(root,display_width, type = 'attacks'):
    # based on passed though parameter we determine the type of content and how long the list is.
    # iterate though a for loop where for enteries in the content list we add a button with whatever
    # default styling is appropriate then call a function to create a appropriate entry content object within the button widget
    # we will also need to create a flag for whether the button is clickable or just a container
    length = 5
    height = 2
    interactive= True

    def button_event():
        print('the button event triggered')
        return True

    for counter in range(0,length):
        Button = tk.Button(root,text = counter,command=button_event, height = height,width=display_width)
        if interactive == False:
            Button.config(state=tk.DISABLED)
        Button.pack(side = 'top',fill='x', expand=(True))
    root.update_idletasks()


def scroll_list(root,display_width = 100, display_height = 100):
    object_container = tk.Frame(root,height = 50, width = display_width, bg='dimgray', highlightbackground='dimgray')
    canvas = tk.Canvas(object_container, width = (display_width-4), height = display_height, bg='dimgray', highlightbackground='dimgray')
    list_frame = tk.Frame(canvas, bg="dimgray", highlightbackground='dimgray')
    list_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
    )
    canvas.update_idletasks()
    canvas.create_window((((display_width/2)),0) , window=list_frame, anchor='center')
    scrollbar = ttk.Scrollbar(object_container, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)


    scroll_list_entries(list_frame,display_width)

    root.update_idletasks()
    expection_frame = tk.Frame(list_frame,height=1, highlightbackground='dimgray', bg='dimgray')
    if list_frame.winfo_height() < display_height:
        expection_frame.pack(side = 'top',fill='both', expand=(True), pady=(0,(display_height-list_frame.winfo_height())))
    else:
        expection_frame.pack(side = 'top',fill='both', expand=(True))


    object_container.pack(side='left',expand=True)
    canvas.pack(side = 'left')
    scrollbar.pack(side = 'left', fill='y')
    object_container.update_idletasks()
    canvas.yview_moveto(0)

def front_end_main():
    root = tk.Tk()
    define_window(root)
    top_frame = tk.Frame(root, bg="dimgray", highlightthickness=2, highlightbackground='black', height=200)
    top_frame.pack(side = 'top',fill = tk.X)
    bottom_frame = tk.Frame(root, bg="dimgray", height=200)
    bottom_frame.pack(side = 'top',fill='both', expand=(True))
    left_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    left_frame.pack(side = 'left',fill='both', expand=(True))
    middle_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    middle_frame.pack(side = 'left',fill='both', expand=(True))
    right_frame = tk.Frame(bottom_frame, bg="dimgray", highlightthickness=2, highlightbackground='black')
    right_frame.pack(side = 'left',fill='both', expand=(True))
    scroll_list(left_frame)
    root.mainloop()

if __name__ == "__main__":
    front_end_main()
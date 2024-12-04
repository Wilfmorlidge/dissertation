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




def scroll_list(root):
    display_width = 100
    display_height = 100
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


    left_frame = tk.Frame(list_frame, bg="dimgray", highlightthickness=1, highlightbackground='black',width=display_width, height = 1)
    left_frame.pack(side = 'top',fill='both', expand=(True))
    middle_frame = tk.Frame(list_frame, bg="dimgray", highlightthickness=1, highlightbackground='green', height = 1)
    middle_frame.pack(side = 'top',fill='both', expand=(True))
    right_frame = tk.Frame(list_frame, bg="dimgray", highlightthickness=1, highlightbackground='black', height = 1)
    right_frame.pack(side = 'top',fill='both', expand=(True))

    root.update_idletasks()
    expection_frame = tk.Frame(list_frame,height=1, highlightbackground='dimgray')
    print('this is the height of the frame' + str(list_frame.winfo_height()))
    if list_frame.winfo_height() < display_height:
        print('life is not purposeful')
        expection_frame.pack(side = 'top',fill='both', expand=(True), pady=(0,(display_height-list_frame.winfo_height())))
    else:
        expection_frame.pack(side = 'top',fill='both', expand=(True))


    object_container.pack(side='left',expand=True)
    canvas.pack(side = 'left')
    scrollbar.pack(side = 'left', fill='y')

    object_container.update_idletasks()

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
import tkinter as tk
from PIL import Image
import numpy as np

def denormalize_and_save_image(image,ident,type):
    display_2 = Image.fromarray(((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8))
    display_2.save(f'./images/{type}/image_{ident}.png')

from tkinter import ttk

def define_window(window):
    #this component defines the aesthetic attributes of the window and the application background
    window.geometry("1500x750")
    window.resizable(False, False)
    window.attributes('-topmost', 1)
    window.configure(bg='dimgray')
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def front_end_main():
    root = tk.Tk()
    define_window(root)
    top_frame = tk.Frame(root, bg="lightblue", width=100, height=200)
    top_frame.pack(fill = tk.X)
    root.mainloop()

if __name__ == "__main__":
    front_end_main()
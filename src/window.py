import tkinter as tk
from PIL import Image
import numpy as np

def denormalize_and_save_image(image,ident,type):
    display_2 = Image.fromarray(((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8))
    display_2.save(f'./images/{type}/image_{ident}.png')

from tkinter import ttk

def define_window(window):
    #this component defines the aesthetic attributes of the window and the application background
    window.title('adversarial trial runner')
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
    root.mainloop()

if __name__ == "__main__":
    front_end_main()